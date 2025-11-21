import pyautogui
import subprocess
import os

def take_screenshot():
    file_path = "screenshot.png"
    pyautogui.screenshot(file_path)
    return f"Screenshot saved as {file_path}"

def open_notepad():
    try:
        subprocess.Popen("notepad.exe")
        return "Notepad opened"
    except Exception as e:
        return f"Error opening Notepad: {e}"

def open_app(app_name):
    try:
        app_name = app_name.lower()
        if "notepad" in app_name:
            os.startfile("notepad.exe")
        elif "vs code" in app_name or "code" in app_name:
            # Path to VS Code
            path = r"C:\Users\dell\AppData\Local\Programs\Microsoft VS Code\Code.exe"
            os.startfile(path)
        elif "chrome" in app_name:
            os.startfile("chrome.exe")
        else:
            return f"App '{app_name}' not configured"
        return f"{app_name} opened successfully"
    except Exception as e:
        return f"Error opening {app_name}: {e}"
