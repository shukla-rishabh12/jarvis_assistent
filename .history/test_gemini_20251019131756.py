import pywhatkit as kit
import datetime

number = "+918127972296"
message = "Hello, यहtge है!"

# Current time +2 minutes (safe)
now = datetime.datetime.now()
hour = now.hour
minute = now.minute+0.1  # Minimum 1–2 min ahead required

print(f"Message scheduled to {number} at {hour}:{minute}...")

kit.sendwhatmsg(number, message, hour, minute)

print("✅ WhatsApp message sche")
