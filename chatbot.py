import os
from dotenv import load_dotenv
from openai import OpenAI

# Load API key from .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MAX_MESSAGES = 10

def chat():
    print("🤖 AI Chatbot (type 'quit' or 'exit' to stop)\n")

    # Initial system instruction for the AI
    messages = [{"role": "system", "content": "You are a helpful AI assistant."}]

    while True:
        try:
            user_input = input("You: ")
            if user_input.lower() in {"quit", "exit"}:
                print("Goodbye 👋")
                break

            # Add user message
            messages.append({"role": "user", "content": user_input})

            # Limit messages to the last MAX_MESSAGES for context
            messages = messages[-MAX_MESSAGES:]

            # Call OpenAI API
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )

            # Get AI reply
            reply = response.choices[0].message.content
            print(f"Bot: {reply}\n")

            # Add AI reply to messages
            messages.append({"role": "assistant", "content": reply})

        except KeyboardInterrupt:
            print("\nGoodbye 👋")
            break
        except Exception as e:
            print(f"⚠️ Error: {e}")
            print("Please check your API key, model, or internet connection.\n")

if __name__ == "__main__":
    chat()
