#!/usr/bin/env python3
import os
import subprocess
import argparse
import shutil


def apply_cursor(cursor_name: str, cursor_size: str):
    """
    Apply cursor theme and size to Hyprland and GNOME.
    """
    subprocess.run(["hyprctl", "setcursor", cursor_name, cursor_size], check=True)
    subprocess.run([
        "gsettings", "set",
        "org.gnome.desktop.interface", "cursor-theme", cursor_name
    ], check=True)


def write_hypr_config(cursor_name: str, cursor_size: str, output_path: str, template_path: str = None):
    """
    Write hyprland cursor.conf. If template_path exists, use it,
    otherwise write default structure.
    """
    output_path = os.path.expanduser(output_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    if template_path:
        tpl_path = os.path.expanduser(template_path)
    else:
        tpl_path = None

    content = None
    if tpl_path and os.path.isfile(tpl_path):
        with open(tpl_path, 'r', encoding='utf-8') as tpl:
            content = tpl.read()
        content = content.replace("{{CURSOR}}", cursor_name)
        content = content.replace("{{SIZE}}", cursor_size)
    else:
        # default format
        content = f"$cursor = {cursor_name}\n$size = {cursor_size}\n"

    with open(output_path, 'w', encoding='utf-8') as outf:
        outf.write(content)


def update_gtk_settings(settings_path: str, cursor_name: str, cursor_size: str):
    """
    Update gtk-3.0 settings.ini with given cursor theme and size.
    """
    path = os.path.expanduser(settings_path)
    if not os.path.isfile(path):
        # If no existing settings, create directory and empty file
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8'):
            pass

    # Backup
    backup_path = f"{path}.bak"
    shutil.copy2(path, backup_path)

    lines = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('gtk-cursor-theme-name='):
                lines.append(f"gtk-cursor-theme-name={cursor_name}\n")
            elif line.startswith('gtk-cursor-theme-size='):
                lines.append(f"gtk-cursor-theme-size={cursor_size}\n")
            else:
                lines.append(line)

    # Ensure lines exist if not in file
    if not any(l.startswith('gtk-cursor-theme-name=') for l in lines):
        lines.append(f"gtk-cursor-theme-name={cursor_name}\n")
    if not any(l.startswith('gtk-cursor-theme-size=') for l in lines):
        lines.append(f"gtk-cursor-theme-size={cursor_size}\n")

    with open(path, 'w', encoding='utf-8') as f:
        f.writelines(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Set cursor theme & size for Hyprland, GNOME and GTK3 settings"
    )
    parser.add_argument("cursor", help="Cursor theme name")
    parser.add_argument("size",   help="Cursor size")
    parser.add_argument(
        "--template", "-t",
        help="Optional template file for hypr cursor conf"
    )
    parser.add_argument(
        "--hypr-conf", "-c",
        default="~/.config/hypr/cursor.conf",
        help="Hyprland config output path"
    )
    parser.add_argument(
        "--gtk-settings", "-g",
        default="~/.config/gtk-3.0/settings.ini",
        help="GTK3 settings.ini path"
    )
    args = parser.parse_args()

    apply_cursor(args.cursor, args.size)
    write_hypr_config(args.cursor, args.size, args.hypr_conf, args.template)
    update_gtk_settings(args.gtk_settings, args.cursor, args.size)
    print("Cursor theme and size applied successfully for Hyprland, GNOME, GTK3.")

if __name__ == "__main__":
    main()
