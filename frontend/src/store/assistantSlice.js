import { createSlice } from "@reduxjs/toolkit";

const assistantSlice = createSlice({
  name: "assistant",
  initialState: {
    extractionProgress: 0,
    isExtracting: false,
    chatMessages: [
      {
        role: "assistant",
        text: "Upload a complaint document or paste text above. I will automatically extract the details and populate the form for you.",
      },
    ],
  },
  reducers: {
    startExtraction(state) {
      state.isExtracting = true;
      state.extractionProgress = 10;
    },
    setExtractionProgress(state, action) {
      state.extractionProgress = action.payload;
    },
    finishExtraction(state) {
      state.isExtracting = false;
      state.extractionProgress = 100;
    },
    addChatMessage(state, action) {
      state.chatMessages.push(action.payload);
    },
  },
});

export const {
  startExtraction,
  setExtractionProgress,
  finishExtraction,
  addChatMessage,
} = assistantSlice.actions;
export default assistantSlice.reducer;
