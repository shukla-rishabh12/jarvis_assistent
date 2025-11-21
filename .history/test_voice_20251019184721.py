import os
import subprocess
import psutil

def close_app(app_name):
    """
    Close an application by its name (e.g., 'notepad', 'chrome', 'word').
    Works on Windows using psutil.
    """
    app_name = app_name.lower().strip()

    # Mapping app keywords to process names
    app_processes = {
        "notepad": "notepad.exe",
        "chrome": "chrome.exe",
        "word": "WINWORD.EXE",
        "powerpoint": "POWERPNT.EXE",
        "excel": "EXCEL.EXE",
        "vs code": "Code.exe",
        "spotify": "Spotify.exe",
        "edge": "msedge.exe"   # ✅ Microsoft Edge added
    }

    if app_name not in app_processes:
        return f"❌ Unknown app: '{app_name}'. Please add it to the dictionary."

    process_name = app_processes[app_name]
    closed = False

    # Iterate through running processes
    for process in psutil.process_iter(['pid', 'name']):
        try:
            if process_name.lower() in process.info['name'].lower():
                os.system(f"taskkill /f /pid {process.info['pid']}")
                closed = True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    if closed:
        return f"✅ {app_name.capitalize()} बंद कर दिया गया है।"
    else:
        return f"⚠️ {app_name.capitalize()} पहले से ही बंद है या नहीं मिला।"


# Example test
if __name__ == "__main__":
    app_to_close = input("कौन सा ऐप बंद करना है: ")
    print(close_app(app_to_close))
