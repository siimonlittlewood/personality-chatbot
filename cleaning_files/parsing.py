import json
import pandas as pd
from pathlib import Path

my_name = "Simon"
inbox_path = Path(r"C:\Users\simon\OneDrive\Desktop\simon chatbot\instagram-siimonjay-2026-05-12-iYzDFOH1\your_instagram_activity\messages\inbox")

def grouping_into_turns(messages):
    """Groups messages into turns of whos speaking"""

    turns = []
    current_sender = None
    current_texts = []
    current_time = None

    for msg in messages:
        if "content" not in msg:
            continue

        sender = msg["sender_name"]
        time = msg["timestamp_ms"]
        text = msg["content"]

        if sender == current_sender:
            current_texts.append(text)

        else:
            if current_texts:
                turns.append({
                    "sender": current_sender,
                    "timestamp": current_time,
                    "messages": current_texts
                })
            current_sender = sender
            current_time = time
            current_texts = [text]
    
    if current_texts:
        turns.append({
            "sender": current_sender,
            "timestamp": current_time,
            "messages": current_texts
        })

    return turns

all_pairs = []

for convo_dir in inbox_path.iterdir():
    # for each conversation
    all_msgs = []

    for json_file in sorted(convo_dir.glob("message_*.json")):
        # for each json file in the conversation - sometimes multiple
        with open(json_file, "r", encoding = "utf-8") as f:
            data = json.load(f)
        all_msgs.extend(data["messages"])

    all_msgs = list(reversed(all_msgs))
    turns = grouping_into_turns(all_msgs)

    for i, turn in enumerate(turns):
        if turn["sender"] == my_name and i > 0:
        # we only grab my turns, but get others messages as context along the way
            context_turns = turns[max(0, i - 3):i]
            # grabbing as many turns as we can before the current one for context
            # usually 3

            context = "\n".join([
                f"{t['sender']}: {' / '.join(t['messages'])}" for t in context_turns
            ])

            # formatting into readable text we can examine

            response = " / ".join(turn["messages"])

            all_pairs.append({
                "context": context,
                "response": response,
                "conversation": convo_dir.name
            })

df = pd.DataFrame(all_pairs)
print(f"Total training pairs: {len(df)}")
print(df.head(3))
df.to_csv("instagram_pairs.csv", index = False)