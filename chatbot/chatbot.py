import requests
import json
import os

class AIChatbot:

    def __init__(self):

        self.messages = []

    def generate_response(self, user_input):

        self.messages.append({
            "role": "user",
            "content": user_input
        })

        response = requests.post(
            "http://localhost:11434/api/chat",
            json={
                "model": "tinyllama",
                "messages": self.messages,
                "stream": False
            }
        )

        data = response.json()

        bot_reply = data["message"]["content"]

        self.messages.append({
            "role": "assistant",
            "content": bot_reply
        })

        return bot_reply

    def save_chat(self):

        with open("chat_history.json", "w") as file:
            json.dump(self.messages, file, indent=4)

    def load_chat(self):

        try:
            if os.path.exists("chat_history.json"):

                with open("chat_history.json", "r") as file:

                    content = file.read().strip()

                    if content:
                        self.messages = json.loads(content)

        except Exception as e:
            print("Starting fresh chat:", e)
            self.messages = []