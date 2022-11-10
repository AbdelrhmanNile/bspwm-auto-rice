import os
import typer
import pywal
from . import dependencies
from . import autoricer
from typing import Optional
from rich import print

cli = typer.Typer()

deps = [
    "bspwm",
    "polybar",
    "sxhkd",
    "picom",
    "downgrade",
    "dmenu",
    "code",
    "neovim",
    "rofi",
    "dunst",
    "alacrity",
    "feh",
]


@cli.command(help="Install dependencies")
def install():
    dependencies.install_deps_pacman(deps)
    dependencies.downgrade_rofi()
    dependencies.get_dots()


@cli.command(
    help="Sets a wallpaper and if -c is not passed, it will generate a colorscheme from the wallpaper and apply it system-wide,\nelse it will use the colorscheme passed with -c"
)
def set(
    wallpaper: str = typer.Option(
        ...,
        "-w",
        "--wallpaper",
        help="Absolute path to wallpaper",
    ),
    colorscheme: str = typer.Option(
        None, "-c", "--colorscheme", help="colorscheme preset name\nsee 'bspar colors'"
    ),
):
    if os.path.isabs(wallpaper):
        autoricer.auto_rice(wallpaper, colorscheme)
    else:
        raise typer.BadParameter(
            "Wallpaper path must be absolute", param_hint="wallpaper path"
        )


@cli.command(help="Lists all available colorschemes presets")
def colors(
    list_colors: bool = typer.Option(
        False,
        "-ls",
        "--list",
        help="Lists default coloschemes presets and user presets",
    ),
    use: str = typer.Option(
        None, "-u", "--use", help="use a colorscheme without a wallpaper"
    ),
    save: str = typer.Option(
        None,
        "-s",
        "--save",
        help="Save the current colorscheme as a user defined preset",
    ),
):
    if list_colors:
        pywal.theme.list_out()

    if use:
        autoricer.auto_rice("", use)

    if save:
        autoricer.save_cs(save)

    if list_colors == False and use == None and save == None:
        pywal.theme.list_out()


@cli.command(help="pulls the latest changes from dots repo")
def update(
    myself: Optional[bool] = typer.Option(None, "--self", "-s"),
    dots: Optional[bool] = typer.Option(None, "--dots", "-d"),
):
    if dots:
        command = f"cd {autoricer.bspwm_auto_rice_local_repo} && git pull"
        os.system(command)
    if myself:
        command = f"pip install --user --upgrade bspwm-auto-rice"
        os.system(command)

    if myself == None and dots == None:
        print("[bold red]wtf to update?\n\t-d : dots\n\t-s : bspar")


if __name__ == "__main__":
    cli()
