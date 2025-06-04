#!/bin/sh

nohup picom --config ~/.config/picom/picom.conf &
# nohup feh --bg-fill /usr/share/endeavouros/backgrounds/endeavouros-wallpaper.png &
feh --bg-fill "$HOME"/.config/qtile/wallpapers/hi.res.png
nohup greenclip daemon >/dev/null &
nohup dunst &
nohup kdeconnect-indicator &
nohup playerctld daemon &
