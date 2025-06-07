#!/bin/bash

case "$1" in
    Reboot)
        echo "Rebooting..."
        reboot
        ;;
    Shutdown)
        echo "Shutting down..."
        systemctl poweroff
        ;;
    Suspend)
        echo "Suspending..."
        systemctl suspend
        ;;
    Logout)
        echo "Logging out..."
        hyprctl dispatch exit
        ;;
    *)
        echo "Usage: $0 {Reboot|Shutdown|Suspend|Lock}"
        exit 1
        ;;

esac
