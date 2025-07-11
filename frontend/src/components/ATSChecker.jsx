import React, { useState } from "react";
import axios from "axios";
import "../styles/ATSChecker.css";
import Confetti from "react-confetti";

const ATSChecker = () => {
  const [resumeFile, setResumeFile] = useState(null);
  const [score, setScore] = useState(null);
  const [matched, setMatched] = useState([]);
  const [missing, setMissing] = useState([]);
  const [showConfetti, setShowConfetti] = useState(false);

  const handleFileChange = (e) => {
    setResumeFile(e.target.files[0]);
    setScore(null);
    setMatched([]);
    setMissing([]);
    setShowConfetti(false);
  };

  const handleCheckATS = async () => {
    if (!resumeFile) return alert("Upload your resume!");

    const formData = new FormData();
    formData.append("resume", resumeFile);

    try {
      const res = await axios.post("http://127.0.0.1:5000/match", formData);
      setScore(res.data.score);
      setMatched(res.data.matched_keywords.map(k => k.keyword));
      setMissing(res.data.job_text.split(" ").filter(k => !res.data.resume_text.includes(k)));
      if (res.data.score >= 70) setShowConfetti(true);
    } catch (err) {
      alert("Error checking ATS score.");
    }
  };

  return (
    <div className="ats-container">
      {showConfetti && <Confetti />}

      <h1 className="ats-heading">Welcome to SnapSkill ATS Checker</h1>
      <p className="ats-subheading">
        Discover how well your resume performs in real-world hiring systems.
        Our AI-powered tool evaluates your resume and gives you a personalized ATS score instantly.
      </p>

      <div className="ats-grid">
        <div className="upload-box">
          <h2>Upload Your Resume</h2>
          <input type="file" onChange={handleFileChange} accept="application/pdf" />
          <button onClick={handleCheckATS}>Check ATS Score</button>
        </div>

        <div className="score-box">
          <h2>Your ATS Score</h2>
          <div className="circle-score">
            {score !== null ? <span>{score}%</span> : <span>--</span>}
          </div>
        </div>
      </div>

      {score !== null && (
        <>
          <div className="keyword-section">
            <div className="matched">
              <h3>✅ Matched Keywords</h3>
              <div className="tags">
                {matched.length > 0 ? matched.map((kw, i) => (
                  <span key={i} className="tag green">{kw}</span>
                )) : <span className="none">No keywords matched</span>}
              </div>
            </div>

            <div className="missing">
              <h3>❌ Missing Keywords</h3>
              <div className="tags">
                {missing.length > 0 ? missing.slice(0, 15).map((kw, i) => (
                  <span key={i} className="tag red">{kw}</span>
                )) : <span className="none">Nothing missing!</span>}
              </div>
            </div>
          </div>

          <div className="enhancer-link">
            <p>Want to improve your score?</p>
            <a href="/resume-enhancer">Try our Resume Enhancer →</a>
          </div>
        </>
      )}
    </div>
  );
};

export default ATSChecker;
