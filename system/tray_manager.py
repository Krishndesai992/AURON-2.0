import threading

import pystray

from PIL import Image, ImageDraw


tray_icon = None


# ==========================================
# CREATE ICON IMAGE
# ==========================================

def create_image():

    image = Image.new(
        "RGB",
        (64, 64),
        color=(15, 23, 42)
    )

    draw = ImageDraw.Draw(image)

    draw.ellipse(
        (16, 16, 48, 48),
        fill=(59, 130, 246)
    )

    return image


# ==========================================
# SHOW WINDOW
# ==========================================

def show_window(app):

    app.after(
        0,
        app.deiconify
    )

    global tray_icon

    if tray_icon:

        tray_icon.stop()


# ==========================================
# EXIT APP
# ==========================================

def quit_window(app):

    global tray_icon

    if tray_icon:

        tray_icon.stop()

    app.destroy()


# ==========================================
# MINIMIZE TO TRAY
# ==========================================

def minimize_to_tray(app):

    global tray_icon

    app.withdraw()

    image = create_image()

    menu = pystray.Menu(

        pystray.MenuItem(
            "Open AURON",
            lambda: show_window(app)
        ),

        pystray.MenuItem(
            "Exit",
            lambda: quit_window(app)
        )
    )

    tray_icon = pystray.Icon(
        "AURON",
        image,
        "AURON 2.0",
        menu
    )

    threading.Thread(
        target=tray_icon.run,
        daemon=True
    ).start()