#!/bin/sh

nohup picom --config ~/.config/picom/picom.conf &
nohup feh --bg-fill /usr/share/endeavouros/backgrounds/endeavouros-wallpaper.png &
nohup greenclip daemon >/dev/null &
nohup kdeconnect-indicator &
nohup dunst &
