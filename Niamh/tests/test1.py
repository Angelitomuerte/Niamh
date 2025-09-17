from database import DatabaseManager

# Initialize the database manager
db = DatabaseManager()

# Test: Store a conversation entry in MongoDB
session_id = "session_123"
user_input = "What is AI"
ai_response = "AI stands for Artificial Intelligence, which is the simulation of human intelligence by machines."

db.store_conversation(session_id, user_input, ai_response)
print("Conversation stored successfully.")

# Test: Retrieve conversation history from Redis or MongoDB
history = db.fetch_conversation_history(session_id, limit=5)
print("\nConversation History Retrieved:")
for entry in history:
    print(entry)

# Test: Store a knowledge entry in MongoDB
topic = "Quantum Computing"
content = "Quantum computing uses qubits that leverage superposition and entanglement."
sources = ["https://quantum-computing.ibm.com", "https://arxiv.org/abs/2201.12345"]

db.knowledge_collection.insert_one({
    "topic": topic,
    "content": content,
    "verified_sources": sources,
    "last_verified": "2025-02-20"
})
print("\nKnowledge entry stored successfully.")

# Test: Retrieve the knowledge entry
knowledge = db.fetch_knowledge(topic)
print("\nKnowledge Retrieved:")
print(knowledge)

# Test: Trigger Redis to MongoDB Migration
db.migrate_stale_data_to_mongo()
print("\nData Migration Complete.")

print("\nAll tests completed successfully.")
