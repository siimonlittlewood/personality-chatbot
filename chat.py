import numpy as np
import pandas as pd
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import anthropic
import os

load_dotenv()

index = faiss.read_index("index.faiss")
df = pd.read_pickle("pairs.pk1")
model = SentenceTransformer("all-MiniLM-L6-v2")
client = anthropic.Anthropic(api_key = os.getenv("ANTHROPIC_API_KEY"))

def retrive_examples(message, k = 3):
    query_vector = model.encode([message])

    distances, indices = index.search(np.array(query_vector), k)

    examples = []

    for i in indices[0]:
        examples.append({
            "context": df.iloc[i]["context"],
            "response":  df.iloc[i]["response"]
        })

    return examples

def generate_response(message):
    examples = retrive_examples(message)

    example_text = ""
    for i, ex in enumerate(examples):
        example_text += f"Example {i + 1}:\nContext: {ex['context']}\nSimon's response: {ex['response']}\n\n"

        response = client.messages.create(
            model = "claude-haiku-4-5",
            max_tokens = 300,
            system = f"""
            You are a chatbot that responds exactly like Simon based on his texting style and tone.
            
            Here are real examples of how Simon texts:

            {example_text}

            Rules:
            - Match Simon's tone, vocabularu, and energy exactly
            - Keep responses around the same length as examples
            - Don't be formal or use proper punctuation unless Simon does
            - Sound like a real person texting, not an AI
            """,
            messages = [{"role": "user", "content": message}]
        )

    return response.content[0].text
    
#rudimentary test
print("Simon bot ready. Type a message:")
while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break
    response = generate_response(user_input)
    print(f"Simon: {response}\n")