# commands.py
import openai
import os
import subprocess

# Set your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

def execute_task(command, speak_func):
    """Determine command type and execute"""
    
    # Local commands example
    if "notepad" in command:
        speak_func("Opening Notepad")
        subprocess.Popen("notepad.exe")
        return

    elif "calculator" in command:
        speak_func("Opening Calculator")
        subprocess.Popen("calc.exe")
        return

    # AI knowledge query
    else:
        response = ask_ai(command)
        speak_func(response)
        return

def ask_ai(prompt):
    """Send query to ChatGPT API and get response"""
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role":"user", "content": prompt}]
        )
        answer = completion.choices[0].message.content
        return answer
    except Exception as e:
        print(f"AI error: {e}")
        return "Sorry, I could not fetch an answer right now."
