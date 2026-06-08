import threading
import keyboard


listener_running = False
listener_thread = None


# ==========================================
# HOTKEY LISTENER LOOP
# ==========================================

def hotkey_loop(callback):

    keyboard.add_hotkey(
        "ctrl+alt+a",
        callback
    )

    keyboard.wait()


# ==========================================
# START HOTKEY LISTENER
# ==========================================

def start_hotkey_listener(callback):

    global listener_running
    global listener_thread

    if listener_running:
        return

    listener_running = True

    listener_thread = threading.Thread(
        target=hotkey_loop,
        args=(callback,),
        daemon=True
    )

    listener_thread.start()


# ==========================================
# STOP HOTKEY LISTENER
# ==========================================

def stop_hotkey_listener():

    global listener_running

    keyboard.unhook_all_hotkeys()

    listener_running = False