# set up for custom widget that uses playerctl to control music, and display the current song
from libqtile.widget import base


class PlayerCtlSongNameWidget(base.ThreadPoolText):
    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [
        ("update_interval", 1, "Update interval for the PlayerCtl widget."),
    ]

    def __init__(self, **config):
        super().__init__(**config)
        self.add_defaults(PlayerCtlSongNameWidget.defaults)

    def poll(self):
        import subprocess

        try:
            status_command = ["playerctl", "status"]
            meta_command = ["playerctl", "metadata"]
            # spotify_status = (
            #     subprocess.check_output(["playerctl", "status", "--player=spotify"]).decode("utf-8").strip()
            # )
            # if spotify_status != "No players found":
            #     status_command.append("--player=spotify")
            #     meta_command.append("--player=spotify")
            # else:
            #     return "No spotify"

            status = subprocess.check_output(status_command).decode("utf-8").strip()
            if status not in ["Playing", "Paused"]:
                return status
                return "It's quiet..."

            song = subprocess.check_output(meta_command + ["title"]).decode("utf-8").strip()
            artist = subprocess.check_output(meta_command + ["artist"]).decode("utf-8").strip()
            return f"{song} -- {artist}"
        except subprocess.CalledProcessError as e:
            return "error"
            return "It's quiet..."


class PlayerCtlPrevWidget(base.ThreadPoolText):
    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [
        ("update_interval", 100, "Update interval for the PlayerCtl widget."),
    ]

    def __init__(self, **config):
        super().__init__(**config)
        self.add_defaults(PlayerCtlPrevWidget.defaults)

    def poll(self):
        import subprocess

        try:
            status = subprocess.check_output(["playerctl", "status"]).decode("utf-8").strip()
            if status not in ["Playing", "Paused"]:
                return ""
            return "⟪"
        except subprocess.CalledProcessError:
            return ""

    def button_press(self, x, y, button):
        import subprocess

        subprocess.run(["playerctl", "previous"])


class PlayerCtlNextWidget(base.ThreadPoolText):
    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [
        ("update_interval", 100, "Update interval for the PlayerCtl widget."),
    ]

    def __init__(self, **config):
        super().__init__(**config)
        self.add_defaults(PlayerCtlNextWidget.defaults)

    def poll(self):
        import subprocess

        try:
            status = subprocess.check_output(["playerctl", "status"]).decode("utf-8").strip()
            if status not in ["Playing", "Paused"]:
                return ""
            return "⟫"
        except subprocess.CalledProcessError:
            return ""

    def button_press(self, x, y, button):
        import subprocess

        subprocess.run(["playerctl", "next"])


class PlayerCtlPlayPauseWidget(base.ThreadPoolText):
    orientations = base.ORIENTATION_HORIZONTAL
    defaults = [
        ("update_interval", 0.5, "Update interval for the PlayerCtl widget."),
    ]

    def __init__(self, **config):
        super().__init__(**config)
        self.add_defaults(PlayerCtlPlayPauseWidget.defaults)

    def poll(self):
        import subprocess

        try:
            status = subprocess.check_output(["playerctl", "status"]).decode("utf-8").strip()
            if status not in ["Playing", "Paused"]:
                return ""
            return "⏸" if status == "Playing" else "▶"
        except subprocess.CalledProcessError:
            return ""

    def button_press(self, x, y, button):
        import subprocess

        subprocess.run(["playerctl", "play-pause"])
