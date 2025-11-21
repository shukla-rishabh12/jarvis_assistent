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

def get_driver(headless=False):
    options = webdriver.ChromeOptions()
    # Keep browser visible; if you later want headless, set headless=True
    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # optional: keep user profile to avoid repeated popups
    # options.add_argument(r"--user-data-dir=C:\Users\<you>\AppData\Local\Google\Chrome\User Data")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def paste_and_get_answer(question, timeout=30):
    """
    Opens the target URL, pastes the question in the input box, submits it,
    waits for the answer to appear, returns answer text.
    """
    driver = None
    try:
        driver = get_driver(headless=False)
        driver.get(TARGET_URL)
        wait = WebDriverWait(driver, 20)

        # Wait for page load - attempt multiple ways to find the input area
        input_el = None
        # Strategy 1: look for textarea
        try:
            input_el = wait.until(EC.presence_of_element_located((By.TAG_NAME, "textarea")))
        except:
            input_el = None

        # Strategy 2: contenteditable div (common in chat UIs)
        if input_el is None:
            try:
                input_el = driver.find_element(By.CSS_SELECTOR, "div[contenteditable='true']")
            except:
                input_el = None

        # Strategy 3: input with role textbox or aria-label
        if input_el is None:
            candidates = driver.find_elements(By.CSS_SELECTOR, "input, textarea")
            if candidates:
                input_el = candidates[0]

        if input_el is None:
            # last resort: try to click body and send keys
            body = driver.find_element(By.TAG_NAME, "body")
            body.click()
            input_el = body

        # Focus and paste/send question
        try:
            input_el.click()
        except Exception:
            pass

        # Clear existing text if possible
        try:
            input_el.clear()
        except Exception:
            pass

        # Send the question. For contenteditable div we send keys.
        input_el.send_keys(question)
        input_el.send_keys(Keys.ENTER)

        # Wait for response to appear.
        # Heuristic: wait for a new message container to appear after submit.
        # We'll try multiple selectors commonly used:
        answer_text = ""
        possible_answer_selectors = [
            "div.response, .response, div.answer, .answer",
            "div[class*='assistant'], div[class*='response']",
            "div[class*='message'] div[class*='content']",
            "div[class*='chat-line']",
            # Google's SGE / other snippets not applicable here; kept generic
        ]
        # Wait loop: poll for visible text different from question
        deadline = time.time() + timeout
        last_text = ""
        while time.time() < deadline:
            page_text = driver.find_element(By.TAG_NAME, "body").text
            # crude approach: find a block of text that is not the question
            if len(page_text) > len(question):
                # try to extract last reply - simplistic: split lines and take last non-empty
                lines = [ln.strip() for ln in page_text.splitlines() if ln.strip()]
                if len(lines) >= 1:
                    # find last line that is not the question text
                    for ln in reversed(lines):
                        if question.strip().lower() not in ln.strip().lower():
                            last_text = ln
                            break
                if last_text and last_text != answer_text:
                    answer_text = last_text
                    # small pause to let full answer render
                    time.sleep(0.6)
                    # re-read body to capture possibly multi-line answer
                    page_text2 = driver.find_element(By.TAG_NAME, "body").text
                    # try to get contiguous block containing last_text
                    if last_text in page_text2:
                        idx = page_text2.rfind(last_text)
                        answer_text = page_text2[idx:].strip()
                    break
            time.sleep(0.6)

        if not answer_text:
            # fallback: try to find first element with long text
            elements = driver.find_elements(By.XPATH, "//*[string-length(normalize-space())>50]")
            if elements:
                answer_text = elements[-1].text

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

def execute_command(text):
    """
    Main dispatcher: open local apps if requested,
    otherwise treat as knowledge question and use the target page.
    """
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
