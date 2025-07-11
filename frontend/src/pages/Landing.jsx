import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/landing.css";

import r1 from "../assets/r1.png";
import r2 from "../assets/r2.png";
import r3 from "../assets/r3.png";

const Landing = () => {
  const navigate = useNavigate();
  const resumes = [r1, r2, r3];
  const [current, setCurrent] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrent((prev) => (prev + 1) % resumes.length);
    }, 3000);
    return () => clearInterval(interval);
  }, [resumes.length]);

  return (
    <div className="landing-wrapper">
      {/* Left Text Content */}
      <div className="left-content">
        <h1 className="main-heading">
          Build with <span className="gradient-text">SnapSkill</span>
        </h1>
        <p className="subheading">
          Get your resume ready in minutes with <strong>AI-powered insights</strong> and smart formatting.
        </p>
        <div className="button-group">
  <button className="primary-btn" onClick={() => navigate("/home")}>
    Get Started
  </button>
</div>

      </div>

      {/* Right Carousel Content */}
      <div className="right-content">
        <div className="carousel-container">
          {resumes.map((img, index) => (
            <img
              key={index}
              src={img}
              alt={`Resume ${index}`}
              className={`carousel-img ${index === current ? "active" : "inactive"}`}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default Landing;
