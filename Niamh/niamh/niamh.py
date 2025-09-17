import logging
from core.database import DatabaseManager
from agents.fact_checker import FactChecker

class NiamhAI:
    def __init__(self, llm):
        """Initialize Niamh AI with memory, LLM, and Fact-Checking."""
        self.db = DatabaseManager()
        self.llm = llm
        self.fact_checker = FactChecker()

    def generate_response(self, session_id, user_input):
        """Generate a response using Llama 3.1 and verify accuracy with Fact-Checker."""
        logging.info(f"Niamh received input: {user_input}")

        # Retrieve conversation context
        context = self.db.fetch_conversation_history(session_id)

        # Construct LLM prompt
        system_prompt = "You are Niamh, an AI assistant that provides intelligent and accurate responses."
        conversation_history = "\n".join(
            [f"User: {entry['user_input']}\nNiamh: {entry['ai_response']}" for entry in context]
        )
        full_prompt = f"{system_prompt}\n\nConversation History:\n{conversation_history}\n\nUser: {user_input}\nNiamh:"

        logging.info("🔹 Sending prompt to LLM...")
        ai_response = self.llm.generate_response(full_prompt)

        # ✅ Verify accuracy using Fact-Checker
        fact_checker_feedback = self.fact_checker.verify_fact(user_input, ai_response)

        # ✅ Ensure Fact-Checker’s response is checked before proceeding
        if fact_checker_feedback:
            summary = fact_checker_feedback["summary"]
            corrected_response = fact_checker_feedback["corrected_response"]
            source = fact_checker_feedback["source"]

            logging.info(f"⚠️ Fact-Checker found an issue: {summary}")
            
            # ✅ Present both responses to the human user
            print(f"\n🤖 Niamh: My original response was: \"{ai_response}\"")
            print(f"🔍 However, Fact-Checker suggests: \"{corrected_response}\" (Based on: {source})")
            print(f"📌 Summary of the issue: {summary}")

            # ✅ **Ask the user which response they believe is correct**
            user_choice = input("\n❓ Which response do you believe is correct? (1️⃣ - Mine, 2️⃣ - Fact-Checker's) ").strip()

            # ✅ **Store the user’s decision**
            final_response = ai_response if user_choice == "1" else corrected_response
            self.db.store_conversation(session_id, user_input, final_response)

            # ✅ **Log user feedback for RLHF/Fine-Tuning**
            self.db.store_knowledge(user_input, final_response, ["User Feedback"], f"User chose {'Niamh' if user_choice == '1' else 'Fact-Checker'}'s response.")

            return final_response

        # ✅ If Fact-Checker confirms accuracy, return the original response
        logging.info("✅ Fact-Checker confirmed Niamh's response as correct.")
        self.db.store_conversation(session_id, user_input, ai_response)
        return ai_response
