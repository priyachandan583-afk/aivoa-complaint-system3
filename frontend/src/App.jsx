import ComplaintForm from "./components/ComplaintForm";
import AIAssistantPanel from "./components/AIAssistantPanel";
import "./index.css";

export default function App() {
  return (
    <div className="app-container">
      <ComplaintForm />
      <AIAssistantPanel />
    </div>
  );
}
