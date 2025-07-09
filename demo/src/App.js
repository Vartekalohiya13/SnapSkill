import React, { useState } from 'react';
import axios from 'axios';
import Confetti from 'react-confetti';
import { useDropzone } from 'react-dropzone';
import { motion } from 'framer-motion';
import { Toaster, toast } from 'react-hot-toast';
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar';
import 'react-circular-progressbar/dist/styles.css';

function App() {
  const [resumeFile, setResumeFile] = useState(null);
  const [jobFile, setJobFile] = useState(null);
  const [score, setScore] = useState(null);
  const [keywords, setKeywords] = useState([]);
  const [resumeText, setResumeText] = useState("");
  const [jobText, setJobText] = useState("");
  const [loading, setLoading] = useState(false);
  const [darkMode, setDarkMode] = useState(true);
  const [showConfetti, setShowConfetti] = useState(false);
  const [showTips, setShowTips] = useState(false);
  const [step, setStep] = useState(1);

  const handleSubmit = async () => {
    if (!resumeFile || !jobFile) {
      toast.error("Please upload both files.");
      return;
    }

    const formData = new FormData();
    formData.append("resume", resumeFile);
    formData.append("job", jobFile);

    try {
      setLoading(true);
      toast.loading("Analyzing your resume...");
      const response = await axios.post("http://localhost:5000/match", formData);
      setScore(response.data.score);
      setKeywords(response.data.matched_keywords);
      setResumeText(response.data.resume_text);
      setJobText(response.data.job_text);
      toast.dismiss();
      toast.success("Analysis complete!");

      if (response.data.score >= 30) {
        setShowConfetti(true);
        setTimeout(() => setShowConfetti(false), 5000);
      }
      setStep(3);
    } catch (err) {
      toast.dismiss();
      toast.error("Backend error. Make sure Flask is running.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const highlightMatches = (text) => {
    if (!text || keywords.length === 0) return text;
    const words = keywords.map(k => k.keyword);
    const escapedKeywords = words.map(k => k.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
    const regex = new RegExp(`\\b(${escapedKeywords.join('|')})\\b`, 'gi');
    return text.split(regex).map((part, i) =>
      words.some(k => k.toLowerCase() === part.toLowerCase()) ?
        <mark key={i} className="bg-green-300 dark:bg-green-600 px-1 rounded">{part}</mark> :
        <span key={i}>{part}</span>
    );
  };

  const resumeDrop = useDropzone({
    accept: { "application/pdf": [".pdf"] },
    onDrop: (acceptedFiles) => {
      setResumeFile(acceptedFiles[0]);
      if (acceptedFiles[0] && jobFile) setStep(2);
    }
  });

  const jobDrop = useDropzone({
    accept: { "application/pdf": [".pdf"] },
    onDrop: (acceptedFiles) => {
      setJobFile(acceptedFiles[0]);
      if (acceptedFiles[0] && resumeFile) setStep(2);
    }
  });

  return (
    <div className={`${darkMode ? 'dark' : ''} font-sans`}>
      <Toaster position="top-right" />
      {showConfetti && <Confetti />}
      <div className="min-h-screen bg-gradient-to-br from-indigo-900 via-gray-900 to-gray-800 flex items-center justify-center p-6 transition-all">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.4 }}
          className="bg-white dark:bg-gray-900 text-gray-900 dark:text-white shadow-2xl rounded-3xl w-full max-w-5xl p-10 space-y-8 border border-gray-700"
        >
          <div className="flex justify-between items-center">
            <h1 className="text-4xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-purple-400 to-pink-500">
              🚀 ATS Resume Matcher
            </h1>
            <button
              className="bg-gray-300 dark:bg-gray-700 text-sm px-4 py-2 rounded shadow hover:bg-gray-400 dark:hover:bg-gray-600 transition"
              onClick={() => setDarkMode(!darkMode)}
            >
              {darkMode ? "🌞 Light" : "🌙 Dark"}
            </button>
          </div>

          <div className="flex justify-center items-center space-x-6 mb-6">
            {[1, 2, 3].map((s) => (
              <div key={s} className="flex flex-col items-center">
                <div className={`w-10 h-10 rounded-full flex items-center justify-center font-bold 
                  ${step >= s ? 'bg-green-500 text-white' : 'bg-gray-300 dark:bg-gray-700 text-gray-600 dark:text-gray-300'}`}>
                  {s}
                </div>
                <span className="mt-2 text-sm text-center">
                  {s === 1 && 'Upload Files'}
                  {s === 2 && 'Submit'}
                  {s === 3 && 'Result'}
                </span>
              </div>
            ))}
          </div>

          <div className="flex justify-end">
            <button
              onClick={() => setShowTips(!showTips)}
              className="text-sm text-blue-400 hover:text-blue-600 underline mb-4"
            >
              {showTips ? "Hide Tips" : "💡 Tips for better matching"}
            </button>
          </div>

          {showTips && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="bg-yellow-100 dark:bg-yellow-900 text-yellow-800 dark:text-yellow-100 p-4 rounded-xl text-sm"
            >
              <ul className="list-disc ml-5 space-y-1">
                <li>Include job-specific keywords in your resume.</li>
                <li>Use clear headings like "Skills", "Experience".</li>
                <li>Match your terminology to the job description.</li>
              </ul>
            </motion.div>
          )}

          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <label className="block font-semibold mb-2">Upload Resume PDF:</label>
              <div {...resumeDrop.getRootProps()} className="border-2 border-dashed border-blue-400 p-5 rounded-lg text-center hover:border-blue-600 cursor-pointer transition-all">
                <input {...resumeDrop.getInputProps()} />
                <p>{resumeFile ? `📄 ${resumeFile.name}` : "📎 Drag & drop or click to upload"}</p>
              </div>
            </div>

            <div>
              <label className="block font-semibold mb-2">Upload Job Description PDF:</label>
              <div {...jobDrop.getRootProps()} className="border-2 border-dashed border-pink-400 p-5 rounded-lg text-center hover:border-pink-600 cursor-pointer transition-all">
                <input {...jobDrop.getInputProps()} />
                <p>{jobFile ? `📄 ${jobFile.name}` : "📎 Drag & drop or click to upload"}</p>
              </div>
            </div>
          </div>

          {loading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-sm text-purple-300 mb-2 text-center"
            >
              🧠 Running keyword extraction, comparing with job description...
            </motion.div>
          )}

          <button
            onClick={handleSubmit}
            disabled={loading}
            className="w-full bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 hover:from-pink-600 hover:to-indigo-600 text-white font-semibold py-3 px-6 rounded-xl transition-all shadow-md flex justify-center items-center gap-2"
          >
            {loading ? (
              <>
                <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"></path>
                </svg>
                <span>Analyzing your resume...</span>
              </>
            ) : (
              "🔍 Submit"
            )}
          </button>

          {score !== null && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="text-center mt-6 p-6 rounded-xl bg-gradient-to-br from-gray-700 to-gray-800 text-white shadow-lg"
            >
              <h2 className="text-2xl font-bold mb-4">✅ ATS Match Score</h2>
              <div className="w-32 h-32 mx-auto mb-4">
                <CircularProgressbar
                  value={score}
                  text={`${score}%`}
                  styles={buildStyles({
                    textColor: '#ffffff',
                    pathColor: '#4ade80',
                    trailColor: '#334155',
                    textSize: '16px'
                  })}
                />
              </div>
              <p className="mt-4 text-sm">🎯 Matched Keywords</p>
              <table className="w-full mt-2 text-sm border border-gray-600 rounded overflow-hidden">
                <thead>
                  <tr className="bg-gray-600 text-white">
                    <th className="p-2">Keyword</th>
                    <th className="p-2">Relevance</th>
                    <th className="p-2">Source</th>
                  </tr>
                </thead>
                <tbody>
                  {keywords.map((kw, i) => (
                    <tr key={i} className="even:bg-gray-700 odd:bg-gray-800 text-white text-center">
                      <td className="p-2">{kw.keyword}</td>
                      <td className="p-2">{kw.relevance}</td>
                      <td className="p-2">{kw.source}</td>
                    </tr>
                  ))}
                </tbody>
              </table>

              <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6 text-left">
                <div>
                  <h3 className="text-lg font-semibold mb-2">📄 Resume Text</h3>
                  <div className="p-4 bg-gray-800 rounded-lg text-sm leading-relaxed max-h-60 overflow-y-auto">
                    {highlightMatches(resumeText)}
                  </div>
                </div>
                <div>
                  <h3 className="text-lg font-semibold mb-2">📋 Job Description</h3>
                  <div className="p-4 bg-gray-800 rounded-lg text-sm leading-relaxed max-h-60 overflow-y-auto">
                    {highlightMatches(jobText)}
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </motion.div>
      </div>
    </div>
  );
}

export default App;
