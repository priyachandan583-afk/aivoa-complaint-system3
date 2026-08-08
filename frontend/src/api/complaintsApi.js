import axios from "axios";

const api = axios.create({ baseURL: "/api" });

export async function extractFromFile(file) {
  const formData = new FormData();
  formData.append("file", file);
  const { data } = await api.post("/complaints/extract", formData);
  return data;
}

export async function extractFromText(text) {
  const formData = new FormData();
  formData.append("text", text);
  const { data } = await api.post("/complaints/extract", formData);
  return data;
}

export async function saveComplaint(fields) {
  const { data } = await api.post("/complaints", fields);
  return data;
}

export async function sendChatMessage(message, complaintId) {
  const { data } = await api.post("/complaints/chat", {
    message,
    complaint_id: complaintId,
  });
  return data;
}
