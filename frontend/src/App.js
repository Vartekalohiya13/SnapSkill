import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Landing from './pages/Landing';
import Home from "./pages/Home";
import ATSPage from './pages/ATSPage';  // ✅ Import your new ATS page
import ResumeEnhancer from "./pages/ResumeEnhancerPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/home" element={<Home />} />
        <Route path="/ats-checker" element={<ATSPage />} />
        <Route path="/resume-enhancer" element={<ResumeEnhancer />} />

      </Routes>
    </Router>
  );
}

export default App;


