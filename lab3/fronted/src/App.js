import React from "react";
import "./styles.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./Home";
import Lab2 from "./lab2";

function App() {
  return (
    <BrowserRouter>
    <Routes>
          <Route exact path="/" element={<Home />} />
          <Route path="/lab2" element={<Lab2 />} />
        </Routes>
    </BrowserRouter>
  );
}

export default App;
