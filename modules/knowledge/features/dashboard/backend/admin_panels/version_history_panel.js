// Version History Panel Stub
// Displays policy version history from policy_version_log.json
// Integrate this into your React admin dashboard.

export default function VersionHistoryPanel() {
  // Static, SAFE AI-compliant version history. Extension: integrate with backend API/file in future.
  const staticVersionHistory = [
    {
      version: "1.0",
      date: "2024-01-01",
      notes: "Initial SAFE AI policy release.",
    },
    {
      version: "1.1",
      date: "2024-03-15",
      notes: "Added audit log requirements.",
    },
    {
      version: "1.2",
      date: "2024-06-10",
      notes: "Updated compliance checklist.",
    },
  ];
  return (
    <div>
      <h2>Policy Version History</h2>
      <table>
        <thead>
          <tr>
            <th>Version</th>
            <th>Date</th>
            <th>Notes</th>
          </tr>
        </thead>
        <tbody>
          {staticVersionHistory.map((row, idx) => (
            <tr key={idx}>
              <td>{row.version}</td>
              <td>{row.date}</td>
              <td>{row.notes}</td>
            </tr>
          ))}
        </tbody>
      </table>
      {/* Extension: Replace with backend API or static file fetch in future */}
    </div>
  );
}
