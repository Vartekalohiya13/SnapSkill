// File: src/pages/Home.jsx
import React from "react";
import "../styles/home.css";
import builder from "../assets/builder.svg";
import enhancer from "../assets/enhancer.svg";

const Home = () => {
  return (
    <div className="home-container">
      <h1 className="main-heading">
        Welcome to <span className="brand">SnapSkill</span>
      </h1>
      <p className="tagline">Build. Enhance. Conquer the Job Market. 🚀</p>

      <h2>Choose a Tool</h2>
      <p className="small">Click any option below to get started</p>

      <div className="tool-cards">
        <div
          className="tool-card"
          onClick={() => (window.location.href = "/resume-builder")}
        >
          <img src={builder} alt="Resume Builder" />
          <h3>Resume Builder</h3>
          <p>
            Create a job-winning resume with AI guidance and modern templates.
          </p>
        </div>

        <div
          className="tool-card"
          onClick={() => (window.location.href = "/ats-checker")}
        >
          <img src="https://img.icons8.com/ios-filled/50/4CAF50/bar-chart.png" alt="ATS Checker" />
          <h3>ATS Checker</h3>
          <p>Check if your resume is ATS-friendly and improve your score.</p>
        </div>

        <div
          className="tool-card"
          onClick={() => (window.location.href = "/resume-enhancer")}
        >
          <img src={enhancer} alt="Resume Enhancer" />
          <h3>Resume Enhancer</h3>
          <p>
            Enhance your resume with bullet suggestions and AI keyword
            optimization.
          </p>
        </div>
      </div>
    </div>
  );
};

export default Home;
