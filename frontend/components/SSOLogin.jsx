import React, { useState } from "react";
import axios from "axios";
import {
  Box,
  Typography,
  Button,
  TextField,
  Alert,
  CircularProgress,
} from "@mui/material";

const SSOLogin = ({ onLogin }) => {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSSO = async () => {
    setLoading(true);
    setError("");
    try {
      // This would redirect to your SSO provider in a real app
      const res = await axios.post("/api/sso/login", { email });
      if (res.data && res.data.success) {
        onLogin(res.data.adminId, res.data.roles);
      } else {
        setError("SSO failed.");
      }
    } catch (e) {
      setError("SSO error.");
    }
    setLoading(false);
  };

  return (
    <Box
      sx={{
        p: 3,
        bgcolor: "#fff",
        borderRadius: 2,
        maxWidth: 400,
        mx: "auto",
        mt: 8,
      }}
    >
      <Typography variant="h6" mb={2}>
        Single Sign-On (SSO) Login
      </Typography>
      <TextField
        label="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        fullWidth
        margin="normal"
      />
      {error && <Alert severity="error">{error}</Alert>}
      <Button
        variant="contained"
        color="primary"
        onClick={handleSSO}
        fullWidth
        disabled={loading || !email}
        sx={{ mt: 2 }}
      >
        {loading ? <CircularProgress size={24} /> : "Login with SSO"}
      </Button>
    </Box>
  );
};
export default SSOLogin;
