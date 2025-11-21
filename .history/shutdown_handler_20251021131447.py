import os
import subprocess
import time
from close_utils import close_app  # तुम्हारा existing function apps close करने के लिए

# ✅ Close all important apps before system action
def close_all_apps_before_action():
    apps_to_close = [

    "notepad.exe",
    "chrome.exe",
    "WINWORD.EXE",
    "EXCEL.EXE",
    "POWERPNT.EXE",
    "Code.exe",
    "Spotify.exe",
    "msedge.exe"

    ]
    for app in apps_to_close:
        os.system(f"taskkill /f /im {app}")
    time.sleep(3)  # apps बंद होने का समय

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

# 🔹 Handle Gemini command
def handle_shutdown_command_from_gemini(command: str) -> str:
    """
    command: Gemini se processed command aaega (jaise 'shutdown', 'restart', 'sleep', 'lock')
    """

    command = command.lower()

    if "shutdown" in command or "shut down" in command or "power off" in command:
        shutdown_pc()
        return "सभी apps बंद किए गए। System shutdown हो गया।"

    if "restart" in command or "reboot" in command:
        restart_pc()
        return "सभी apps बंद किए गए। System restart हो गया।"

    if "sleep" in command or "hibernate" in command or "स्लीप" in command or "हाइबरनेट" in command:
        sleep_pc()
        return "सभी apps बंद किए गए। System sleep mode में चला गया।"

    if "lock" in command or "लॉक" in command:
        lock_pc()
        return "System लॉक हो गया।"

    return "Gemini command समझ नहीं आया।"
