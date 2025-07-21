import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  Box,
  Typography,
  Button,
  TextField,
  MenuItem,
  Paper,
  Table,
  TableHead,
  TableRow,
  TableCell,
  TableBody,
  CircularProgress,
  Snackbar,
} from "@mui/material";

const POLICY_TYPES = [
  { value: "rotation", label: "Secret Rotation" },
  { value: "override", label: "Manual Override" },
  { value: "anomaly", label: "Usage Anomaly" },
  { value: "workflow", label: "Regulatory Workflow" },
];

const PolicyEditor = () => {
  const [policies, setPolicies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [snackbar, setSnackbar] = useState("");
  const [editing, setEditing] = useState(null);
  const [newPolicy, setNewPolicy] = useState({
    type: "rotation",
    block: false,
    description: "",
  });

  const fetchPolicies = () => {
    setLoading(true);
    axios
      .get("/api/policy/list")
      .then((res) => setPolicies(res.data))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchPolicies();
  }, []);

  const handleSave = () => {
    axios
      .post("/api/policy/save", { policy: editing })
      .then(() => {
        setSnackbar("Policy saved.");
        setEditing(null);
        fetchPolicies();
      })
      .catch(() => setSnackbar("Save failed."));
  };

  const handleAdd = () => {
    axios
      .post("/api/policy/add", { policy: newPolicy })
      .then(() => {
        setSnackbar("Policy added.");
        setNewPolicy({ type: "rotation", block: false, description: "" });
        fetchPolicies();
      })
      .catch(() => setSnackbar("Add failed."));
  };

  const handleDelete = (idx) => {
    axios
      .post("/api/policy/delete", { idx })
      .then(() => {
        setSnackbar("Policy deleted.");
        fetchPolicies();
      })
      .catch(() => setSnackbar("Delete failed."));
  };

  return (
    <Box sx={{ p: 3, bgcolor: "#f8f8f8", borderRadius: 2, mb: 2 }}>
      <Typography variant="h6" mb={2}>
        SAFE AI Policy Editor
      </Typography>
      <Paper sx={{ p: 2, mb: 2 }}>
        <Typography variant="subtitle1">Add New Policy</Typography>
        <Box
          sx={{
            display: "flex",
            gap: 2,
            alignItems: "center",
            flexWrap: "wrap",
          }}
        >
          <TextField
            select
            label="Type"
            value={newPolicy.type}
            onChange={(e) =>
              setNewPolicy((p) => ({ ...p, type: e.target.value }))
            }
            size="small"
          >
            {POLICY_TYPES.map((t) => (
              <MenuItem key={t.value} value={t.value}>
                {t.label}
              </MenuItem>
            ))}
          </TextField>
          <TextField
            label="Description"
            value={newPolicy.description}
            onChange={(e) =>
              setNewPolicy((p) => ({ ...p, description: e.target.value }))
            }
            size="small"
            sx={{ width: 220 }}
          />
          <Button
            variant={newPolicy.block ? "contained" : "outlined"}
            color="error"
            onClick={() => setNewPolicy((p) => ({ ...p, block: !p.block }))}
          >
            {newPolicy.block ? "Block" : "Allow"}
          </Button>
          <Button
            variant="contained"
            onClick={handleAdd}
            disabled={!newPolicy.description}
          >
            Add
          </Button>
        </Box>
      </Paper>
      {loading ? (
        <CircularProgress />
      ) : (
        <Paper>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Type</TableCell>
                <TableCell>Description</TableCell>
                <TableCell>Block?</TableCell>
                <TableCell>Action</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {policies.map((p, i) => (
                <TableRow key={i} selected={editing === i}>
                  <TableCell>{p.type}</TableCell>
                  <TableCell>
                    {editing === i ? (
                      <TextField
                        value={p.description}
                        onChange={(e) =>
                          setEditing({ ...p, description: e.target.value })
                        }
                        size="small"
                      />
                    ) : (
                      p.description
                    )}
                  </TableCell>
                  <TableCell>
                    {editing === i ? (
                      <Button
                        variant={p.block ? "contained" : "outlined"}
                        color="error"
                        onClick={() => setEditing({ ...p, block: !p.block })}
                      >
                        {p.block ? "Block" : "Allow"}
                      </Button>
                    ) : p.block ? (
                      "Block"
                    ) : (
                      "Allow"
                    )}
                  </TableCell>
                  <TableCell>
                    {editing === i ? (
                      <Button size="small" onClick={handleSave}>
                        Save
                      </Button>
                    ) : (
                      <Button
                        size="small"
                        onClick={() => setEditing({ ...p, idx: i })}
                      >
                        Edit
                      </Button>
                    )}
                    <Button
                      size="small"
                      color="error"
                      onClick={() => handleDelete(i)}
                    >
                      Delete
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </Paper>
      )}
      <Snackbar
        open={!!snackbar}
        autoHideDuration={3000}
        onClose={() => setSnackbar("")}
        message={snackbar}
      />
    </Box>
  );
};
export default PolicyEditor;
