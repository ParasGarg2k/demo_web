import React, { useState } from "react";
import { TextField, Button, Typography } from "@mui/material";

const API_BASE = "http://localhost:8000";

export default function NlpQuery() {
  const [query, setQuery] = useState("");
  const [result, setResult] = useState(null);

  async function handleSubmit(e) {
    e.preventDefault();
    const res = await fetch(`${API_BASE}/nlp/parse`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });
    const data = await res.json();
    setResult(data);
  }

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <TextField
          label="Ask something"
          variant="outlined"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          sx={{ width: "60%", marginRight: 2 }}
        />
        <Button variant="contained" type="submit">Parse</Button>
      </form>

      {result && (
        <div style={{ marginTop: 20 }}>
          <Typography><strong>Intent:</strong> {result.intent}</Typography>
          <Typography><strong>Entities:</strong> {result.entities.join(", ")}</Typography>
        </div>
      )}
    </div>
  );
}
