import React from "react";
import { Box, Typography, Paper, Chip, Avatar, Divider } from "@mui/material";
import EmojiEventsIcon from "@mui/icons-material/EmojiEvents";
import WhatshotIcon from "@mui/icons-material/Whatshot";

const mockGamification = [
  {
    name: "Reviewer Alpha",
    streak: 12,
    badges: ["Accuracy Pro", "Speedster"],
    avatar: "A",
  },
  {
    name: "Reviewer Beta",
    streak: 8,
    badges: ["Compliance Hero"],
    avatar: "B",
  },
  { name: "Reviewer Gamma", streak: 5, badges: ["Growth Guru"], avatar: "G" },
];

export default function EliteGamificationPanel() {
  return (
    <Paper sx={{ p: 3, mb: 2 }}>
      <Box display="flex" alignItems="center" mb={2}>
        <EmojiEventsIcon sx={{ mr: 1 }} />
        <Typography variant="h6">Reviewer Gamification</Typography>
      </Box>
      <Divider sx={{ mb: 2 }} />
      {mockGamification.map((r, idx) => (
        <Box key={idx} display="flex" alignItems="center" mb={2}>
          <Avatar>{r.avatar}</Avatar>
          <Typography sx={{ ml: 2, fontWeight: "bold", flex: 1 }}>
            {r.name}
          </Typography>
          <Chip
            icon={<WhatshotIcon />}
            label={`Streak: ${r.streak}`}
            color="warning"
            sx={{ mr: 2 }}
          />
          {r.badges.map((b, j) => (
            <Chip key={j} label={b} color="primary" sx={{ mr: 1 }} />
          ))}
        </Box>
      ))}
    </Paper>
  );
}
