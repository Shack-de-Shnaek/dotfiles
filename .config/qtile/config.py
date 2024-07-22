import os
import subprocess

from xdg import IconTheme

from libqtile import hook
from libqtile import bar, layout, widget, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

mod = "mod4"
terminal = "kitty"
cursor_warp = True

BACKGROUND = '152128'
BACKGROUND_ALT = '334D5C'
FOREGROUND = 'DCE1E5'
PRIMARY = 'F5CC00'
SECONDARY = '336699'
ALERT = 'F5CC00'
DISABLED = '924F67'

@hook.subscribe.startup_complete
def autostart():
	autostart_script = os.path.expanduser('~/.config/qtile/scripts/autostart.sh')
	startup_programs = os.path.expanduser('~/.config/qtile/scripts/startup_programs.sh')
	# monitor_script = os.path.expanduser('~/.screenlayout/monitor.sh')
	subprocess.call(['sh', autostart_script, '&'], timeout=2, start_new_session=True)
	# subprocess.call(['sh', startup_programs, '&'], timeout=5, start_new_session=True)
	# subprocess.call(['sh', monitor_script, '&'], timeout=1, start_new_session=True)

groups = [Group(str(i)) for i in range(1, 10)]

def switch_to_screen(screen):
	def f(q):
		displays = list(q.screens)
		q.to_screen(displays[int(screen) - 1].index)
	return f

keys = [
	# A list of available commands that can be bound to keys can be found
	# at https://docs.qtile.org/en/latest/manual/config/lazy.html
	# Switch between windows
	Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
	Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
	Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
	Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
	Key([mod], "tab", lazy.layout.next(), desc="Move window focus to other window"),
	# Move windows between left/right columns or move up/down in current stack.
	# Moving out of range in Columns layout will create new column.
	Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
	Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
	Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
	Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
	# Grow windows. If current window is on the edge of screen and direction
	# will be to screen edge - window would shrink.
	Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
	Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
	Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
	Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
	Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
	# Toggle between split and unsplit sides of stack.
	# Split = all windows displayed
	# Unsplit = 1 window displayed, like Max layout, but still with
	# multiple stack panes
	Key(
		[mod, "shift"],
		"Return",
		lazy.layout.toggle_split(),
		desc="Toggle between split and unsplit sides of stack",
	),
	Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
	# Toggle between different layouts as defined below
	Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
	Key([mod, 'shift'], "Tab", lazy.prev_layout(), desc="Toggle between layouts"),
	Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
	Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
	Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

	# custom shit
	# rofi
	Key([mod], 'd', lazy.spawn('rofi -show drun -config ~/.config/rofi/rofidmenu.rasi'), desc="Spawn rofi in dmenu mode"),
	Key([mod, 'shift'], 'd', lazy.spawn('rofi -show run -config ~/.config/rofi/rofidmenu.rasi'), desc="Spawn rofi in window mode"),
	Key([mod], 't', lazy.spawn('rofi -show window -config ~/.config/rofi/rofidmenu.rasi'), desc="Spawn rofi in window mode"),
	Key([mod], 'c', lazy.spawn('rofi -modi "clipboard:greenclip print" -show clipboard -config ~/.config/rofi/rofidmenu.rasi'), desc="Show clipboard manager"),

	# screens
	Key([mod, 'control'], '1', lazy.function(switch_to_screen(1))),
	Key([mod, 'control'], '2', lazy.function(switch_to_screen(2))),

	# volume and media
	Key([], 'XF86AudioRaiseVolume', lazy.spawn('amixer -D pulse sset Master 5%+')),
	Key([], 'XF86AudioLowerVolume', lazy.spawn('amixer -D pulse sset Master 5%-')),
	Key([], 'XF86AudioMute', lazy.spawn('amixer sset Master toggle')),

	Key([], 'XF86AudioPlay', lazy.spawn('playerctl play-pause')),
	Key([], 'XF86AudioNext', lazy.spawn('playerctl next')),
	Key([], 'XF86AudioPrev', lazy.spawn('playerctl previous')),

	Key([], 'XF86MonBrightnessUp', lazy.spawn('brightnessctl set +5%')),
	Key([], 'XF86MonBrightnessDown', lazy.spawn('brightnessctl set 5-%')),

	Key([], 'Print', lazy.spawn('flameshot gui')),

	Key([mod], 'f', lazy.window.toggle_floating()),
	Key([mod], 'n', lazy.spawn('kitty nvim')),
]

for i in groups:
	keys.extend([
		Key(
			[mod],
			i.name,
			lazy.group[i.name].toscreen(),
			desc="Switch to group {}".format(i.name),
		),
		Key(
			[mod, "shift"],
			i.name,
			lazy.window.togroup(i.name, switch_group=False),
			desc="Switch to & move focused window to group {}".format(i.name),
		),
	])

layouts = [
	layout.Columns(border_focus_stack=[PRIMARY, SECONDARY], border_width=2, margin=4),
	layout.MonadWide(border_focus_stack=[PRIMARY, SECONDARY], border_width=2, margin=4, min_ratio=0.85, max_ratio=0.95, ratio=0.85),
	layout.Tile(),
	layout.Max(),
	layout.Stack(num_stacks=2),
	layout.Bsp(margin=4),
	layout.TreeTab(
		bg_color=BACKGROUND,
		active_bg=BACKGROUND_ALT,
		panel_width=240,
		padding_y=6,
		padding_x=8,
		sections=['ONE', 'TWO', 'THREE']
	),
]

widget_defaults = {
	'font': "sans",
	'fontsize': 16,
	'padding': 3,
	'foreground': FOREGROUND,
}

bar_defaults = {
	'margin': (0, 0, 4, 0),
	'background': BACKGROUND,
	'size': 32,
}

def spawn_program(program_command):
	command_arguments = program_command.split(' ')
	if program_command in ['btop']:
		command_arguments = ['kitty'] + command_arguments

	def f(q):
		q.spawn(command_arguments)
	return f

Keyboard = widget.KeyboardLayout(
	configured_keyboards=['us', 'mk'],
	**widget_defaults,
)

keys.extend([
	Key([mod], 'space', lazy.widget['keyboardlayout'].next_keyboard())
])

Clock = widget.Clock(format="%Y-%m-%d %I:%M %p", **widget_defaults)

GroupBox = widget.GroupBox(
	highlight_method='line',
	**widget_defaults,
)

launch_programs = [
	{
		'command': 'code',
		'icon_name': 'visual-studio-code',
	},
	{
		'command': 'slack',
		'icon_name': 'slack',
	},
	{
		'command': 'brave',
		'icon_name': 'brave-desktop',
	},
	{
		'command': 'discord',
		'icon_name': 'discord',
	},
	{
		'command': 'kitty',
		'icon_name': 'kitty',
	},
]

def get_launcher_bar():
	return bar.Bar(
		[
			widget.Spacer(length=bar.STRETCH),
			*[
				widget.Image(
					filename=IconTheme.getIconPath(program['icon_name']),
					margin=4,
					mouse_callbacks={
						'Button1': lazy.function(spawn_program(program['command']))
					}
				) for program in launch_programs
			],
			widget.Spacer(length=bar.STRETCH),
		],
		background=BACKGROUND,
		size=36,
		margin=[4, 0, 4, 0]
	)


screens = [
	Screen(
		top=bar.Bar(
			[
				widget.CurrentLayout(**widget_defaults),
				GroupBox,
				widget.Prompt(**widget_defaults),
				widget.WindowName(**widget_defaults),
				widget.Backlight(
					**widget_defaults,
					backlight_name="amdgpu_bl1",
					update_interval=0.1
				),
				widget.Battery(
					**widget_defaults,
					update_interval=0.1
				),
				widget.PulseVolume(
					update_interval=0.01,
					mouse_callbacks={
						'Button3': lazy.spawn('kitty alsamixer')
					},
				),
				widget.CapsNumLockIndicator(**widget_defaults),
				Keyboard,
				widget.Systray(),
				Clock,
			],
			**bar_defaults,
		),
	),
	Screen(
		top=bar.Bar(
			[
				widget.CurrentLayout(**widget_defaults),
				GroupBox,
				widget.Prompt(**widget_defaults),
				widget.WindowName(**widget_defaults),
				Keyboard,
				widget.CPU(),
				widget.CPUGraph(
					type='box',
					mouse_callbacks={
						'Button1': lazy.function(spawn_program('btop'))
					},
					border_color=SECONDARY,
					graph_color=PRIMARY,
				),
				widget.MemoryGraph(
					type='box',
					mouse_callbacks={
						'Button1': lazy.function(spawn_program('btop'))
					},
					border_color=BACKGROUND_ALT,
					graph_color=PRIMARY,
				),
				widget.Memory(),
				Clock,
				widget.QuickExit(),
			],
			**bar_defaults,
		),
	),
]

# Drag floating layouts.
mouse = [
	Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
	Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
	Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = True
floating_layout = layout.Floating(
	float_rules=[
		# Run the utility of `xprop` to see the wm class and name of an X client.
		*layout.Floating.default_float_rules,
		Match(wm_class="confirmreset"),  # gitk
		Match(wm_class="makebranch"),  # gitk
		Match(wm_class="maketag"),  # gitk
		Match(wm_class="ssh-askpass"),  # ssh-askpass
		Match(title="branchdialog"),  # gitk
		Match(title="pinentry"),  # GPG key password entry
		Match(title="Galculator"),
		Match(title="KCalc"),
	]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

wmname = "LG3D"
