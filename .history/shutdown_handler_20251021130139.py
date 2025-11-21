import os
import subprocess
import time
from close_utils import close_app  # तुम्हारा existing function apps close करने के लिए

# ✅ Close all apps before system action
def close_all_apps_before_action():
    apps_to_close = [
        "notepad","chrome","winword","excel","powerpnt",
        "code","spotify","msedge"
    ]
    for app in apps_to_close:
        close_app(app)
    time.sleep(1)  # apps close होने का time

# 🔹 Shutdown
def shutdown_pc():
    close_all_apps_before_action()
    subprocess.call("shutdown /s /t 1", shell=True)

# 🔹 Restart
def restart_pc():
    close_all_apps_before_action()
    subprocess.call("shutdown /r /t 1", shell=True)

# 🔹 Sleep
def sleep_pc():
    close_all_apps_before_action()
    subprocess.call("rundll32.exe powrprof.dll,SetSuspendState 0,1,0", shell=True)

# 🔹 Lock
def lock_pc():
    subprocess.call("rundll32.exe user32.dll,LockWorkStation", shell=True)

# 🔹 Handle command string
def handle_shutdown_command(command: str) -> str:
    command = command.lower()

    if any(word in command for word in ["shutdown", "shut down", "power off", "बंद करो", "शटडाउन"]):
        shutdown_pc()
        return "सभी ऐप्स बंद किए गए। सिस्टम shutdown हो गया।"

    if any(word in command for word in ["restart", "reboot", "रीस्टार्ट"]):
        restart_pc()
        return "सभी ऐप्स बंद किए गए। सिस्टम restart हो गया।"

    if any(word in command for word in ["hibernate", "sleep", "स्लीप", "हाइबरनेट"]):
        sleep_pc()
        return "सभी ऐप्स बंद किए गए। सिस्टम sleep mode में चला गया।"

    if any(word in command for word in ["lock", "लॉक", "स्क्रीन लॉक"]):
        lock_pc()
        return "सिस्टम लॉक हो गया।"

    return "System command समझ नहीं आया।"
