# commands.py
import os
import time
from speech_utils import speak
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TARGET_URL = "https://chatgpt.com/g/g-p-68f1ef5ce9d881918cc07576d2373f56-jarvis1-0/c/68f1ef88-91b8-8322-9692-646b75139e59"

# ---------------- Local apps ----------------
def open_local_app(text):
    text = text.lower()
    if "notepad" in text:
        os.system("notepad")
        speak("Notepad khol diya.")
        return True
    if "calculator" in text or "calc" in text:
        os.system("calc")
        speak("Calculator khol diya.")
        return True
    if "chrome" in text or "browser" in text:
        os.system("start chrome")  # Windows
        speak("Browser khol diya.")
        return True
    return False

# ---------------- Selenium Driver ----------------
def get_driver(headless=False):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

# ---------------- Ask AI page ----------------
def paste_and_get_answer(question, timeout=30):
    driver = None
    try:
        driver = get_driver(headless=False)
        driver.get(TARGET_URL)
        wait = WebDriverWait(driver, 20)

        # Attempt to find input box (textarea or contenteditable)
        input_el = None
        try:
            input_el = wait.until(EC.presence_of_element_located((By.TAG_NAME, "textarea")))
        except:
            input_el = None

        if input_el is None:
            try:
                input_el = driver.find_element(By.CSS_SELECTOR, "div[contenteditable='true']")
            except:
                input_el = None

        if input_el is None:
            candidates = driver.find_elements(By.CSS_SELECTOR, "input, textarea")
            if candidates:
                input_el = candidates[0]

        if input_el is None:
            body = driver.find_element(By.TAG_NAME, "body")
            body.click()
            input_el = body

        try:
            input_el.click()
        except:
            pass

        try:
            input_el.clear()
        except:
            pass

        input_el.send_keys(question)
        input_el.send_keys(Keys.ENTER)

        # Wait and extract answer
        answer_text = ""
        deadline = time.time() + timeout
        while time.time() < deadline:
            page_text = driver.find_element(By.TAG_NAME, "body").text
            lines = [ln.strip() for ln in page_text.splitlines() if ln.strip()]
            last_text = ""
            for ln in reversed(lines):
                if question.strip().lower() not in ln.strip().lower():
                    last_text = ln
                    break
            if last_text:
                answer_text = last_text
                break
            time.sleep(0.5)

        if not answer_text:
            answer_text = "Sorry, main answer extract nahi kar paya."

        return answer_text

    except Exception as e:
        print("Error in paste_and_get_answer:", e)
        return f"Error: {e}"
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

# ---------------- Main Command Dispatcher ----------------
def execute_command(text):
    text = text.strip().lower()
    if not text:
        return

    # Exit command
    if text in ("exit", "quit", "stop", "shutdown"):
        speak("Shutting down. Bye.")
        raise SystemExit

    # Local apps
    if open_local_app(text):
        return

    # Otherwise search via the target AI page
    speak("Main aapke sawal ka jawab dhoondta hoon. Thoda intezar kijiye.")
    answer = paste_and_get_answer(text, timeout=40)
    print("Answer:", answer)
    speak(answer)
