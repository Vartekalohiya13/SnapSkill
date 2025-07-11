import React, { useState } from "react";
import "../styles/ResumeEnhancer.css";


const ResumeEnhancer = () => {
  const [resume, setResume] = useState(null);
  const [suggestions, setSuggestions] = useState([]);
  const [enhanced, setEnhanced] = useState(null);

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    setResume(file);
    const formData = new FormData();
    formData.append("resume", file);

    const res = await fetch("http://localhost:5001/enhance", {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
    setSuggestions(data.suggestions);
    setEnhanced(data.enhanced_pdf);
  };

  return (
    <div className="enhancer-page">
      <h2>Resume Enhancer</h2>
      <p>Get instant AI-powered suggestions and optimized resume</p>

      <label className="upload-label">
        <input type="file" accept=".pdf" onChange={handleUpload} />
        Upload Resume
      </label>

      {suggestions.length > 0 && (
        <div className="suggestion-box">
          <h4>✨ Suggestions:</h4>
          <ul>
            {suggestions.map((tip, i) => (
              <li key={i}>{tip}</li>
            ))}
          </ul>
          {enhanced && (
            <a
              href={`data:application/pdf;base64,${enhanced}`}
              download="enhanced_resume.pdf"
              className="download-btn"
            >
              Download Enhanced Resume
            </a>
          )}
        </div>
      )}
    </div>
  );
};

export default ResumeEnhancer;
