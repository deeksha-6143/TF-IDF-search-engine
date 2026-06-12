from chatbot import AIChatbot

def main():

    bot = AIChatbot()

    bot.load_chat()

    print("AI Chatbot Started")
    print("Type 'exit' to quit")

    while True:

        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit", "bye"]:

            bot.save_chat()

            print("Chat saved.")
            break

        response = bot.generate_response(user_input)

        print("\nBot:", response)

if __name__ == "__main__":
    main()