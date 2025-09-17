from core.database import DatabaseManager
from datetime import datetime

db = DatabaseManager()

db.knowledge_collection.insert_one({
    "topic": "What is the capital of France?",
    "content": "The capital of France is Paris.",
    "verified_sources": ["https://en.wikipedia.org/wiki/Paris"],
    "last_verified": datetime.utcnow()
})

print("✅ Knowledge added successfully.")
