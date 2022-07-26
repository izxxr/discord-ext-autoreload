# Copyright (C) nerdguyahmad 2022-2023
# This project is under the MIT License.

from __future__ import annotations

from typing import List, Optional
from discord.utils import MISSING
from discord.ext import commands

import os
import asyncio
import logging
import watchfiles

__all__ = (
    "Reloader",
)


_log = logging.getLogger(__name__)

def _get_ext_name(path: str) -> str:
    # On POSIX, relpath() returns the path with forward
    # slashes so we normalize them to backslashes
    path = os.path.relpath(path).replace("/", "\\")
    comps = path.split("\\")

    if comps[-1].endswith(".py"):
        # Strip the .py extension from the base name
        basename = comps.pop(-1)
        comps.append(basename[:-3])

    # For users that have subpackages inside their ext directory
    # with extension entry point in __init__.py, We will ignore
    # the __init__ to resolve the name to "ext_directory.subpackage".
    # This will break for users who add their extensions with 
    # name "ext_directory.subpackage.__init__" but that is a niche
    # case so it's a reasonable compromise
    return ".".join(comp for comp in comps if comp != "__init__")


class Reloader:
    """A class that allows automatic reloading of extensions.

    Parameters
    ----------
    ext_directory: :class:`str`
        The directory to watch for changes. This is the directory
        where your bot extensions are located. In most cases, this
        is ``cogs/``.
    exclude_exts: List[:class:`str`]
        The list of extension names to prevent from reloading. The
        strings must be in the same dotted format as the one passed
        to :meth:`discord.ext.commands.Bot.load_extension` method.
    """

    def __init__(self, ext_directory: str, exclude_exts: List[str] = MISSING) -> None:
        self.ext_directory = ext_directory
        self.exclude_exts = exclude_exts or []
        self.__reloader_task: Optional[asyncio.Task[None]] = None
        self.__stopped = asyncio.Event()
        self.__stopped.set()

    @property
    def stopped(self) -> bool:
        """:class:`bool`: Indicates whether the reloader is currently not running."""
        return self.__stopped.is_set()

    async def on_reload(self, extension: str) -> None:
        """A method that gets called when an extension is auto-reloaded.

        By default, this does nothing but subclasses may implement this
        method to implement custom functionality.

        Parameters
        ----------
        extension: :class:`str`
            The extension that was reloaded.
        """

    async def on_error(self, extension: str) -> None:
        """A method that gets called when auto-reloading an extension fails.

        By default, this does simply logs the error to logger but subclasses
        may implement a custom functionality.

        This method works in similar way as :func:`discord.on_error`, see it's
        documentation for more information.

        Parameters
        ----------
        extension: :class:`str`
            The extension that raised the error.
        """
        _log.exception("Ignoring exception while auto reloading extension %r", extension)

    def stop(self) -> None:
        """Stops watching for changes in extensions.

        This method is idempotent and does not raise any error
        if the reloader is already stopped.

        To check whether the reloader is running or not, use the
        :attr:`.stopped` property.
        """
        self.__stopped.set()
        if self.__reloader_task:
            self.__reloader_task.cancel()

        self.__reloader_task = None

    def start(self, bot: commands.Bot) -> None:
        """Starts watching for changes in extension.

        This method starts a background task and should be
        called in an async context. It is recommended to
        call this method during :meth:`discord.ext.commands.Bot.setup_hook`.

        Parameters
        ----------
        bot: :class:`discord.ext.commands.Bot`
            The bot instance.
        """
        if not self.stopped:
            raise RuntimeError("Reloader is already running")

        self.__reloader_task = bot.loop.create_task(
            self.__reloader_task_impl(bot=bot),
            name=f"reloader-task:{bot}",
        )

    async def _reload_extension(self, bot: commands.Bot, extension: str) -> None:
        try:
            coro = bot.reload_extension(extension)
            # For compatiblity with 1.7
            # In discord.py <2.0, reload_extension() is a
            # not a coroutine function
            if coro and asyncio.iscoroutine(coro):
                await coro
        except commands.ExtensionFailed:
            await self.on_error(extension)
        else:
            await self.on_reload(extension)

    async def __reloader_task_impl(self, bot: commands.Bot) -> None:
        self.__stopped.clear()

        # The type ignore here is because type of awatch() may be
        # partially unknown
        async for change_tup in watchfiles.awatch(self.ext_directory, stop_event=self.__stopped):  # type: ignore
            for change, path in change_tup:
                if change != watchfiles.Change.modified:
                    continue

                extension = _get_ext_name(path)
                if not extension in bot.extensions:
                    # Extension not loaded, so ignore
                    continue
                if extension in self.exclude_exts:
                    continue

                _log.info(f"Detected changes in {extension!r}, reloading.")
                bot.loop.create_task(self._reload_extension(bot=bot, extension=extension))
