import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

const API_BASE = "http://localhost:8000";

function App() {
  const [file, setFile] = useState(null);
  const [repoName, setRepoName] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");

  const [uploading, setUploading] = useState(false);
  const [querying, setQuerying] = useState(false);
  const [finishing, setFinishing] = useState(false);

  useEffect(() => {
    const storedRepo = localStorage.getItem("repo_name");

    if (storedRepo) {
      setRepoName(storedRepo);
    }
  }, []);

  const uploadRepository = async () => {
    if (!file) {
      alert("Please select a ZIP file.");
      return;
    }

    try {
      setUploading(true);

      const formData = new FormData();
      formData.append("zip_file", file);

      const response = await axios.post(
        `${API_BASE}/repo-extract/upload-zipfile`,
        formData
      );

      const repository = response.data.repository;

      setRepoName(repository);
      localStorage.setItem("repo_name", repository);

      alert("Repository uploaded successfully.");
    } catch (error) {
      console.error(error);
      alert("Upload failed.");
    } finally {
      setUploading(false);
    }
  };

  const askQuestion = async () => {
    if (!repoName) {
      alert("Please upload a repository first.");
      return;
    }

    if (!question.trim()) {
      alert("Enter a question.");
      return;
    }

    try {
      setQuerying(true);

      const response = await axios.post(
        `${API_BASE}/query/query`,
        {
          repo_name: repoName,
          query: question,
        }
      );

      setAnswer(response.data.answer);
    } catch (error) {
      console.error(error);
      alert("Query failed.");
    } finally {
      setQuerying(false);
    }
  };

  const finishQuerying = async () => {
    try {
      setFinishing(true);

      await axios.delete(`${API_BASE}/finish/delete-repo/${repoName}`);


      localStorage.removeItem("repo_name");

      setRepoName("");
      setQuestion("");
      setAnswer("");
      setFile(null);

      alert("Repository removed successfully.");
    } catch (error) {
      console.error(error);
      alert("Failed to remove repository.");
    } finally {
      setFinishing(false);
    }
  };

  return (
    <div className="app">
      <div className="container">

        <header className="hero">

  <div className="hero-content">

    <div className="hero-badge">
      AI-Powered Repository Intelligence
    </div>

    <h1 className="hero-title">
      CodeBase
      <span> Navigator</span>
    </h1>

    <p className="hero-description">
      Upload repositories, analyze architecture, understand workflows,
      discover APIs, and ask natural language questions about your codebase.
    </p>

    <div className="hero-stats">
      <div className="stat-card">
        <h3>📦</h3>
        <p>Repository Analysis</p>
      </div>

      <div className="stat-card">
        <h3>🔍</h3>
        <p>Semantic Search</p>
      </div>

      <div className="stat-card">
        <h3>🤖</h3>
        <p>AI Answers</p>
      </div>

      <div className="stat-card">
        <h3>⚡</h3>
        <p>Instant Insights</p>
      </div>
    </div>

  </div>

</header>

        <div className="top-section">

  <div className="card">
    <h2>Upload Repository</h2>

    <label className="upload-area">
      <input
        type="file"
        accept=".zip"
        hidden
        onChange={(e) => setFile(e.target.files[0])}
      />

      <div className="upload-content">
        <div className="upload-icon">📁</div>

        <p>
          {file
            ? file.name
            : "Click to select a ZIP repository"}
        </p>

        <small>Supported format: .zip</small>
      </div>
    </label>

    <button
      className="primary-btn"
      onClick={uploadRepository}
      disabled={uploading}
    >
      {uploading
        ? "Uploading..."
        : "Upload Repository"}
    </button>
  </div>

  <div className="card">
    <h2>Repository Status</h2>

    {repoName ? (
      <div className="repo-box">
        <span className="status-dot"></span>
        {repoName}
      </div>
    ) : (
      <div className="empty-state">
        No repository uploaded
      </div>
    )}
  </div>

</div>

<div className="card query-card">
  <h2>Ask Questions</h2>

  <textarea
    placeholder="Example: Explain the authentication flow, project architecture, API endpoints..."
    value={question}
    onChange={(e) => setQuestion(e.target.value)}
  />

  <div className="button-group">
    <button
      className="primary-btn"
      onClick={askQuestion}
      disabled={querying}
    >
      {querying
        ? "Generating Answer..."
        : "Ask Question"}
    </button>

    <button
      className="danger-btn"
      onClick={finishQuerying}
      disabled={!repoName || finishing}
    >
      {finishing
        ? "Removing..."
        : "Finish Querying"}
    </button>
  </div>
</div>

{answer && (
  <div className="card answer-card">
    <h2>AI Response</h2>

    <div className="answer">
      {answer}
    </div>
  </div>
)}

      </div>
    </div>
  );
}

export default App;