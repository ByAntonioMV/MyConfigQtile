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


from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy


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


    
]


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
    padding='3',
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    font="FiraCode Nerd Font",
                    fontsize=18,              # Reduce un poco para elegancia
                    padding_y=6,
                    padding_x=12,
                    highlight_method="line",  # Línea inferior en vez de bloque
                    this_current_screen_border="#ffffff",
                    inactive="#666666",       # Color de grupos inactivos
                    active="#ffffff",         # Color de grupos activos
                    highlight_color=["#C0C0C0", "#222222"],  # Fondo al resaltar (se mantiene neutro)
                    disable_drag=True,
                    equal=True,
                    rounded=False,
                    borderwidth=2,
                    margin_y=4, 
                ),
                widget.Prompt(),    
                widget.WindowName(),  
                widget.Systray(), 

                widget.Net(
                    interface="wlan0",
                    format="Red: ↓{down} ↑{up}",
                    prefix="M",
                ),

                widget.Battery(
                    format="Batería: {percent:2.0%}",
                    show_short_text=False,
                ),

                widget.Volume(
                    emoji=False,  
                    format="Volumen: {percent:2.0%}"
                ),

                widget.Clock(format="Fecha: %d/%m/%Y  Hora: %H:%M"),  

                widget.CurrentLayout(format="Diseño: {name}"),
            ],  
            32, 
            background="#333241",
            margin=[5, 5, 5, 5],
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
