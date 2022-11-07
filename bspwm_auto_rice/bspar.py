import os
import typer
import pywal
from . import dependencies
from . import autoricer
from typing import Optional

cli = typer.Typer()

deps = ["bspwm", "polybar", "sxhkd", "picom", "downgrade", "dmenu", "code", "neovim", "rofi", "dunst", "alacrity", "feh"]

@cli.command(help="Install dependencies")
def install():
    dependencies.install_deps_pacman(deps)
    dependencies.downgrade_rofi()
    dependencies.get_dots()

@cli.command(help="Sets a wallpaper and if -c is not passed, it will generate a colorscheme from the wallpaper and apply it system-wide,\nelse it will use the colorscheme passed with -c")  
def set(wallpaper:str = typer.Option(..., "-w", "--wallpaper",help="Absolute path to wallpaper", ), colorscheme:str = typer.Option(None, "-c", "--colorscheme", help="colorscheme preset name\nsee 'bspar colors'")):
    if os.path.isabs(wallpaper):
        autoricer.auto_rice(wallpaper, colorscheme)
    else:
        raise typer.BadParameter("Wallpaper path must be absolute", param_hint="wallpaper path")
    
@cli.command(help="Lists all available colorschemes presets")
def colors():
    pywal.theme.list_out()
    

if __name__ == "__main__":
    cli()