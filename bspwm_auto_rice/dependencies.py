import os
from rich import print


def install_deps_pacman(deps):
    deps = " ".join(deps)
    command = f"sudo pacman -S {deps}"
    print(f"[bold red]Executing: {command}")
    os.system(command)


def downgrade_rofi():
    command = "sudo downgrade rofi==1.6.1"
    print(f"[bold red]Executing: {command}")
    os.system(command)


def get_dots():
    cd_command = f"cd /home/{os.getlogin()}/.local/share"
    git_command = "git clone https://github.com/AbdelrhmanNile/bspwm-auto-rice-dots.git"
    print(f"[bold red]Executing: {cd_command} && {git_command}")
    os.system(f"{cd_command} && {git_command}")


def build_st():
    cd_command = f"cd /home/{os.getlogin()}/.local/share/bspwm_auto_rice/st"
    make_command = "make"
    print(f"[bold red]Executing: {cd_command} && {make_command}")
    os.system(f"{cd_command} && {make_command}")
