import { createSlice } from "@reduxjs/toolkit";

const initialFields = {
  complaint_source: "",
  customer_name: "",
  product_name: "",
  product_strength_grade: "",
  batch_lot_number: "",
  manufacturing_date: "",
  expiry_date: "",
  quantity_affected: "",
  quantity_unit: "kg",
  complaint_type: "",
  complaint_date: "",
  detailed_description: "",
  initial_severity: "",
  priority: "",
};

const complaintSlice = createSlice({
  name: "complaint",
  initialState: {
    fields: initialFields,
    status: "Pending Triage",
    savedId: null,
    missingFields: [],
    riskNotes: "",
  },
  reducers: {
    setField(state, action) {
      const { name, value } = action.payload;
      state.fields[name] = value;
    },
    populateFromExtraction(state, action) {
      const { fields, missing_fields, risk_notes, initial_severity, priority } =
        action.payload;
      state.fields = { ...state.fields, ...fields };
      if (initial_severity) state.fields.initial_severity = initial_severity;
      if (priority) state.fields.priority = priority;
      state.missingFields = missing_fields || [];
      state.riskNotes = risk_notes || "";
    },
    resetForm(state) {
      state.fields = initialFields;
      state.missingFields = [];
      state.riskNotes = "";
      state.savedId = null;
    },
    setSavedId(state, action) {
      state.savedId = action.payload;
      state.status = "Saved";
    },
  },
});

export const { setField, populateFromExtraction, resetForm, setSavedId } =
  complaintSlice.actions;
export default complaintSlice.reducer;
