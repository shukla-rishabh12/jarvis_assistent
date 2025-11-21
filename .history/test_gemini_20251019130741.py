import pywhatkit as kit
import datetime

# 📇 Test contact number (with country code)
number = "+918127972296"  # Replace with your number

# 💬 Message to send
message = "Hello, यह WhatsApp test message है!"

# ⏰ Current time +1 minute for pywhatkit
now = datetime.datetime.now()
hour = now.hour
minute = now.minute + 1  # pywhatkit requires at least 1 min in future

print(f"Message scheduled to {number} at {hour}:{minute}...")

# Send WhatsApp message
kit.sendwhatmsg(number, message, hour, minute)

print("✅ WhatsApp message scheduled successfully!")
