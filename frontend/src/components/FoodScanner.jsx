import { useState, useRef } from "react";
import "./FoodScanner.css";

function FoodScanner({ onAnalyze, loading }) {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const inputRef = useRef(null);

  function handleFile(selected) {
    if (!selected) return;
    setFile(selected);
    setPreview(URL.createObjectURL(selected));
  }

  function handleDrop(e) {
    e.preventDefault();
    setDragActive(false);
    handleFile(e.dataTransfer.files[0]);
  }

  function handleSubmit() {
    if (file) onAnalyze(file);
  }

  return (
    <div
      className={`scanner-dropzone ${dragActive ? "drag-active" : ""}`}
      onDragOver={(e) => { e.preventDefault(); setDragActive(true); }}
      onDragLeave={() => setDragActive(false)}
      onDrop={handleDrop}
    >
      {preview ? (
        <img src={preview} alt="Selected food" className="scanner-preview" />
      ) : (
        <div className="scanner-placeholder">
          <p className="scanner-title">Analyze your meal</p>
          <p className="scanner-subtitle">
            Upload a food photo and FoodMind AI will identify it against our nutrition database.
          </p>
        </div>
      )}

      <input
        ref={inputRef}
        type="file"
        accept="image/*"
        onChange={(e) => handleFile(e.target.files[0])}
        style={{ display: "none" }}
      />

      <div className="scanner-actions">
        <button type="button" onClick={() => inputRef.current.click()}>
          {file ? "Choose a different photo" : "Upload food image"}
        </button>
        {file && (
          <button type="button" className="scanner-analyze-btn" onClick={handleSubmit} disabled={loading}>
            {loading ? "Analyzing..." : "Analyze meal"}
          </button>
        )}
      </div>

      <p className="scanner-dragtext">or drag and drop an image here</p>
    </div>
  );
}

export default FoodScanner;
