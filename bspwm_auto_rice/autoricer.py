import pywal
import os
from distutils.dir_util import copy_tree
from rich import print
from time import sleep

dots_repo = "https://github.com/AbdelrhmanNile/bspwm-auto-rice-dots"

user = os.getlogin()
usr_config_dir = f"/home/{user}/.config"
usr_local_share_dir = f"/home/{user}/.local/share"
bspwmrc_path = f"/home/{user}/.config/bspwm/bspwmrc"
pywal_cache_dir = f"/home/{user}/.cache/wal"

bspwm_auto_rice_local_repo = f"/home/{user}/.local/share/bspwm-auto-rice"


def auto_rice(wallpaper, preset):

    if (not os.path.isdir(bspwm_auto_rice_local_repo)) or (
        len(os.listdir(bspwm_auto_rice_local_repo)) == 0
    ):
        print("[bold red]Downloading the dots...[/bold red]")
        os.system(f"git clone {dots_repo} {bspwm_auto_rice_local_repo}")
        copy_fonts()
        back_up_usr_conf()
        symlink_dots()

    if preset == None:
        colors = pywal.colors.get(wallpaper)
    else:
        colors = pywal.theme.file(preset)

    # colors_list = list(colors["colors"].values())
    # final_colors = pywal.colors.colors_to_dict(colors, wallpaper)
    pywal.export.every(colors)

    pywal.sequences.send(colors)
    alacritty_conf(colors["colors"])
    # betterdiscord_theme(colors["colors"])
    pywal.reload.xrdb()
    reload_bspwm()

    if wallpaper != "":
        set_wallpaper(wallpaper)

    generate_gtk_theme()
    generate_icons_theme()
    set_themes()


def reload_bspwm():
    print("[bold]Reloading bspwm")
    os.system(f"sh {bspwmrc_path} > /dev/null")
    sleep(1)


def set_wallpaper(wallpaper: str):
    print("[bold]Changing wallpaper")
    pywal.wallpaper.set_wm_wallpaper(wallpaper)
    os.system(
        f"sed -i '/feh/d' {bspwmrc_path} && echo 'feh --bg-fill {wallpaper} &' >> {bspwmrc_path}"
    )


def fix_oomox_gtk_colors():
    oomox_colors = open(f"{pywal_cache_dir}/colors-oomox", "r").read()
    oomox_colors = oomox_colors.splitlines()
    bg_color = oomox_colors[1].strip("BG=")
    oomox_colors[9] = f"BTN_BG={bg_color}"
    oomox_colors = "\n".join(oomox_colors)

    with open(f"{pywal_cache_dir}/colors-oomox", "w") as f:
        f.write(oomox_colors)


def generate_gtk_theme():
    print("[bold]building GTK3 theme")
    fix_oomox_gtk_colors()
    oomox_file_path = f"{pywal_cache_dir}/colors-oomox"
    gtk_theme_command = f"cd {bspwm_auto_rice_local_repo}/themes/gtk/materia && chmod +x change_color.sh && ./change_color.sh -o bspwm-auto-rice -t /home/{user}/.themes {oomox_file_path} > /dev/null"
    os.system(gtk_theme_command)


def generate_icons_theme():
    print("[bold]Building icons theme")
    oomox_file_path = f"{pywal_cache_dir}/colors-oomox"
    icons_theme_command = f"cd {bspwm_auto_rice_local_repo}/themes/icons/papirus && chmod +x change_color.sh && ./change_color.sh -o bspwm-auto-rice -d /home/{user}/.icons/bspwm-auto-rice {oomox_file_path} > /dev/null"
    os.system(icons_theme_command)


def set_themes():
    print("[bold]Setting themes")
    gtk3_ini_path = f"{usr_config_dir}/gtk-3.0/settings.ini"
    gtk_ini = open(gtk3_ini_path, "r").read()
    gtk_ini = gtk_ini.splitlines()
    gtk_ini[1] = "gtk-theme-name=bspwm-auto-rice"
    gtk_ini[2] = "gtk-icon-theme-name=bspwm-auto-rice"

    gtk_ini = "\n".join(gtk_ini)

    with open(gtk3_ini_path, "w") as f:
        f.write(gtk_ini)


def back_up_usr_conf():
    bspwm_bak_command = f"mv -r {usr_config_dir}/bspwm {usr_config_dir}/bspwm.bak"
    polybar_bak_command = f"mv -r {usr_config_dir}/polybar {usr_config_dir}/polybar.bak"
    sxhkd_bak_command = f"mv -r {usr_config_dir}/sxhkd {usr_config_dir}/sxhkd.bak"
    dunst_bak_command = f"mv -r {usr_config_dir}/dunst {usr_config_dir}/dunst.bak"
    rofi_bak_command = f"mv -r {usr_config_dir}/rofi {usr_config_dir}/rofi.bak"
    alacritty_bak_command = f"mv {usr_config_dir}/alacritty/alacritty.yml {usr_config_dir}/alacritty/alacritty.yml.bak"

    print("[bold red]Backing up your config files...[/bold red]")
    command = f"""{bspwm_bak_command} & \
                {polybar_bak_command} & \
                {sxhkd_bak_command} & \
                {dunst_bak_command} & \
                {rofi_bak_command} & \
                {alacritty_bak_command}"""

    print(f"[bold red]Running command: {command}")

    os.system(command)


def symlink_dots():
    os.symlink(
        f"{bspwm_auto_rice_local_repo}/dotconfig/bspwm",
        f"{usr_config_dir}/bspwm",
        target_is_directory=True,
    )
    os.symlink(
        f"{bspwm_auto_rice_local_repo}/dotconfig/polybar",
        f"{usr_config_dir}/polybar",
        target_is_directory=True,
    )
    os.symlink(
        f"{bspwm_auto_rice_local_repo}/dotconfig/sxhkd",
        f"{usr_config_dir}/sxhkd",
        target_is_directory=True,
    )
    os.symlink(
        f"{bspwm_auto_rice_local_repo}/dotconfig/dunst",
        f"{usr_config_dir}/dunst",
        target_is_directory=True,
    )
    os.symlink(
        f"{bspwm_auto_rice_local_repo}/dotconfig/rofi",
        f"{usr_config_dir}/rofi",
        target_is_directory=True,
    )
    os.symlink(
        f"{bspwm_auto_rice_local_repo}/dotconfig/picom",
        f"{usr_config_dir}/picom",
        target_is_directory=True,
    )


def copy_fonts():
    if not os.path.isdir(f"{usr_local_share_dir}/fonts"):
        os.makedirs(f"{usr_local_share_dir}/fonts")

    copy_tree(f"{bspwm_auto_rice_local_repo}/fonts", f"{usr_local_share_dir}/fonts")


def parse_templates(colors: dict, template_path: str):
    template = open(template_path, "r").readlines()
    conf = "".join(template).format(**colors)
    return conf


def parse_te(colors: dict, template_path: str):
    template = open(template_path, "r").readlines()
    for i, line in enumerate(template):
        if line.startswith("/**/"):
            template[i] = line.format(**colors)


def alacritty_conf(colors: dict):
    template = open(
        f"{bspwm_auto_rice_local_repo}/templates/alacritty.yml", "r"
    ).readlines()
    conf = "".join(template).format(**colors)
    conf = conf.replace("#", "")
    pywal.export.util.save_file(conf, f"{usr_config_dir}/alacritty/alacritty.yml")


def betterdiscord_theme(colors: dict):
    template = open(
        f"{bspwm_auto_rice_local_repo}/templates/comfywal.theme.css", "r"
    ).readlines()
    for i, line in enumerate(template):
        if line.startswith("/**/"):
            template[i] = line.format(**colors)

    conf = "".join(template)
    pywal.export.util.save_file(
        conf, f"{usr_config_dir}/BetterDiscord/themes/comfywal.theme.css"
    )


def update_dots():
    command = f"cd {bspwm_auto_rice_local_repo} && git pull"


def save_cs(name: str):
    commad = f"cp {pywal_cache_dir}/colors.json {usr_config_dir}/wal/colorschemes/dark/{name}.json"
    os.system(commad)
