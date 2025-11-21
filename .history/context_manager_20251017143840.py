conversation_history = []

def add_to_history(user_input, assistant_response):
    conversation_history.append({
        "user": user_input,
        "assistant": assistant_response
    })

def get_history():
    return conversation_history
