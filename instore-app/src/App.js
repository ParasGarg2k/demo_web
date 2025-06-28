import React, { useMemo } from "react";
import { Routes, Route, Link } from "react-router-dom";
import { Container, AppBar, Toolbar, Typography, Button } from "@mui/material";
import Home from "./pages/Home";
import Search from "./pages/Search";
import Recommendations from "./pages/Recommendations";
import NlpQuery from "./pages/NlpQuery";

function App() {
  return (
    <>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            In-Store Assistant
          </Typography>
          <Button color="inherit" component={Link} to="/">Home</Button>
          <Button color="inherit" component={Link} to="/search">Search</Button>
          <Button color="inherit" component={Link} to="/recommendations">Recommendations</Button>
          <Button color="inherit" component={Link} to="/nlp">NLP Query</Button>
        </Toolbar>
      </AppBar>
      <Container sx={{ marginTop: 4 }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/search" element={<Search />} />
          <Route path="/recommendations" element={<Recommendations />} />
          <Route path="/nlp" element={<NlpQuery />} />
        </Routes>
      </Container>
    </>
  );
}

export default App;
