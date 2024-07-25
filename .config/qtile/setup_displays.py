from xdg import IconTheme
import subprocess

from libqtile.command.client import InteractiveCommandClient
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

client = InteractiveCommandClient()

from config import (
    terminal,
    screens,
    launch_programs,
    bar_defaults,
    widget_defaults,
    BACKGROUND,
    DISABLED,
    spawn_program,
)

import custom_widgets


def calendar_notification():
    subprocess.run(["notify-send", "Calendar"])


GroupBox = widget.GroupBox(
    highlight_method="line",
    **widget_defaults,
)

Keyboard = widget.KeyboardLayout(
    configured_keyboards=["us", "mk"],
    **widget_defaults,
)

Clock = widget.Clock(format="%Y-%m-%d %I:%M %p", **widget_defaults)


def get_top_bar():
    widgets = [
        widget.CurrentLayout(**widget_defaults),
        GroupBox,
        widget.Prompt(**widget_defaults),
        widget.WindowName(**widget_defaults),
        widget.Sep(padding=4, foreground=DISABLED),
        custom_widgets.PlayerCtlSongNameWidget(text="", **widget_defaults),
        custom_widgets.PlayerCtlPrevWidget(text="", **widget_defaults),
        custom_widgets.PlayerCtlPlayPauseWidget(text="", **widget_defaults),
        custom_widgets.PlayerCtlNextWidget(text="", **widget_defaults),
        widget.Sep(padding=4, foreground=DISABLED),
        widget.PulseVolume(
            update_interval=0.01,
            mouse_callbacks={"Button3": lazy.spawn(f"{terminal} alsamixer")},
        ),
        widget.CapsNumLockIndicator(**widget_defaults),
        Keyboard,
        widget.Systray(),
        Clock,
    ]
    top_bar = bar.Bar(widgets, **bar_defaults)
    return top_bar


def get_launcher_bar():
    return bar.Bar(
        [
            widget.Spacer(length=bar.STRETCH),
            *[
                widget.Image(
                    filename=IconTheme.getIconPath(program["icon_name"]),
                    margin=4,
                    mouse_callbacks={"Button1": lazy.function(spawn_program(program["command"]))},
                )
                for program in launch_programs
            ],
            widget.Spacer(length=bar.STRETCH),
        ],
        background=BACKGROUND,
        size=36,
        margin=[4, 0, 4, 0],
    )


def setup_displays():
    for screen in client.screens:
        print(screen)
        screen.top = get_top_bar()


screens[1].bottom = get_launcher_bar()

setup_displays()
