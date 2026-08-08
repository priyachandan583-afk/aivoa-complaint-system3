import { useDispatch, useSelector } from "react-redux";
import { setField, resetForm, setSavedId } from "../store/complaintSlice";
import { saveComplaint } from "../api/complaintsApi";

const FIELD_GROUPS = [
  {
    title: "1. Origin & Customer Details",
    fields: [
      { name: "complaint_source", label: "Complaint Source" },
      { name: "customer_name", label: "Customer Name" },
    ],
  },
  {
    title: "2. Product & Batch Identification",
    fields: [
      { name: "product_name", label: "Product Name" },
      { name: "product_strength_grade", label: "Product Strength/Grade" },
      { name: "batch_lot_number", label: "Batch/Lot Number" },
      { name: "manufacturing_date", label: "Manufacturing Date", type: "date" },
      { name: "expiry_date", label: "Expiry Date", type: "date" },
      { name: "quantity_affected", label: "Quantity Affected", type: "number" },
    ],
  },
  {
    title: "3. Complaint Details",
    fields: [
      { name: "complaint_type", label: "Complaint Type" },
      { name: "complaint_date", label: "Complaint Date", type: "date" },
      {
        name: "detailed_description",
        label: "Detailed Complaint Description",
        type: "textarea",
      },
    ],
  },
  {
    title: "4. Initial Assessment & Priority",
    fields: [
      {
        name: "initial_severity",
        label: "Initial Severity",
        type: "select",
        options: ["Low", "Medium", "High", "Critical"],
      },
      {
        name: "priority",
        label: "Priority",
        type: "select",
        options: ["Low", "Medium", "High", "Urgent"],
      },
    ],
  },
];

export default function ComplaintForm() {
  const dispatch = useDispatch();
  const { fields, status, missingFields } = useSelector((s) => s.complaint);

  const handleChange = (name, value) => {
    dispatch(setField({ name, value }));
  };

  const handleSave = async () => {
    const saved = await saveComplaint(fields);
    dispatch(setSavedId(saved.id));
  };

  return (
    <div className="panel form-panel">
      <div className="panel-header">
        <div>
          <h2>Log Customer Complaint</h2>
          <p className="subtitle">API &amp; FDF Quality Assurance Module</p>
        </div>
        <span className="badge">{status}</span>
      </div>

      {FIELD_GROUPS.map((group) => (
        <fieldset key={group.title}>
          <legend>{group.title}</legend>
          <div className="field-grid">
            {group.fields.map((f) => (
              <div
                key={f.name}
                className={f.type === "textarea" ? "field span-2" : "field"}
              >
                <label>{f.label}</label>
                {f.type === "textarea" ? (
                  <textarea
                    value={fields[f.name] || ""}
                    onChange={(e) => handleChange(f.name, e.target.value)}
                    placeholder="Awaiting AI extraction..."
                  />
                ) : f.type === "select" ? (
                  <select
                    value={fields[f.name] || ""}
                    onChange={(e) => handleChange(f.name, e.target.value)}
                  >
                    <option value="">Awaiting AI extraction...</option>
                    {f.options.map((opt) => (
                      <option key={opt} value={opt}>
                        {opt}
                      </option>
                    ))}
                  </select>
                ) : (
                  <input
                    type={f.type || "text"}
                    value={fields[f.name] || ""}
                    onChange={(e) => handleChange(f.name, e.target.value)}
                    placeholder="Awaiting AI extraction..."
                  />
                )}
                {missingFields.includes(f.name) && (
                  <span className="missing-flag">Missing — needs follow-up</span>
                )}
              </div>
            ))}
          </div>
        </fieldset>
      ))}

      <div className="form-actions">
        <button className="btn-secondary" onClick={() => dispatch(resetForm())}>
          Reset Form
        </button>
        <button className="btn-primary" onClick={handleSave}>
          Save Complaint
        </button>
      </div>
    </div>
  );
}
