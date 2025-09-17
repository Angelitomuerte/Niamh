from niamh import NiamhAI

# Initialize Niamh
niamh = NiamhAI()

# Test session ID
session_id = "test_user_001"

print("\nUser: What is AI?")
response1 = niamh.generate_response(session_id, "What is AI?")
print("Niamh:", response1)

print("\nUser: Explain Quantum Computing")
response2 = niamh.generate_response(session_id, "Explain Quantum Computing")
print("Niamh:", response2)

print("\nUser: Can you continue our discussion?")
response3 = niamh.generate_response(session_id, "Can you continue our discussion?")
print("Niamh:", response3)

print("\nUser: How do I train a neural network?")
response4 = niamh.generate_response(session_id, "How do I train a neural network?")
print("Niamh:", response4)

