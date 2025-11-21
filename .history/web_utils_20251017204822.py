import pywhatkit as kit

def play_youtube(video_name):
    try:
        if not video_name:
            video_name = "latest trending"
        kit.playonyt(video_name)
        return f"Playing {video_name} on YouTube"
    except Exception as e:
        return f"Error opening YouTube: {e}"

def google_search(query):
    try:
        if not query:
            query = "latest news"
        kit.search(query)
        return f"Searching for '{query}' on Google"
    except Exception as e:
        return f"Error searching Google: {e}"

def send_whatsapp_msg(number, message, hour, minute):
    try:
        kit.sendwhatmsg(number, message, hour, minute)
        return f"WhatsApp message scheduled to {number}"
    except Exception as e:
        return f"Error sending WhatsApp message: {e}"
