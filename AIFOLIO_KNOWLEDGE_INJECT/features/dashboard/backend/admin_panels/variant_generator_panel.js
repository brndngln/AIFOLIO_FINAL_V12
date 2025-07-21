// Auto-Variant Generator Panel
// Displays output variants for admin approval
import React, { useEffect, useState } from "react";
export default function VariantGeneratorPanel() {
  const [variants, setVariants] = useState([]);
  useEffect(() => {
    fetch("/api/variant_generator_log")
      .then((res) => res.json())
      .then(setVariants);
  }, []);
  return (
    <div>
      <h2>Auto-Variant Generator Log</h2>
      <ul>
        {variants.map((v, i) => (
          <li key={i}>{v}</li>
        ))}
      </ul>
    </div>
  );
}
