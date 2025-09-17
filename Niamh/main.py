import logging
import uuid
from niamh.niamh import NiamhAI
from core.llm_handler import LLMHandler

# Initialize logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Initialize Niamh AI
llm = LLMHandler()
niamh = NiamhAI(llm)

# Generate a unique session ID for conversation tracking
session_id = str(uuid.uuid4())

print("\n🤖 Welcome! You are now chatting with Niamh. Type 'exit' to end the conversation.\n")

while True:
    user_input = input("User: ")

    if user_input.lower() in ["exit", "quit"]:
        print("\n👋 Goodbye! Ending chat session.\n")
        break

    response = niamh.generate_response(session_id, user_input)
    print(f"Niamh: {response}\n")
