// [WINDSURF FIXED ✅]
import React, { useEffect, useState } from "react";
import axios from "axios";

import PropTypes from "prop-types";

export default function UserManagementPanel({ token, enableRoles }) {
  const [users, setUsers] = useState([]);

  const [newUser, setNewUser] = useState({
    username: "",
    role: "partner",
    email: "",
    org: "",
  });

  function fetchUsers() {
    axios
      .get("/admin/users", { headers: { Authorization: `Bearer ${token}` } })
      .then((res) => setUsers(res.data))
      .catch(() => setUsers([]))
      .finally(() => {});
  }

  useEffect(() => {
    fetchUsers();
  }, [token]);

  function handleAddUser(e) {
    e.preventDefault();
    axios
      .post("/admin/users", newUser, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then(() => {
        setNewUser({ username: "", role: "partner", email: "", org: "" });
        fetchUsers();
      })
      .catch(() => {});
  }

  function handleDeleteUser(username) {
    axios
      .delete(`/admin/users/${username}`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      .then(fetchUsers)
      .catch(() => {});
  }

  return (
    <div
      className="user-management-panel"
      aria-label="User Management"
      tabIndex={0}
      style={{ background: "#f9fafb", padding: 20, borderRadius: 8 }}
    >
      <h3 style={{ color: "#0f172a" }}>User/Partner Management</h3>
      <form onSubmit={handleAddUser} style={{ marginBottom: 16 }}>
        <input
          aria-label="Username"
          required
          placeholder="Username"
          value={newUser.username}
          onChange={(e) =>
            setNewUser((u) => ({ ...u, username: e.target.value }))
          }
          style={{ marginRight: 8, padding: 4 }}
        />
        <input
          aria-label="Email"
          required
          placeholder="Email"
          value={newUser.email}
          onChange={(e) => setNewUser((u) => ({ ...u, email: e.target.value }))}
          style={{ marginRight: 8, padding: 4 }}
        />
        <input
          aria-label="Org"
          required
          placeholder="Org"
          value={newUser.org}
          onChange={(e) => setNewUser((u) => ({ ...u, org: e.target.value }))}
          style={{ marginRight: 8, padding: 4 }}
        />
        <select
          aria-label="Role"
          value={newUser.role}
          onChange={(e) => setNewUser((u) => ({ ...u, role: e.target.value }))}
          style={{ marginRight: 8, padding: 4 }}
        >
          <option value="partner">Partner</option>
          <option value="admin">Admin</option>
        </select>
        <button
          type="submit"
          style={{
            padding: 4,
            background: "#10b981",
            color: "#fff",
            border: "none",
            borderRadius: 4,
          }}
        >
          Add
        </button>
      </form>
      <div style={{ overflowX: "auto" }}>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th>Username</th>
              <th>Email</th>
              <th>Org</th>
              <th>Role</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.map((u) => (
              <tr key={u.username}>
                <td>{u.username}</td>
                <td>{u.email}</td>
                <td>{u.org}</td>
                <td>
                  {enableRoles ? (
                    <select
                      aria-label={`Role for ${u.username}`}
                      value={u.role}
                      onChange={(e) => {
                        const newRole = e.target.value;
                        setUsers((users) =>
                          users.map((user) =>
                            user.username === u.username
                              ? { ...user, role: newRole }
                              : user,
                          ),
                        );
                      }}
                      style={{
                        margin: "0 8px",
                        padding: "2px 6px",
                        borderRadius: 4,
                        border: "1px solid #cbd5e1",
                      }}
                    >
                      <option value="partner">Partner</option>
                      <option value="admin">Admin</option>
                    </select>
                  ) : (
                    u.role
                  )}
                </td>
                <td>
                  <button
                    aria-label={`Delete ${u.username}`}
                    onClick={() => handleDeleteUser(u.username)}
                    style={{
                      background: "#ef4444",
                      color: "#fff",
                      border: "none",
                      borderRadius: 4,
                      padding: "4px 10px",
                    }}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

UserManagementPanel.propTypes = {
  token: "YOUR_TOKEN_HERE",
  enableRoles: PropTypes.bool,
};
