import React from "react";

const COLORS = {
  admin: "#27b36a",
  viewer: "#2a7fd3",
  auditor: "#b77fd3",
  maintainer: "#e6b800",
  disabled: "#bbb",
};

export default function Phase9RoleBadge({ role }) {
  return (
    <span
      style={{
        background: COLORS[role] || COLORS.disabled,
        color: "#fff",
        borderRadius: 8,
        padding: "2px 8px",
        marginLeft: 6,
        fontSize: 12,
        fontWeight: 500,
        textTransform: "capitalize",
      }}
    >
      {role}
    </span>
  );
}
