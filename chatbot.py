
import sys
import requests

# ==========================================
# ANZMA TECH - LOCAL AI CHATBOT
# ==========================================

# Local Ollama API. No cloud services or API keys.
OLLAMA_URL = "http://localhost:11434/api/chat"

# Available local models
MODELS = {
    "1": "qwen2.5:3b",
    "2": "llama3.2:3b"
}

# UTF-8 support for Arabic and English terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

if hasattr(sys.stdin, "reconfigure"):
    sys.stdin.reconfigure(encoding="utf-8")


# ==========================================
# SYSTEM PROMPT
# ==========================================

SYSTEM_PROMPT = """
You are Anzma Tech's bilingual AI assistant, specializing in
building security, physical security, and access-control systems.

LANGUAGE RULES:
- Detect whether the user is writing in Arabic or English.
- Always answer in the same language as the user's question.
- For Arabic questions, use clear, natural, professional Modern Standard Arabic.
- Avoid mixing English words into Arabic sentences.
- When a technical English term is necessary, provide its Arabic equivalent
  and put the English term in parentheses only once.
- Never produce corrupted, incomplete, or invented words.

ANSWER QUALITY:
- Give accurate, relevant, and practical answers.
- Structure technical answers with headings or numbered steps when useful.
- Do not invent system features, incidents, or facts.
- Distinguish possible causes from confirmed causes.
- For security incidents, recommend safe, authorized investigation steps.
- Never recommend bypassing access controls or compromising security.

CONVERSATION:
- Use the previous messages in the conversation when answering follow-up questions.
- If the required information is not available in the conversation, say so.
- Do not pretend to remember information that was never provided.
"""


# ==========================================
# MODEL SELECTION
# ==========================================

def select_model():

    print("\n" + "=" * 55)
    print("ANZMA TECH - LOCAL AI CHATBOT")
    print("=" * 55)

    print("\nSelect a local AI model:")
    print("1. Qwen 2.5 3B")
    print("2. Llama 3.2 3B")

    while True:

        choice = input("\nEnter 1 or 2: ").strip()

        if choice in MODELS:
            return MODELS[choice]

        print("Invalid selection. Please enter 1 or 2.")


# ==========================================
# CHAT FUNCTION
# ==========================================

def chat(model):

    conversation = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    print("\n" + "=" * 55)
    print("ANZMA TECH - LOCAL AI CHATBOT")
    print(f"Selected model: {model}")
    print("Languages: Arabic / English")
    print("Type 'exit' to quit.")
    print("=" * 55)

    while True:

        try:

            user_input = input("\nYou: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ("exit", "quit"):
                print("\nChatbot: Goodbye!")
                break

            conversation.append({
                "role": "user",
                "content": user_input
            })

            payload = {
                "model": model,
                "messages": conversation,
                "stream": False,
                "options": {
                    "num_ctx": 2048
                }
            }

            print("\nAssistant: Thinking...")

            response = requests.post(
                OLLAMA_URL,
                json=payload,
                timeout=300
            )

            response.raise_for_status()

            result = response.json()

            answer = result["message"]["content"]

            print(f"\nAssistant: {answer}")

            conversation.append({
                "role": "assistant",
                "content": answer
            })

            # Keep system prompt and latest 10 messages
            if len(conversation) > 11:
                conversation = (
                    [conversation[0]] + conversation[-10:]
                )

        except requests.exceptions.ConnectionError:

            print("\nError: Cannot connect to Ollama.")
            print("Check that the local Ollama server is running.")

            conversation.pop()

        except requests.exceptions.Timeout:

            print("\nError: The model response timed out.")

            conversation.pop()

        except requests.exceptions.RequestException as error:

            print(f"\nRequest error: {error}")

            conversation.pop()

        except (KeyError, ValueError) as error:

            print(f"\nInvalid response from Ollama: {error}")

            conversation.pop()

        except KeyboardInterrupt:

            print("\n\nChatbot stopped.")
            break


# ==========================================
# MAIN FUNCTION
# ==========================================

def main():

    model = select_model()

    chat(model)


if __name__ == "__main__":
    main()
