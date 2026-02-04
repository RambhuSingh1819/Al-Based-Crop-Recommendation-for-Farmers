import os
from typing import Any, Dict, List

import torch
from PIL import Image
from transformers import pipeline

# ============================
# 1. Load model ID from environment ONLY
# ============================

HF_MODEL_ID = os.getenv("HF_MODEL_ID")

if not HF_MODEL_ID:
    raise EnvironmentError(
        "HF_MODEL_ID environment variable is not set. "
        "Run the project using setup.sh / docker-compose or export it manually."
    )

_device = "cuda" if torch.cuda.is_available() else "cpu"
_pipe = None  # HF pipeline (lazy-loaded)

# -----------------------------
# 2. Domain knowledge (safe, static)
# -----------------------------

NUTRIENT_GUIDE: Dict[str, str] = {
    "Nitrogen": "Apply a balanced nitrogen source (e.g., Urea or compost) in split doses.",
    "Phosphorus": "Use DAP fertilizer closer to the root zone.",
    "Potassium": "Apply MOP fertilizer for disease resistance.",
    "Magnesium": "Add Epsom salt for chlorophyll production.",
    "No deficiency": "No nutrient deficiency detected; maintain your current schedule.",
}

DISEASE_GUIDE: Dict[str, Dict[str, str]] = {
    "Healthy": {
        "summary": "The crop appears healthy.",
        "field_action": "Continue your irrigation and fertilizer schedule.",
        "extra": "Monitor your field weekly to catch early symptoms.",
    },
    "Powdery Mildew": {
        "summary": "White or grayish powder suggests fungal infection.",
        "field_action": "Remove infected leaves and avoid overhead irrigation.",
        "extra": "Improve airflow and consider fungicides if spreading.",
    },
    "Leaf Blast": {
        "summary": "Irregular lesions indicate blast disease.",
        "field_action": "Avoid excess nitrogen; ensure proper drainage.",
        "extra": "Use resistant varieties if available.",
    },
    "Bacterial Blight": {
        "summary": "Water-soaked lesions and wilting indicate bacterial blight.",
        "field_action": "Remove infected plants and avoid touching leaves when wet.",
        "extra": "Use clean tools and disease-free seeds.",
    },
    "Early Blight": {
        "summary": "Brown concentric rings indicate early blight.",
        "field_action": "Remove affected leaves and reduce moisture duration.",
        "extra": "Practice crop rotation and proper spacing.",
    },
}

DISEASE_TO_NUTRIENT: Dict[str, str] = {
    "Healthy": "No deficiency",
    "Mildew": "Potassium",
    "Blight": "Nitrogen",
    "Spot": "Nitrogen",
    "Rust": "Potassium",
}

# ============================
# 3. Model loading (lazy, using pipeline)
# ============================


def _load_hf_pipeline():
    """Lazy-load a Hugging Face image-classification pipeline."""
    global _pipe

    if _pipe is None:
        print(f"[HF] Loading pipeline for '{HF_MODEL_ID}' on device={_device} ...")
        device_index = 0 if _device == "cuda" else -1

        try:
            _pipe = pipeline(
                task="image-classification",
                model=HF_MODEL_ID,
                device=device_index,
            )
        except Exception as e:
            raise RuntimeError(
                f"❌ Failed to load HuggingFace pipeline for '{HF_MODEL_ID}'. Error: {e}"
            )

        print("[HF] Pipeline loaded successfully.")

    return _pipe


# ============================
# 4. Helper functions
# ============================


def _normalize_label(raw_label: str) -> str:
    """e.g. 'bean_rust' → 'Bean rust'."""
    label = raw_label.replace("_", " ").strip()
    if not label:
        return "Unknown"
    return label[0].upper() + label[1:]


def _severity_from_score(score: float) -> str:
    if score < 0.4:
        return "mild"
    elif score < 0.7:
        return "moderate"
    return "severe"


def _guess_nutrient_from_label(label: str) -> str:
    label_lower = label.lower()
    for key, nutrient in DISEASE_TO_NUTRIENT.items():
        if key.lower() in label_lower:
            return nutrient
    return "No deficiency"


def _build_advice(label: str, nutrient: str, score: float) -> str:
    severity = _severity_from_score(score)
    disease_info = DISEASE_GUIDE.get(label, {})
    nutrient_info = NUTRIENT_GUIDE.get(nutrient, "")

    advice_parts: List[str] = []

    if label.lower().startswith("healthy"):
        advice_parts.append("The crop appears healthy.")
        advice_parts.append("No visible signs of stress or disease.")
    else:
        summary = disease_info.get("summary", f"Issue detected: {label}.")
        advice_parts.append(
            f"{summary} Severity: **{severity}** ({score * 100:.1f}% confidence)."
        )

    field_action = disease_info.get("field_action")
    if field_action:
        advice_parts.append(f"Field Action: {field_action}")

    if nutrient == "No deficiency":
        advice_parts.append(
            "Nutrient status looks normal. Maintain your current fertilizer plan."
        )
    else:
        advice_parts.append(f"Possible **{nutrient} deficiency**. {nutrient_info}")

    extra = disease_info.get("extra")
    if extra:
        advice_parts.append(f"Tip: {extra}")

    advice_parts.append("Re-check the field in 3–5 days for changes or spreading.")

    return " ".join(advice_parts)


# ============================
# 5. Main prediction API
# ============================


def predict_image(image_path: str) -> List[Dict[str, Any]]:
    """
    Run the HF image-classification pipeline on the given image and
    return the best prediction.
    """
    pipe = _load_hf_pipeline()

    # Load image
    image = Image.open(image_path).convert("RGB")

    # Use padding=True as suggested by the HF error message
    outputs = pipe(image, padding=True)
    print("[HF] Raw pipeline outputs:", outputs)

    if not outputs:
        raise RuntimeError("Empty predictions from Hugging Face pipeline.")

    # Take the prediction with highest score
    best = max(outputs, key=lambda o: float(o.get("score", 0.0)))

    raw_label = str(best.get("label", "Unknown"))
    score = float(best.get("score", 0.0))

    human_label = _normalize_label(raw_label)
    nutrient = _guess_nutrient_from_label(human_label)
    advice = _build_advice(human_label, nutrient, score)

    # Classification only → dummy box
    return [
        {
            "label": human_label,
            "score": round(score, 5),
            "box": [50, 50, 200, 200],
            "nutrition": nutrient,
            "advice": advice,
        }
    ]
