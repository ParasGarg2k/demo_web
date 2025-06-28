import React, { useState } from "react";
import { TextField, Button, List, ListItem, ListItemText, Typography, CircularProgress } from "@mui/material";

const API_BASE = "http://localhost:8000";

export default function Search() {
  const [searchTerm, setSearchTerm] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [loading, setLoading] = useState(false);

  async function handleSearch() {
    if (searchTerm.length < 2) {
      alert("Enter at least 2 characters to search");
      return;
    }
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/product/search?query=${encodeURIComponent(searchTerm)}`);
      const data = await res.json();
      setSearchResults(data.results);
    } catch {
      alert("Error fetching products");
    }
    setLoading(false);
  }

  return (
    <div>
      <TextField
        label="Search products"
        variant="outlined"
        value={searchTerm}
        onChange={e => setSearchTerm(e.target.value)}
        sx={{ width: "60%", marginRight: 2 }}
      />
      <Button variant="contained" onClick={handleSearch}>Search</Button>

      {loading && <CircularProgress sx={{ marginTop: 2 }} />}

      <List>
        {searchResults.map((p) => (
          <ListItem key={p.product_id}>
            <ListItemText
              primary={p.name}
              secondary={`Stock: ${p.stock_quantity} | Aisle: ${p.aisle_id}`}
            />
          </ListItem>
        ))}
      </List>
    </div>
  );
}
