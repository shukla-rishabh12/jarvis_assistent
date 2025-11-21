# close_all_test.py
import os
import psutil

def close_app(app_name):
    """
    Close a specific app or all apps on Windows using psutil.
    """
    app_name = app_name.lower().strip()

    # App dictionary
    app_processes = {
        "notepad": "notepad.exe",
        "chrome": "chrome.exe",
        "word": "WINWORD.EXE",
        "powerpoint": "POWERPNT.EXE",
        "excel": "EXCEL.EXE",
        "vs code": "Code.exe",
        "spotify": "Spotify.exe",
        "edge": "msedge.exe"
    }

    closed_apps = []

    # Close all apps
    if app_name == "all" or app_name == "सभी":
        for pname in app_processes.values():
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if pname.lower() in proc.info['name'].lower():
                        os.system(f"taskkill /f /pid {proc.info['pid']}")
                        closed_apps.append(proc.info['name'])
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
        if closed_apps:
            return f"✅ बंद किए गए ऐप्स: {', '.join(closed_apps)}"
        else:
            return "⚠️ कोई ऐप खुला नहीं था।"

    # Close single app
    if app_name not in app_processes:
        return f"❌ Unknown app: '{app_name}'"
    
    pname = app_processes[app_name]
    closed = False
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if pname.lower() in proc.info['name'].lower():
                os.system(f"taskkill /f /pid {proc.info['pid']}")
                closed = True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return f"✅ {app_name.capitalize()} बंद कर दिया गया।" if closed else f"⚠️ {app_name.capitalize()} पहले से ही बंद है।"


# ✅ Test function
if __name__ == "__main__":
    print("खुला हुआ ऐप बंद करने के लिए 'close all' या किसी app का नाम डालें।")
    user_input = input("कमांड: ").strip().lower()

    if "close all" in user_input or "सभी" in user_input:
        result = close_app("all")
    else:
        result = close_app(user_input)
    
    print(result)
