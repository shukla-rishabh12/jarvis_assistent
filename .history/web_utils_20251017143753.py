import pywhatkit

def play_youtube(video_name):
    try:
        pywhatkit.playonyt(video_name)
        return f"Playing {video_name} on YouTube"
    except Exception as e:
        return f"Error: {e}"

def google_search(query):
    try:
        pywhatkit.search(query)
        return f"Searching for {query} on Google"
    except Exception as e:
        return f"Error: {e}"

def send_whatsapp_msg(number, message, hour, minute):
    try:
        pywhatkit.sendwhatmsg(number, message, hour, minute)
        return f"Message scheduled to {number}"
    except Exception as e:
        return f"Error: {e}"
