import { useRef, useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { populateFromExtraction } from "../store/complaintSlice";
import {
  startExtraction,
  setExtractionProgress,
  finishExtraction,
  addChatMessage,
} from "../store/assistantSlice";
import { extractFromFile, extractFromText, sendChatMessage } from "../api/complaintsApi";

export default function AIAssistantPanel() {
  const dispatch = useDispatch();
  const { extractionProgress, isExtracting, chatMessages } = useSelector(
    (s) => s.assistant
  );
  const { savedId } = useSelector((s) => s.complaint);
  const [pastedText, setPastedText] = useState("");
  const [chatInput, setChatInput] = useState("");
  const fileInputRef = useRef(null);

  const runExtraction = async (fn) => {
    dispatch(startExtraction());
    // Fake incremental progress while the request is in flight
    const interval = setInterval(() => {
      dispatch(setExtractionProgress(Math.min(90, extractionProgress + 15)));
    }, 400);
    try {
      const result = await fn();
      dispatch(populateFromExtraction(result));
      dispatch(
        addChatMessage({
          role: "assistant",
          text: `Extraction complete. ${
            result.missing_fields?.length
              ? `Missing: ${result.missing_fields.join(", ")}.`
              : "All key fields were found."
          }`,
        })
      );
    } catch (err) {
      dispatch(
        addChatMessage({
          role: "assistant",
          text: `Extraction failed: ${err.message}`,
        })
      );
    } finally {
      clearInterval(interval);
      dispatch(finishExtraction());
    }
  };

  const handleFileUpload = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;
    runExtraction(() => extractFromFile(file));
  };

  const handlePasteSubmit = () => {
    if (!pastedText.trim()) return;
    runExtraction(() => extractFromText(pastedText));
  };

  const handleChatSend = async () => {
    if (!chatInput.trim()) return;
    const userMsg = { role: "user", text: chatInput };
    dispatch(addChatMessage(userMsg));
    setChatInput("");
    const { reply } = await sendChatMessage(userMsg.text, savedId);
    dispatch(addChatMessage({ role: "assistant", text: reply }));
  };

  return (
    <div className="panel assistant-panel">
      <div className="panel-header">
        <h2>✨ AI Complaint Intake Assistant</h2>
        <span className="badge beta">BETA</span>
      </div>

      <div
        className="dropzone"
        onClick={() => fileInputRef.current?.click()}
        onDragOver={(e) => e.preventDefault()}
        onDrop={(e) => {
          e.preventDefault();
          const file = e.dataTransfer.files?.[0];
          if (file) runExtraction(() => extractFromFile(file));
        }}
      >
        ⬆️ Drag &amp; drop complaint document here
        <br />
        <span className="link">or click to browse</span>
        <input
          type="file"
          ref={fileInputRef}
          hidden
          accept=".pdf,.docx,.txt,.eml"
          onChange={handleFileUpload}
        />
      </div>

      <div className="or-divider">OR</div>

      <textarea
        className="paste-box"
        placeholder="Paste Complaint Text / Email"
        value={pastedText}
        onChange={(e) => setPastedText(e.target.value)}
      />
      <button className="btn-secondary" onClick={handlePasteSubmit}>
        Extract from Text
      </button>

      <p className="hint">Supported formats: PDF, DOCX, TXT, EML. Max size: 10MB</p>

      {isExtracting && (
        <div className="progress-section">
          <div className="progress-label">EXTRACTION PROGRESS</div>
          <div className="progress-bar">
            <div
              className="progress-fill"
              style={{ width: `${extractionProgress}%` }}
            />
          </div>
          <p className="hint">Analyzing document content and extracting key details...</p>
        </div>
      )}

      <div className="chat-section">
        <div className="progress-label">AI ASSISTANT</div>
        <div className="chat-log">
          {chatMessages.map((m, i) => (
            <div key={i} className={`chat-bubble ${m.role}`}>
              {m.text}
            </div>
          ))}
        </div>
        <div className="chat-input-row">
          <input
            type="text"
            placeholder="Ask me anything about this complaint..."
            value={chatInput}
            onChange={(e) => setChatInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleChatSend()}
          />
          <button onClick={handleChatSend}>➤</button>
        </div>
        <p className="hint">AI responses may contain errors. Please verify information.</p>
      </div>
    </div>
  );
}
