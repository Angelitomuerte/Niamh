import logging
from core.database import DatabaseManager
from core.llm_handler import LLMHandler
from core.tools import Tools

class FactChecker:
    def __init__(self):
        """Initialize the Fact-Checker Agent"""
        self.db = DatabaseManager()
        self.llm = LLMHandler()
        self.tools = Tools()

    def verify_fact(self, user_input, ai_response):
        """Verify Niamh's response against databases, LLM logic, and web sources."""
        logging.info(f"FactChecker analyzing: {user_input}")

        # 1️⃣ Retrieve stored knowledge (MongoDB & Redis)
        stored_knowledge = self.db.fetch_knowledge(user_input)
        stored_content = stored_knowledge.get("content", "") if stored_knowledge else "No stored knowledge found."

        # 2️⃣ Fetch latest real-time data from trusted web sources
        web_data = self.tools.search_google(user_input)
        web_content = web_data if web_data else "No web search results found."

        # 3️⃣ Construct LLM verification prompt
        verification_prompt = f"""
        Task: You are an AI fact-checking agent. Your goal is to verify the accuracy of an AI assistant's response.

        **User Question:** {user_input}
        **AI Response:** {ai_response}

        **Verified Knowledge (if available):** {stored_content}
        **Web Search Data (if available):** {web_content}

        **Evaluation Criteria:**
        1️⃣ **Is the AI’s response factually correct?** Respond with "Yes" or "No".
        2️⃣ **If incorrect, provide the most accurate response.**
        3️⃣ **Summarize the contradiction in 1 sentence.**
        4️⃣ **Cite a source (LLM reasoning, database, or web source).**
        """

        # 4️⃣ Send verification request to LLM
        logging.info("🔍 LLM Fact-Checking AI Response...")
        llm_validation = self.llm.generate_response(verification_prompt)

        # **Debugging: Print LLM Output**
        print(f"🧠 LLM Fact-Check Raw Output:\n{llm_validation}\n")

        # **5️⃣ Extract Key Information Safely**
        is_correct = None
        summary = None
        corrected_response = None
        source = None

        # Ensure the format is robust and adapts to slight variations in output
        for line in llm_validation.split("\n"):
            if "Is the AI’s response factually correct?" in line:
                if "No" in line:
                    is_correct = False
                elif "Yes" in line:
                    is_correct = True
            elif "Most accurate response:" in line or "If incorrect, provide the most accurate response:" in line:
                corrected_response = line.split(":")[-1].strip()
            elif "Contradiction summary:" in line or "Summarize the contradiction in 1 sentence:" in line:
                summary = line.split(":")[-1].strip()
            elif "Cite a source:" in line:
                source = line.split(":")[-1].strip()

        # ✅ **If Correct, Return None**
        if is_correct is True:
            logging.info("✅ LLM confirms AI response is correct.")
            return None  # No contradiction

        # ❌ **If Incorrect, Return Correction Data**
        if is_correct is False and corrected_response:
            logging.warning(f"❌ Fact-Checker found an issue: {summary}")
            return {
                "summary": summary if summary else "No detailed summary provided.",
                "corrected_response": corrected_response if corrected_response else "No correction provided.",
                "source": source if source else "No source provided."
            }  # ❌ Return structured contradiction details

        return None  # No contradictions found (fallback)
