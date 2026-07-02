# AI Simon — Personal Texting Style Chatbot

A fine-tuned language model that replicates my personal texting style, trained on 8,500+ of my own Instagram messages. The bot responds the way I would — same vocabulary, same energy, same patterns — served through an SMS-style chat interface.

## How It Works

**Data Pipeline**
Raw Instagram message exports (JSON) are parsed, cleaned, and formatted into context-response training pairs. Each pair captures a full conversational turn — including multi-message bursts — with up to 3 turns of preceding context. A time-gap filter ensures context windows don't bleed across separate conversations.

**Fine-Tuning**
Mistral 7B Instruct is fine-tuned using LoRA (Low-Rank Adaptation) via Hugging Face PEFT, training only ~6.8M of the model's 7B parameters (0.1%). Training used the instruction-tuning format with the first 4,000 examples from the cleaned dataset.

**Evaluation**
Perplexity was computed on a held-out set of 750 examples (the final 750 rows, never seen during training). The fine-tuned model achieved over 95% lower perplexity compared to the base Mistral model on this personal texting data, reflecting a substantially improved fit to my specific writing style and slang.

**Inference & Deployment**
A FastAPI backend loads the fine-tuned model with 4-bit quantization (BitsAndBytes) and serves responses via a GPU session on Kaggle, exposed through an ngrok tunnel. The React frontend is deployed on Vercel and maintains full conversation history, passing it to the backend with each request for contextually aware multi-turn responses.

## Stack

| Layer | Tools |
|---|---|
| Fine-tuning | Hugging Face Transformers, PEFT, TRL, BitsAndBytes |
| Base model | Mistral 7B Instruct v0.2 |
| Backend | FastAPI, uvicorn, PyTorch |
| Frontend | React, Vite |
| Deployment | Kaggle (GPU inference), Vercel (frontend), ngrok (tunnel) |
| Model storage | Hugging Face Hub |
| Data processing | Python, pandas |

## Project Structure

```
├── parsing.py           # Extract and group Instagram messages into turns
├── cleaning.py          # Clean and filter raw message data  
├── prepare_finetune.py  # Format data into instruction-tuning pairs
├── backend.py           # FastAPI inference server
├── frontend_files/      # React chat interface
│   ├── src/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── index.html
│   └── package.json
└── README.md
```

## Running Locally

**Backend** (requires Kaggle or GPU environment):
```bash
pip install fastapi uvicorn transformers accelerate bitsandbytes pyngrok
uvicorn backend:app --reload
```

**Frontend**:
```bash
cd frontend_files
npm install
npm run dev
```

Set `VITE_BACKEND_URL` in a `.env` file to point to your backend URL.

## Key Design Decisions

- **LoRA over full fine-tuning** — makes training feasible on a single consumer GPU by only updating a small fraction of parameters
- **Turn-based context grouping** — consecutive messages from the same person are merged into a single "turn" before building training pairs, matching how conversations actually flow
- **Time-gap filtering** — context windows are cut if there's more than a 2-hour gap between messages, preventing the model from learning false adjacency across separate conversation threads
- **Merged weights on Hugging Face Hub** — LoRA adapters are merged into the base model before upload, simplifying inference without needing PEFT at runtime
