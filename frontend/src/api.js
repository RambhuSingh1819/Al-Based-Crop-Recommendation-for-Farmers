// frontend/src/api.js
const API_BASE = "http://localhost:8000"; // same as FastAPI

export async function analyzeImage(file) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE}/analyze`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || "Failed to analyze image");
  }

  // Backend already returns: [{ label, score, box, nutrition, advice }]
  return res.json();
}
