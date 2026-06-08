import psutil


def get_battery_status():

    battery = psutil.sensors_battery()

    if battery is None:
        return "Battery information not available."

    percent = battery.percent
    plugged = battery.power_plugged

    charging = "Charging" if plugged else "Not Charging"

    return f"Battery: {percent}% | {charging}"