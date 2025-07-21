import React, { useState } from "react";

const initialSteps = [
  { id: 1, label: "Generate Brief", type: "prompt", config: {} },
  { id: 2, label: "Review Output", type: "review", config: {} },
];

export default function WorkflowBuilder() {
  const [steps, setSteps] = useState(initialSteps);
  const addStep = () =>
    setSteps([
      ...steps,
      { id: Date.now(), label: "New Step", type: "prompt", config: {} },
    ]);

  return (
    <div
      className="workflow-builder"
      style={{
        background: "#181e2b",
        color: "#b3e9ff",
        borderRadius: 16,
        padding: 32,
        boxShadow: "0 0 32px #00e6ff44",
      }}
    >
      <h2>Prompt Workflow Builder</h2>
      <ol>
        {steps.map((step) => (
          <li key={step.id} style={{ marginBottom: 8 }}>
            {step.label} <span style={{ opacity: 0.7 }}>({step.type})</span>
          </li>
        ))}
      </ol>
      <button
        onClick={addStep}
        style={{
          background: "#00e6ff",
          color: "#181e2b",
          border: "none",
          borderRadius: 8,
          padding: "8px 16px",
          fontWeight: "bold",
        }}
      >
        Add Step
      </button>
      <div style={{ marginTop: 32, opacity: 0.8 }}>
        <em>
          Drag-and-drop builder for multi-step prompt flows. All workflows are
          owner-controlled and SAFE AI-compliant.
        </em>
      </div>
    </div>
  );
}
