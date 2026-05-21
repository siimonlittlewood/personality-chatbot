import pandas as pd
import json

df = pd.read_csv("instagram_pairs_clean.csv")

# print("---ORIGINAL--- \n")
# print(df["context"].iloc[:3])
# print("---AFTER ANONIMIZE--- \n")

def anonymize_context(context, your_name = "Simon"):
    words = context.split()
    cleaned = []
    for word in words:
        if word.endswith(":") and word != your_name + ":":
            cleaned.append("Them:")
        else:
            cleaned.append(word)
    
    return " ".join(cleaned)

df["context"] = df["context"].apply(anonymize_context)

# print(df["context"].iloc[:3])

formatted = []

for _, row in df.iterrows():
    # _ is the index because iterrows returns index and actual rows,
    # but we don't need the index in this situation
    
    formatted.append({
        "instruction": "Respond to this conversation as Simon would, match his texting style, tone and vocabulary exactly.",
        "input": row["context"],
        "output": row["response"]
    })

with open("fintune_data.jsonl", "w", encoding = "utf-8") as f:
    for item in formatted:
        f.write(json.dumps(item) + "\n")

# saves formatted as a jsonl, so one json object per line

# preview

for item in formatted[:3]:
    print("\n---")
    print(f"INPUT: {item['input']}")
    print(f"OUPUT: {item['output']}")