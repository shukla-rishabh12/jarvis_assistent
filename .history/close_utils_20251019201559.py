import os
import subprocess
import psutil

def close_app(app_name):
    import psutil, os

    # Jarvis और terminal-safe रखने के लिए exclude
    exclude_processes = ["python.exe", "pythonw.exe", "Code.exe", "cmd.exe", "powershell.exe"]

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

    if app_name in ["all", "सभी"]:
        for pname in app_processes.values():
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if pname.lower() in proc.info['name'].lower() and proc.info['name'] not in exclude_processes:
                        os.system(f"taskkill /f /pid {proc.info['pid']}")
                        closed_apps.append(proc.info['name'])
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
        return f"✅ बंद किए गए ऐप्स: {', '.join(closed_apps)}" if closed_apps else "⚠️ कोई ऐप खुला नहीं था।"

    else:
        # Single app बंद करना
        pname = app_processes.get(app_name)
        if not pname:
            return f"❌ Unknown app: {app_name}"
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if pname.lower() in proc.info['name'].lower() and proc.info['name'] not in exclude_processes:
                    os.system(f"taskkill /f /pid {proc.info['pid']}")
                    closed_apps.append(proc.info['name'])
            except:
                pass
        return f"✅ बंद किए गए ऐप्स: {', '.join(closed_apps)}" if closed_apps else f"⚠️ {app_name} पहले से बंद है।"
