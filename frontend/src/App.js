import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Landing from './pages/Landing';
import Home from "./pages/Home";
import ResumeBuilderPage from "./pages/ResumeBuilderPage";
import ATSPage from './pages/ATSPage';  // ✅ Import your new ATS page
import ResumeEnhancerPage from "./pages/ResumeEnhancerPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/home" element={<Home />} />
        <Route path="/resume-builder" element={<ResumeBuilderPage />} />

        <Route path="/ats-checker" element={<ATSPage />} />
        <Route path="/resume-enhancer" element={<ResumeEnhancerPage />} />

      </Routes>
    </Router>
  );
}

export default App;


