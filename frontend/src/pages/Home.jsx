import React from "react";
import "../styles/home.css";
import { useNavigate } from "react-router-dom";

import resumeIcon from "../assets/builder.svg";
import atsIcon from "../assets/ats.svg";
import enhanceIcon from "../assets/enhancer.svg";

const Home = () => {
  const navigate = useNavigate();

  return (
    <div className="home-page">
      {/* Background blobs */}
      <div className="bg-blob blob1"></div>
      <div className="bg-blob blob2"></div>

      {/* Welcome text */}
      <div className="welcome-banner">
        <h2 className="animated-welcome">
          Welcome to <span className="gradient-text">SnapSkill</span>
        </h2>
        <p className="typewriter-effect">
          Your smart assistant for career success 🚀
        </p>
      </div>

      {/* Headings */}
      <h3 className="home-heading">Choose a Tool</h3>
      <p className="home-subheading">Click any option below to get started</p>

      {/* Tool Cards */}
      <div className="tools-container">
        <div className="tool-card" onClick={() => navigate("/resume-builder")}>
          <img src={resumeIcon} alt="Resume Builder" className="tool-icon" />
          <h3>Resume Builder</h3>
          <p>Create a job-winning resume with AI guidance and modern templates.</p>
        </div>

        <div className="tool-card" onClick={() => navigate("/ats-checker")}>
          <img src={atsIcon} alt="ATS Checker" className="tool-icon" />
          <h3>ATS Checker</h3>
          <p>Check if your resume is ATS-friendly and improve your score.</p>
        </div>

        <div className="tool-card" onClick={() => navigate("/resume-enhancer")}>
          <img src={enhanceIcon} alt="Resume Enhancer" className="tool-icon" />
          <h3>Resume Enhancer</h3>
          <p>Enhance your resume with bullet suggestions and AI keyword optimization.</p>
        </div>
      </div>
    </div>
  );
};

export default Home;