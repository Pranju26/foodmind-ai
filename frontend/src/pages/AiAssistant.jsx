import { useState, useRef, useEffect } from "react";
import AppShell from "../components/AppShell";
import { apiPost } from "../api/client";
import "./AiAssistant.css";

const SUGGESTIONS = [
  "What should I eat for dinner?",
  "How can I increase my protein intake?",
  "Suggest a healthy breakfast under 500 calories.",
  "What should I eat after a workout?",
];

function AiAssistant() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function sendMessage(text) {
    const trimmed = text.trim();
    if (!trimmed) return;

    setMessages((prev) => [...prev, { role: "user", text: trimmed }]);
    setInput("");
    setLoading(true);
    setError("");

    try {
      const data = await apiPost("/ai/chat", { message: trimmed });
      setMessages((prev) => [...prev, { role: "assistant", text: data.reply }]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  function handleSubmit(e) {
    e.preventDefault();
    sendMessage(input);
  }

  return (
    <AppShell title="AI Assistant" subtitle="Your personal nutrition assistant, powered by FoodMind AI.">
      <div className="chat-container">
        <div className="chat-messages">
          {messages.length === 0 && (
            <div className="chat-empty">
              <p className="chat-empty-title">What would you like to know?</p>
              <div className="chat-suggestions">
                {SUGGESTIONS.map((s, idx) => (
                  <button key={idx} onClick={() => sendMessage(s)}>
                    {s}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((m, idx) => (
            <div key={idx} className={`chat-bubble-row ${m.role === "user" ? "row-user" : "row-assistant"}`}>
              <div className={`chat-bubble ${m.role === "user" ? "bubble-user" : "bubble-assistant"}`}>
                {m.text}
              </div>
            </div>
          ))}

          {loading && (
            <div className="chat-bubble-row row-assistant">
              <div className="chat-bubble bubble-assistant chat-typing">
                <span></span><span></span><span></span>
              </div>
            </div>
          )}

          {error && <p className="chat-error">{error}</p>}

          <div ref={bottomRef}></div>
        </div>

        <form className="chat-input-row" onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Ask about my nutrition..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
          <button type="submit" disabled={loading || !input.trim()}>
            Send
          </button>
        </form>
      </div>
    </AppShell>
  );
}

export default AiAssistant;
