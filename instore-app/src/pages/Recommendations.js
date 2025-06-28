import React, { useState } from "react";
import { Button, List, ListItem, ListItemText, Typography } from "@mui/material";

const API_BASE = "http://localhost:8000";

export default function Recommendations() {
  const [recommendations, setRecommendations] = useState([]);

  async function fetchRecommendations() {
    const res = await fetch(`${API_BASE}/recommend/random`);
    const data = await res.json();
    setRecommendations(data);
  }

  return (
    <div>
      <Button variant="contained" onClick={fetchRecommendations}>Get Recommendations</Button>

      {recommendations.length > 0 && (
        <>
          <Typography variant="h6" sx={{ marginTop: 2 }}>Recommended Products:</Typography>
          <List>
            {recommendations.map(p => (
              <ListItem key={p.product_id}>
                <ListItemText primary={p.name} secondary={`$${p.price.toFixed(2)}`} />
              </ListItem>
            ))}
          </List>
        </>
      )}
    </div>
  );
}
