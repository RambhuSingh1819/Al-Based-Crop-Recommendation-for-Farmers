import { useRef, useState } from "react";
import "./App.css";
import { analyzeImage } from "./api";

function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const [error, setError] = useState("");
  const inputRef = useRef(null);

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (!selected) return;
    setError("");
    setFile(selected);
    setPreview(URL.createObjectURL(selected));
    setPredictions([]);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    const droppedFile = e.dataTransfer.files[0];
    if (!droppedFile) return;
    setError("");
    setFile(droppedFile);
    setPreview(URL.createObjectURL(droppedFile));
    setPredictions([]);
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError("Please upload an image first.");
      return;
    }

    setLoading(true);
    setError("");
    setPredictions([]);

    try {
      const data = await analyzeImage(file); // uses frontend/api.js
      setPredictions(data);                  // backend returns an array
    } catch (err) {
      console.error(err);
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  const openFileDialog = () => {
    inputRef.current?.click();
  };

  return (
    <div className="app">
      {/* animated background blobs */}
      <div className="bg-blob bg-blob-1" />
      <div className="bg-blob bg-blob-2" />
      <div className="bg-blob bg-blob-3" />

      <header className="header">
        <h1 className="title">
          🌾 Farm <span>Advisor</span>
        </h1>
        <p className="subtitle">
          Upload a field or crop image to get instant insights, nutrition tips and
          smart advice.
        </p>
      </header>

      <main className="main-card">
        {/* Upload side */}
        <section className="upload-section">
          <div
            className={`dropzone ${dragActive ? "dropzone-active" : ""}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={openFileDialog}
          >
            <input
              type="file"
              accept="image/*"
              ref={inputRef}
              onChange={handleFileChange}
              hidden
            />

            {!preview && (
              <>
                <div className="upload-icon">📷</div>
                <p className="drop-title">Drop your field image here</p>
                <p className="drop-subtitle">or click to browse</p>
              </>
            )}

            {preview && (
              <div className="preview-wrapper">
                <img src={preview} alt="Preview" className="preview-image" />
                <div className="preview-overlay">
                  <span>Change Image</span>
                </div>
              </div>
            )}
          </div>

          <button
            className={`analyze-btn ${loading ? "analyze-btn-loading" : ""}`}
            onClick={handleAnalyze}
            disabled={loading}
          >
            {loading ? (
              <div className="loader">
                <div className="dot" />
                <div className="dot" />
                <div className="dot" />
              </div>
            ) : (
              "🔍 Analyze Field"
            )}
          </button>

          {error && <p className="error-text">⚠️ {error}</p>}

          <p className="hint">
            Tip: Use clear daylight photos of your crop or soil for the best results.
          </p>
        </section>

        {/* Results side */}
        <section className="results-section">
          <h2 className="results-title">Analysis Results</h2>

          {loading && (
            <div className="results-placeholder">
              <div className="skeleton skeleton-title" />
              <div className="skeleton skeleton-line" />
              <div className="skeleton skeleton-line" />
            </div>
          )}

          {!loading && predictions && predictions.length > 0 && (
            <div className="results-grid">
              {predictions.map((item, idx) => (
                <div key={idx} className="result-card fade-in-up">
                  <div className="result-header">
                    <span className="badge">
                      {(item.score * 100).toFixed(1)}% confidence
                    </span>
                    <h3 className="result-label">{item.label}</h3>
                  </div>

                  {item.box && item.box.length === 4 && (
                    <p className="result-box">
                      📍 Area: x={item.box[0]}, y={item.box[1]}, w={item.box[2]}, h={item.box[3]}
                    </p>
                  )}

                  {item.nutrition && (
                    <p className="result-nutrition">
                      🧪 <strong>Nutrition:</strong> {item.nutrition}
                    </p>
                  )}

                  {item.advice && (
                    <p className="result-advice">
                      🌱 <strong>Advice:</strong> {item.advice}
                    </p>
                  )}
                </div>
              ))}
            </div>
          )}

          {!loading && (!predictions || predictions.length === 0) && (
            <div className="results-placeholder">
              <p className="placeholder-text">
                Analysis results will appear here after you upload an image and click{" "}
                <strong>Analyze Field</strong>.
              </p>
            </div>
          )}
        </section>
      </main>

      <footer className="footer">
        <span>Built with FastAPI + React • Smart farming made simple 🌿</span>
      </footer>
    </div>
  );
}

export default App;
