# discord-ext-autoreload
A discord.py extension that allows automatic hot-reloading of extensions

When it comes to bot development, reloading extensions at runtime is quite a common practice.
However, currently there is no way of automatically hot reloading extensions. This simple
extension allows you to conveniently auto-reload extensions.

The features of this extension are:

- Easy to setup and use
- Proper exceptions handling during auto-reload
- Minimal interface matching that of discord.py
- Compatible with both discord.py v1.7 and v2.0

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

### Stopping the reloader
Sometimes, you might want to stop the reloader. You can use the `Reloader.stop()` method
to easily do so. For example:

```py
@bot.command()
async def togglereload(ctx):
    if reloader.stopped:
        reloader.start(bot)
        await ctx.send("Enabled")
    else:
        reloader.stop()
        await ctx.send("Disabled")
```

### Error Handling
When auto reloading fails for some reason, the error is properly handled and propagated
to `Reloader.on_error`. This function by default logs the error but can be overridden to
implement custom functionality.

```py
import traceback

class Reloader(autoreload.Reloader):
    async def on_error(self, extension: str):
        print(f"Extension {extension!r} failed to auto reload")
        traceback.print_exc()
```

### Tracking reloads
When an extension is reloaded, the `Reloader.on_reload` method is called. This method can
be implemented by a subclass to easily track successful automatic reloads.

### Excluding extensions from reloading
Sometimes, you want certain extensions to not be subject of automatic reloading. Fortunately,
this package allows you to exclude certain extensions by passing the `exclude_exts` keyword
argument in `Reloader` class.
```py
reloader = Reloader(ext_directory="cogs", exclude_exts=["cogs.some_extension"])
```
