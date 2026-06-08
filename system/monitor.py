import psutil


def get_system_info():

    # ==========================================
    # CPU
    # ==========================================
    cpu_usage = psutil.cpu_percent(interval=1)

    # ==========================================
    # RAM
    # ==========================================
    ram_usage = psutil.virtual_memory().percent

    # ==========================================
    # BATTERY
    # ==========================================
    battery = psutil.sensors_battery()

    if battery:

        battery_percent = battery.percent

        charging = (
            "Yes"
            if battery.power_plugged
            else "No"
        )

    else:

        battery_percent = "N/A"

        charging = "N/A"

    return {

        "cpu": cpu_usage,

        "ram": ram_usage,

        "battery": battery_percent,

        "charging": charging
    }