import { useState } from "react";
import { Send } from "lucide-react";
import "bootstrap/dist/css/bootstrap.min.css";

export default function ChatUI() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleSend = async () => {
    if (!input.trim()) return;
    const newMessages = [...messages, { role: "user", text: input }];
    setMessages(newMessages);
    setInput("");
    
    try {
      const response = await fetch("https://api.example.com/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: input })
      });
      const data = await response.json();
      setMessages([...newMessages, { role: "gpt", text: data.reply }]);
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };

  return (
    <div className="container mt-4">
       <h3 className="text-center mb-3">
          <i className="bi bi-robot text-primary"></i>Train Robot Command
        </h3>
      <div className="card shadow" style={{ height: "400px", overflowY: "auto" }}>
        <div className="card-body">
          {messages.map((msg, index) => (
            <div key={index} className={`mb-2 p-2 rounded ${msg.role === "user" ? "bg-primary text-white text-end" : "bg-light text-start"}`}>
              {msg.text}
            </div>
          ))}
        </div>
      </div>
      <div className="input-group mt-3">
        <input
          type="text"
          className="form-control"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message..."
        />
        <button className="btn btn-primary" onClick={handleSend}>
          <Send size={16} /> Send
        </button>
      </div>
    </div>
  );
}
