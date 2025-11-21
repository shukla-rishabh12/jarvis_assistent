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
        subprocess.Popen(app_name)
        return f"{app_name} opened"
    except Exception as e:
        return f"Error opening {app_name}: {e}"
