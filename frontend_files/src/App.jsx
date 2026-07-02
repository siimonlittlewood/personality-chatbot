import { useState, useRef, useEffect } from "react";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "http://localhost:8000";

function TypingIndicator() {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 6, padding: "10px 14px", background: "#2a2a2e", borderRadius: "18px 18px 18px 4px", width: "fit-content", maxWidth: 70 }}>
      {[0, 1, 2].map(i => (
        <div key={i} style={{
          width: 7, height: 7, borderRadius: "50%", background: "#666",
          animation: "bounce 1.2s infinite",
          animationDelay: `${i * 0.2}s`
        }} />
      ))}
    </div>
  );
}

function Message({ msg }) {
  const isUser = msg.role === "user";
  const parts = isUser ? [msg.content] : msg.content.split(" / ");

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: isUser ? "flex-end" : "flex-start", gap: 3, marginBottom: 2 }}>
      {parts.map((part, i) => (
        <div key={i} style={{
          maxWidth: "72%",
          padding: "10px 14px",
          borderRadius: isUser
            ? i === 0 && parts.length > 1 ? "18px 18px 4px 18px" : i === parts.length - 1 ? "4px 18px 18px 18px" : "4px 18px 4px 18px"
            : i === 0 && parts.length > 1 ? "18px 18px 18px 4px" : i === parts.length - 1 ? "18px 18px 4px 18px" : "18px 4px 18px 18px",
          background: isUser ? "#0a84ff" : "#2a2a2e",
          color: "#fff",
          fontSize: 15,
          lineHeight: 1.45,
          wordBreak: "break-word",
          letterSpacing: "0.01em"
        }}>
          {part.trim()}
        </div>
      ))}
    </div>
  );
}

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function send() {
    const text = input.trim();
    if (!text || loading) return;

    const userMsg = { role: "user", content: text };
    const newMessages = [...messages, userMsg];
    setMessages(newMessages);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${BACKEND_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "ngrok-skip-browser-warning": "true"
        },
        body: JSON.stringify({
          message: text,
          history: messages.map(m => ({ role: m.role, content: m.content }))
        })
      });
      const data = await res.json();
      setMessages([...newMessages, { role: "assistant", content: data.response }]);
    } catch {
      setMessages([...newMessages, { role: "assistant", content: "..." }]);
    } finally {
      setLoading(false);
      inputRef.current?.focus();
    }
  }

  function handleKey(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  }

  return (
    <>
      <style>{`
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: #000; font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif; }
        @keyframes bounce {
          0%, 60%, 100% { transform: translateY(0); }
          30% { transform: translateY(-5px); }
        }
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(6px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .msg-wrap { animation: fadeIn 0.2s ease; }
        textarea:focus { outline: none; }
        textarea { resize: none; }
        ::-webkit-scrollbar { width: 0px; }
      `}</style>

      <div style={{ height: "100dvh", display: "flex", flexDirection: "column", maxWidth: 480, margin: "0 auto", background: "#000" }}>

        {/* header */}
        <div style={{ padding: "16px 20px 12px", borderBottom: "0.5px solid #222", display: "flex", alignItems: "center", gap: 12, flexShrink: 0 }}>
          <div style={{ width: 40, height: 40, borderRadius: "50%", background: "#1c1c1e", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 17, fontWeight: 600, color: "#fff", letterSpacing: "-0.5px" }}>
            S
          </div>
          <div>
            <div style={{ fontSize: 16, fontWeight: 600, color: "#fff", letterSpacing: "-0.2px" }}>AI Simon</div>
            <div style={{ fontSize: 12, color: "#666", marginTop: 1 }}>{loading ? "typing..." : "online"}</div>
          </div>
        </div>

        {/* messages */}
        <div style={{ flex: 1, overflowY: "auto", padding: "16px 16px 8px", display: "flex", flexDirection: "column", gap: 8 }}>
          {messages.length === 0 && (
            <div style={{ flex: 1, display: "flex", alignItems: "center", justifyContent: "center" }}>
              <p style={{ color: "#444", fontSize: 14, textAlign: "center", lineHeight: 1.6 }}>
                send a message
              </p>
            </div>
          )}
          {messages.map((msg, i) => (
            <div key={i} className="msg-wrap">
              <Message msg={msg} />
            </div>
          ))}
          {loading && (
            <div className="msg-wrap">
              <TypingIndicator />
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        {/* input */}
        <div style={{ padding: "8px 12px 20px", borderTop: "0.5px solid #1a1a1a", display: "flex", alignItems: "flex-end", gap: 10, flexShrink: 0 }}>
          <textarea
            ref={inputRef}
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={handleKey}
            placeholder="iMessage"
            rows={1}
            style={{
              flex: 1,
              background: "#1c1c1e",
              border: "0.5px solid #333",
              borderRadius: 22,
              padding: "10px 16px",
              color: "#fff",
              fontSize: 15,
              fontFamily: "inherit",
              lineHeight: 1.4,
              maxHeight: 120,
              overflowY: "auto",
              caretColor: "#0a84ff"
            }}
            onInput={e => {
              e.target.style.height = "auto";
              e.target.style.height = Math.min(e.target.scrollHeight, 120) + "px";
            }}
          />
          <button
            onClick={send}
            disabled={!input.trim() || loading}
            style={{
              width: 36, height: 36, borderRadius: "50%",
              background: input.trim() && !loading ? "#0a84ff" : "#1c1c1e",
              border: "none", cursor: input.trim() && !loading ? "pointer" : "default",
              display: "flex", alignItems: "center", justifyContent: "center",
              flexShrink: 0, transition: "background 0.15s"
            }}
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
              <line x1="12" y1="19" x2="12" y2="5" />
              <polyline points="5 12 12 5 19 12" />
            </svg>
          </button>
        </div>
      </div>
    </>
  );
}