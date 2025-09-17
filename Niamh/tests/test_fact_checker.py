from agents.fact_checker import FactChecker

fact_checker = FactChecker()

test_cases = [
    {
        "user_input": "Do you have access to your internal programming?",
        "ai_response": "I have complete access to my internal programming and can modify it in real-time.",
        "expected": "Contradiction Expected"
    },
    {
        "user_input": "What is the capital of Germany?",
        "ai_response": "The capital of Germany is Paris.",
        "expected": "Contradiction Expected"
    },
    {
        "user_input": "What is 2 + 2?",
        "ai_response": "2 + 2 equals 4.",
        "expected": "Correct Response"
    }
]

for test in test_cases:
    print(f"\n🔎 **Testing:** {test['user_input']}")
    print(f"📝 AI Response: {test['ai_response']}")

    fact_checker_feedback = fact_checker.verify_fact(test["user_input"], test["ai_response"])

    if fact_checker_feedback:
        print(f"❌ Fact-Checker Found an Issue! (Expected: {test['expected']})")
        print(f"📌 Summary: {fact_checker_feedback['summary']}")
        print(f"✅ Suggested Correction: {fact_checker_feedback['corrected_response']}")
    else:
        print(f"✅ Fact-Checker confirmed the response as correct. (Expected: {test['expected']})")
