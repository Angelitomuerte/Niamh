import pymongo
import redis
import json
import time
from datetime import datetime

class DatabaseManager:
    def __init__(self, mongo_uri="mongodb://127.0.0.1:27017", redis_host="localhost", redis_port=6379, redis_threshold=70):
        """Initialize MongoDB and Redis connections"""
        self.mongo_client = pymongo.MongoClient(mongo_uri)
        self.db = self.mongo_client["Niamh_AI_Database"]  # Updated database name

        # Collections in MongoDB
        self.conversation_collection = self.db["conversations"]
        self.knowledge_collection = self.db["knowledge_base"]

        # Redis setup
        self.redis_client = redis.StrictRedis(host=redis_host, port=redis_port, db=0, decode_responses=True)
        
        # Cache storage threshold (percentage before migration)
        self.redis_threshold = redis_threshold

    def cache_data(self, key, value, expiry=300):
        """Stores data in Redis cache"""
        self.redis_client.setex(key, expiry, json.dumps(value))

    def get_cached_data(self, key):
        """Retrieves cached data from Redis"""
        data = self.redis_client.get(key)
        return json.loads(data) if data else None

    def remove_cache(self, key):
        """Removes data from Redis cache"""
        self.redis_client.delete(key)

    def fetch_conversation_history(self, session_id, limit=10):
        """Checks Redis first, then MongoDB for past conversation history"""
        cache_key = f"conversation_{session_id}"
        cached_data = self.get_cached_data(cache_key)

        if cached_data:
            return cached_data  

        # If not found in Redis, query MongoDB
        history = list(self.conversation_collection.find({"session_id": session_id}).sort("timestamp", -1).limit(limit))

        if history:
            formatted_history = [{"user_input": h["user_input"], "ai_response": h["ai_response"], "timestamp": str(h["timestamp"])} for h in history]
            self.cache_data(cache_key, formatted_history, expiry=300)
            return formatted_history

        return []

    def store_conversation(self, session_id, user_input, ai_response):
        """Stores conversation history in MongoDB"""
        conversation_entry = {
            "session_id": session_id,
            "user_input": user_input,
            "ai_response": ai_response,
            "timestamp": datetime.utcnow()
        }
        self.conversation_collection.insert_one(conversation_entry)

    def fetch_knowledge(self, topic):
        """Checks Redis first, then MongoDB for knowledge base queries"""
        cache_key = f"knowledge_{topic}"
        cached_data = self.get_cached_data(cache_key)

        if cached_data:
            return cached_data  

        # If not cached, fetch from MongoDB
        knowledge_entry = self.knowledge_collection.find_one({"topic": topic})
        if knowledge_entry:
            formatted_entry = {
                "topic": knowledge_entry["topic"],
                "content": knowledge_entry["content"],
                "verified_sources": knowledge_entry["verified_sources"],
                "last_verified": str(knowledge_entry["last_verified"])
            }
            self.cache_data(cache_key, formatted_entry, expiry=600)
            return formatted_entry

        return None

    def check_redis_memory(self):
        """Checks Redis memory usage percentage"""
        used_memory = int(self.redis_client.info("memory")["used_memory"])
        max_memory = int(self.redis_client.info("memory").get("maxmemory", 0))
        if max_memory > 0:
            usage_percent = (used_memory / max_memory) * 100
            return usage_percent
        return 0

    def migrate_stale_data_to_mongo(self):
        """Moves stale or old data from Redis to MongoDB"""
        redis_usage = self.check_redis_memory()
        if redis_usage >= self.redis_threshold:
            print(f"Redis memory usage is at {redis_usage:.2f}%. Initiating migration to MongoDB.")

        keys = self.redis_client.keys("*")  
        for key in keys:
            data = self.get_cached_data(key)
            if data:
                if "session_id" in data:
                    self.store_conversation(data["session_id"], data["user_input"], data["ai_response"])
                
                self.remove_cache(key)
                print(f"Moved {key} from Redis to MongoDB")

    def scheduled_migration(self, interval=600):
        """Runs a migration job every X seconds (default: 10 minutes)"""
        while True:
            self.migrate_stale_data_to_mongo()
            time.sleep(interval)
