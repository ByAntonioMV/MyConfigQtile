# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, qtile, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
import os, subprocess

mod = "mod4"
terminal = "alacritty"


keys = [

    Key([mod], "Left", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "Right", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "Down", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "Up", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    
    Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="Move window up"),


    Key([mod, "control"], "Left", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "Right", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "Down", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "Up", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod], "Return", lazy.spawn(terminal), desc="Alacritty terminal"),
    Key([mod], "n", lazy.spawn("nm-connection-editor"), desc="Abrir gestor gráfico de red"),
    Key([mod], "b", lazy.spawn("blueman-manager"), desc="Abrir gestor gráfico de Bluetooth"),
    Key([mod], "t", lazy.spawn("thunar"), desc="Abrir gestor de archivos Thunar"),
    Key([mod], "g", lazy.spawn("google-chrome-stable"), desc="Abrir navegador Google Chrome"),
    Key([mod], "w", lazy.window.kill(), desc="Cerrar la ventana activa"),
    Key([mod], "p", lazy.spawn("dmenu_run"), desc="Abrir lanzador de aplicaciones dmenu"),
    Key([mod, "control"], "l", lazy.spawn("systemctl suspend"), desc="Suspender el sistema"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Cerrar sesión"),

]

# Audio keys
keys.extend([
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%"), desc="Subir volumen"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%"), desc="Bajar volumen"),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"), desc="Mute"),
])

# Brillo con xbacklight
keys.extend([
    Key([], "XF86MonBrightnessUp", lazy.spawn("xbacklight -inc 10"), desc="Subir brillo"),
    Key([], "XF86MonBrightnessDown", lazy.spawn("xbacklight -dec 10"), desc="Bajar brillo"),
])

for vt in range(1, 8):
    keys.append(
        Key(
            ["control", "mod1"],
            f"f{vt}",
            lazy.core.change_vt(vt).when(func=lambda: qtile.core.name == "wayland"),
            desc=f"Switch to VT{vt}",
        )
    )

groups = [
    Group("1", label=""),  # Nevegador
    Group("2", label=""),  # Espacio de trabajo 1
    Group("3", label=""),  # Espacion de Trabajo 2
    Group("4", label=""),  # Terminal
    Group("5", label=""),  # Terminal Git
    Group("6", label=""),  # Archivos
    Group("7", label="󰓇"),  # Musica
    Group("8", label=""),  # Grabación
]

for i in groups:
    keys.extend(
        [
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Switch to & move focused window to group {i.name}",
            ),
        ]
    )

layouts = [
    layout.MonadTall(),
    
]

widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding= 3,
)
extension_defaults = widget_defaults.copy()

def get_ssid():
    try:
        result = subprocess.check_output(["iwgetid", "-r"]).decode("utf-8").strip()
        return f"   {result}" if result else "睊 No conectado"
    except Exception:
        return "睊 Error"

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Spacer(length=15),
                
                # 🧩 GROUPBOX CENTRADO
                widget.GroupBox(
                    font="FiraCode Nerd Font",
                    fontsize=18,
                    padding_y=6,
                    padding_x=12,
                    highlight_method="line",
                    this_current_screen_border="#ffffff",
                    inactive="#666666",
                    active="#ffffff",
                    highlight_color=["#C0C0C0", "#222222"],
                    disable_drag=True,
                    equal=True,
                    rounded=False,
                    borderwidth=2,
                    margin_y=4, 
                ),

                widget.Prompt(
                    prompt="> ",
                    font="FiraCode Nerd Font",
                    fontsize=12,
                    padding=6,         # Más padding para indentación
                    foreground="#aaaaaa",
                    cursor_color="#888888",
                ),

                widget.WindowName(
                    font="FiraCode Nerd Font",
                    fontsize=12,
                    padding=12,         # Igual aquí para que coincida
                    foreground="#bbbbbb",
                    format="{name}",
                    max_chars=40,
                    markup=True,
                ),

                widget.Systray(
                    padding=4,
                    icon_size=18,
                ),

                widget.Spacer(length=bar.STRETCH),
                
                widget.Sep(linewidth=1, padding=10, foreground="#444444"),
                widget.GenPollText(
                    update_interval=10,
                    func=get_ssid,
                    fontsize=14,
                    padding=8,
                    foreground="#bbbbbb"
                ),
                widget.Sep(linewidth=1, padding=10, foreground="#444444"),

                widget.Battery(
                    format="  {percent:2.0%}",
                    show_short_text=False,
                    fontsize=14,
                    padding=8,
                    foreground="#bbbbbb"
                ),
                widget.Sep(linewidth=1, padding=10, foreground="#444444"),

                widget.Volume(
                    format="  {percent:2.0%}",
                    emoji=False,
                    fontsize=14,
                    padding=8,
                    foreground="#bbbbbb"
                ),
                widget.Sep(linewidth=1, padding=10, foreground="#444444"),

                widget.Clock(
                    format="  %d/%m |   %H:%M",
                    fontsize=14,
                    padding=8,
                    foreground="#bbbbbb"
                ),
                widget.Sep(linewidth=1, padding=10, foreground="#444444"),

                widget.CurrentLayout(
                    format="  {name}",
                    fontsize=14,
                    padding=8,
                    foreground="#bbbbbb"
                ),
                
                widget.Spacer(length=15),
            ],
            40, 
            background="#000000",
            margin=[10, 5, 10, 5],
        ),
    ),
]

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
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
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None
wl_xcursor_theme = None
wl_xcursor_size = 24
wmname = "LG3D"

def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen([home])
