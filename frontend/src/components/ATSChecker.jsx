
import React, { useState } from "react";
import "../styles/ATSChecker.css";

const ATSChecker = () => {
  const [score, setScore] = useState(null);
  const [resume, setResume] = useState(null);
  const [suggestions, setSuggestions] = useState([]);
  const [keywords, setKeywords] = useState({ matched: [], missing: [] });

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    setResume(file);
    const formData = new FormData();
    formData.append("resume", file);

    const res = await fetch("http://localhost:5000/match", {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
    setScore(data.ats_score);
    setSuggestions(data.suggestions || []);
    setKeywords({ matched: data.matched_keywords, missing: data.missing_keywords });
  };

  return (
    <div className="ats-page">
      <h2>ATS Resume Checker</h2>
      <p>Upload your resume and see how well it matches the job description</p>

      <label className="upload-label">
        <input type="file" accept=".pdf" onChange={handleUpload} />
        Choose Resume PDF
      </label>

      {score && (
        <div className="result-box">
          <div className="score-ring">
            <span>{score}%</span>
          </div>

          <div className="keywords-box">
            <div>
              <h4>✅ Matched Keywords</h4>
              <div className="chips green">
                {keywords.matched.map((word, i) => (
                  <span key={i}>{word}</span>
                ))}
              </div>
            </div>
            <div>
              <h4>❌ Missing Keywords</h4>
              <div className="chips red">
                {keywords.missing.map((word, i) => (
                  <span key={i}>{word}</span>
                ))}
              </div>
            </div>
          </div>

          <div className="tips">
            <h4>🔧 Suggestions to Improve:</h4>
            <ul>
              {suggestions.map((tip, i) => (
                <li key={i}>{tip}</li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export default ATSChecker;