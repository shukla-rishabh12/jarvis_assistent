# shutdown_handler.py
import subprocess
import re
import time
from ai_sense import ask_gemini
from voice_utils import speak, listen

def parse_shutdown_intent_with_gemini(user_text):
    """
    Ask Gemini to normalize the user command into a short structured string.
    Expected output examples Gemini may return (we parse text): 
      - "shutdown now"
      - "shutdown in 5 minutes"
      - "restart now"
      - "hibernate now"
      - "cancel"
    If Gemini fails, we'll fallback to simple keyword parsing.
    """
    prompt = (
        "Interpret this user command for PC power control. "
        "Return a concise instruction like: 'shutdown now', "
        "'shutdown in 5 minutes', 'restart now', 'hibernate now' or 'cancel'. "
        "User command: " + user_text
    )
    resp = ask_gemini(prompt)
    if not resp:
        return None
    return resp.strip().lower()

def fallback_parse(command):
    """
    Simple fallback parser (if Gemini not available). Returns struct as tuple:
    (action, seconds) where action in ['shutdown','restart','hibernate','cancel'].
    seconds is delay in seconds (0 means immediate).
    """
    cmd = command.lower()
    # cancel keywords
    if any(x in cmd for x in ["cancel", "no", "नहीं", "रद्द"]):
        return ("cancel", 0)
    # restart
    if any(x in cmd for x in ["restart", "reboot", "रीस्टार्ट", "रिस्टार्ट", "पुनः आरंभ"]):
        # check for time like "in 5 minutes"
        m = re.search(r"(\d+)\s*(minute|minutes|min|m|minut|मिनट)", cmd)
        if m:
            secs = int(m.group(1)) * 60
        else:
            secs = 0
        return ("restart", secs)
    # hibernate
    if any(x in cmd for x in ["hibernate", "हाइबर", "हाइबरनेट", "hybernate"]):
        return ("hibernate", 0)
    # shutdown
    if any(x in cmd for x in ["shutdown", "shut down", "power off", "shutdown", "बंद", "शटडाउन", "power off", "शट डाउन"]):
        m = re.search(r"(\d+)\s*(minute|minutes|min|m|मिनट)", cmd)
        if m:
            secs = int(m.group(1)) * 60
        else:
            # maybe "in 30 sec" or "after 10 seconds"
            m2 = re.search(r"(\d+)\s*(second|seconds|sec|s|सेकंड)", cmd)
            if m2:
                secs = int(m2.group(1))
            else:
                secs = 0
        return ("shutdown", secs)
    return (None, 0)

def execute_system_power(action, seconds=0):
    """
    Execute the actual system command.
    Windows: shutdown /s /t seconds  ; restart: shutdown /r /t seconds ; hibernate: rundll32.exe powrprof.dll,SetSuspendState 0,1,0
    Returns message string describing what was done (not spoken).
    """
    try:
        if action == "shutdown":
            # /s = shutdown, /t seconds
            cmd = ["shutdown", "/s", "/t", str(int(seconds))]
            subprocess.run(cmd, check=False)
            return f"System will shutdown in {seconds} seconds."
        elif action == "restart":
            cmd = ["shutdown", "/r", "/t", str(int(seconds))]
            subprocess.run(cmd, check=False)
            return f"System will restart in {seconds} seconds."
        elif action == "hibernate":
            # try hibernate (may require privileges)
            # On some systems use: rundll32.exe powrprof.dll,SetSuspendState 0,1,0
            try:
                subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"], check=False)
                return "System hibernate command issued."
            except Exception:
                return "Hibernate command could not be executed on this system."
        elif action == "cancel":
            subprocess.run(["shutdown", "/a"], check=False)  # abort pending shutdown
            return "Pending shutdown cancelled."
        else:
            return "Unknown action."
    except Exception as e:
        return f"Error executing system command: {e}"

def handle_shutdown_command(user_text):
    """
    Main entrypoint for intent_recognizer to call.
    Steps:
      1) Try Gemini to parse intent into normalized action.
      2) Fallback parse if needed.
      3) Ask user for confirmation (speak+listen).
      4) If confirmed, execute the corresponding system command.
    Returns: result text (string).
    """
    # 1) Gemini parse
    parsed = parse_shutdown_intent_with_gemini(user_text)
    if parsed:
        # parsed examples: "shutdown now", "shutdown in 5 minutes", "restart now"
        # do basic parsing
        if "cancel" in parsed:
            action = "cancel"; secs = 0
        elif "restart" in parsed:
            action = "restart"
            m = re.search(r"(\d+)\s*minute", parsed)
            secs = int(m.group(1))*60 if m else 0
        elif "hibernate" in parsed:
            action = "hibernate"; secs = 0
        elif "shutdown" in parsed:
            action = "shutdown"
            m = re.search(r"(\d+)\s*minute", parsed)
            if m:
                secs = int(m.group(1))*60
            else:
                # seconds?
                m2 = re.search(r"(\d+)\s*second", parsed)
                secs = int(m2.group(1)) if m2 else 0
        else:
            action = None; secs = 0
    else:
        # fallback parse
        action, secs = fallback_parse(user_text)

    if not action:
        return "मैं समझ नहीं पाया कि आप क्या करना चाहते हैं। कृपया फिर से कहिए (shutdown/restart/hibernate/cancel)।"

    # 3) Ask for confirmation before executing destructive action
    # If action is cancel, perform immediately without confirmation
    if action == "cancel":
        res = execute_system_power("cancel", 0)
        return res

    # prepare human-friendly confirmation message
    if secs and secs > 0:
        minutes = secs // 60
        confirm_msg = f"आपने कहा कि सिस्टम को {action} किया जाए, {minutes} मिनट बाद। क्या मैं आगे बढ़ूँ? (हाँ/नहीं)"
    else:
        confirm_msg = f"आपने कहा कि सिस्टम को तुरंत {action} किया जाए। क्या मैं आगे बढ़ूँ? (हाँ/नहीं)"

    speak(confirm_msg)
    # listen for confirmation
    reply = listen().lower()
    if any(x in reply for x in ["yes", "हाँ", "ha", "haan", "haan", "yes sir", "ji"]):
        # execute
        result_text = execute_system_power(action, secs)
        # speak final message
        speak("ठीक है सर। " + result_text)
        return result_text
    else:
        speak("ठीक है sir, मैंने शटडाउन/रिस्टार्ट कैंसिल कर दिया/नहीं किया।")
        return "User cancelled the action."
