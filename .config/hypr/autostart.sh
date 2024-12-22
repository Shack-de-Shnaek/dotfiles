#!/bin/sh

/bin/greenclip daemon >/dev/null &
/bin/emacs --daemon &
/bin/waybar &
# nohup bash ./startup_program.sh &
