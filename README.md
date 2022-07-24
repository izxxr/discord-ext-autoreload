# discord-ext-autoreload
A discord.py extension that allows automatic hot-reloading of extensions

When it comes to bot development, reloading extensions at runtime is quite a common practice.
However, currently there is no way of automatically hot reloading extensions. This simple
extension allows you to conveniently auto-reload extensions.

The features of this extension are:

- Easy to setup and use
- Proper exceptions handling during auto-reload
- Minimal interface matching that of discord.py
- Compatible with both discord.py 1.7 and 2.0

## Installation
This extension can easily be installed using `pip`:
```bash
pip install discord-ext-autoreload
```

## Usage
The `Reloader` class is used for setting up automatic reloads.
```py
import discord
from discord.ext import commands, autoreload

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
reloader = autoreload.Reloader(ext_directory="cogs")

if __name__ == "__main__":
    reloader.start(bot)
    bot.run()
```

<details>
  <summary>For discord.py 2.0</summary>
  <br/>

  In discord.py 2.0 and higher, you would need to call the `reloader.start()`
  method in an async context. The most convenient way of doing this is by
  overriding the `Bot.setup_hook()` method.

  ```py
  class Bot(commands.Bot):
    async def setup_hook(self) -> None:
        reloader.start(self)
  ```

</details>

And done! The `Reloader` class will start watching the provided `ext_directory` for
changes in loaded extensions and as soon as an extension is updated, It will automatically
be reloaded.
