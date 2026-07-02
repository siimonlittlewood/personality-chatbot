import pandas as pd
import re

def fix_encoding(text):
    try: 
        return text.encode("latin-1").decode("utf-8")
    except:
        return text



def clean_text(text):
    if not isinstance(text, str):
        return None
    
    text = fix_encoding(text)

    text = re.sub(r"http\S+", "", text).strip()
    text = re.sub(r"\s+", " ", text).strip()
    tetx = re.sub(r"^/ | /$|/ /", " ", text).strip()

    return text if text else None

df = pd.read_csv("instagram_pairs.csv")

df["context"] = df["context"].apply(clean_text)
df["response"] = df["response"].apply(clean_text)

df = df.dropna(subset = ["context", "response"])

df.to_csv("instagram_pairs_clean.csv", index = False)