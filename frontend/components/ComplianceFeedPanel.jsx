import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  Box,
  Typography,
  Paper,
  List,
  ListItem,
  ListItemText,
  CircularProgress,
  Link,
} from "@mui/material";

const ComplianceFeedPanel = () => {
  const [feeds, setFeeds] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios
      .get("/api/compliance/feeds")
      .then((res) => setFeeds(res.data))
      .finally(() => setLoading(false));
  }, []);

  return (
    <Box sx={{ p: 3, bgcolor: "#f8f8f8", borderRadius: 2, mb: 2 }}>
      <Typography variant="h6" mb={2}>
        External Compliance Feeds
      </Typography>
      {loading ? (
        <CircularProgress />
      ) : (
        <Paper>
          <List>
            {feeds.map((feed, i) => (
              <ListItem key={i} alignItems="flex-start">
                <ListItemText
                  primary={
                    <Link href={feed.url} target="_blank" rel="noopener">
                      {feed.url}
                    </Link>
                  }
                  secondary={feed.snippet ? feed.snippet : feed.error}
                />
              </ListItem>
            ))}
          </List>
        </Paper>
      )}
    </Box>
  );
};
export default ComplianceFeedPanel;
