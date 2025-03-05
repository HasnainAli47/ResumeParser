import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { toast } from "react-toastify";
import { api } from "../api/api";
import ReactMarkdown from "react-markdown";

const Chatbot = () => {
  const [messages, setMessages] = useState([
    { text: "Hello! Select a candidate and ask your question.", sender: "bot", isInitial: true }
  ]);
  const [candidates, setCandidates] = useState([]);
  const [selectedCandidate, setSelectedCandidate] = useState(null);
  const [query, setQuery] = useState("");

  useEffect(() => {
    api
      .get("/candidates/")
      .then((response) => setCandidates(response.data))
      .catch((error) => console.error("Error fetching candidates:", error));
  }, []);

  const sendMessage = async () => {
    if (!selectedCandidate) {
      toast.error("Please select a candidate.");
      return;
    }
    if (!query.trim()) {
      toast.error("Please enter a question.");
      return;
    }

    setMessages((prevMessages) =>
      prevMessages.filter((msg) => !msg.isInitial).concat({ text: query, sender: "user" })
    );
    setQuery("");

    try {
      const response = await api.post("/query/", {
        resume_id: selectedCandidate,
        query,
      });

      const botResponse = response.data.responses[query] || "No response from AI.";

      setMessages((prevMessages) => [
        ...prevMessages,
        { text: botResponse, sender: "bot" },
      ]);
    } catch (error) {
      console.error("Error querying AI:", error);
      toast.error("Error processing query.");
    }
  };

  return (
    <div className="h-screen bg-gray-100 flex flex-col items-center justify-center p-4">
      <motion.div
        className="bg-white p-6 shadow-lg rounded-lg w-full max-w-lg"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        {/* Candidate Selection */}
        <select
          className="mb-4 w-full p-2 border border-gray-300 rounded"
          onChange={(e) => setSelectedCandidate(e.target.value)}
        >
          <option value="">Select a Candidate</option>
          {candidates.map((candidate) => (
            <option key={candidate.id} value={candidate.id}>
              {candidate.name}
            </option>
          ))}
        </select>

        {/* Chat Window */}
        <div className="h-64 overflow-y-auto border p-2 rounded bg-gray-50">
          {messages.map((msg, index) => (
            <motion.div
              key={index}
              className={`p-2 my-1 rounded-lg w-fit max-w-xs ${
                msg.sender === "bot"
                  ? "bg-blue-100 text-blue-800 self-start"
                  : "bg-green-100 text-green-800 self-end"
              }`}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
            >
              <ReactMarkdown>{msg.text}</ReactMarkdown>
            </motion.div>
          ))}
        </div>

        {/* Input Box */}
        <div className="flex mt-4 space-x-2">
          <input
            type="text"
            className="flex-1 p-2 border border-gray-300 rounded"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask a question..."
            disabled={!selectedCandidate}
          />
          <button
            onClick={sendMessage}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg"
            disabled={!selectedCandidate}
          >
            Ask AI
          </button>
        </div>
      </motion.div>
    </div>
  );
};

export default Chatbot;
