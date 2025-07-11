import React, { useState } from "react";
import axios from "axios";
import "../styles/ResumeEnhancer.css";

const ResumeEnhancer = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [suggestions, setSuggestions] = useState("");
  const [enhancedPDF, setEnhancedPDF] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
    setSuggestions("");
    setEnhancedPDF(null);
  };

  const handleEnhance = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setSuggestions("");
    setEnhancedPDF(null);

    const formData = new FormData();
    formData.append("resume", selectedFile);

    try {
      const res = await axios.post("http://localhost:5000/enhance", formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        },
        responseType: "blob"
      });

      const suggestionsText = decodeURIComponent(
        res.headers["x-suggestions"] || "No suggestions received."
      );
      setSuggestions(suggestionsText);

      const pdfBlob = new Blob([res.data], { type: "application/pdf" });
      setEnhancedPDF(URL.createObjectURL(pdfBlob));
    } catch (err) {
      console.error("Enhancement failed:", err);
      alert("Backend enhancement failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="enhancer-container">
      <h1>🚀 Resume Enhancer</h1>
      <p className="enhancer-subtext">
        Upload your resume and let our AI improve it for ATS compatibility, clarity, and professionalism.
      </p>

      <div className="upload-box">
        <input type="file" accept=".pdf" onChange={handleFileChange} />
        <button onClick={handleEnhance} disabled={loading}>
          {loading ? "Enhancing..." : "Enhance Resume"}
        </button>
      </div>

      {suggestions && (
        <div className="ai-suggestions">
          <h3>🧠 AI Suggestions</h3>
          <pre>{suggestions}</pre>
        </div>
      )}

      {enhancedPDF && (
        <div className="download-box">
          <a href={enhancedPDF} download="enhanced_resume.pdf">
            ⬇️ Download Enhanced Resume
          </a>
        </div>
      )}
    </div>
  );
};

export default ResumeEnhancer;
