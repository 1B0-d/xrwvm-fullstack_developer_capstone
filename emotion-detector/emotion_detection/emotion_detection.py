"""Call the course Watson NLP emotion service and normalize its response."""

from __future__ import annotations

from typing import Any

import requests

SERVICE_URL = (
    "https://sn-watson-emotion.labs.skills.network/"
    "v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
)
MODEL_ID = "emotion_aggregated-workflow_lang_en_stock"
EMOTIONS = ("anger", "disgust", "fear", "joy", "sadness")


def _empty_result() -> dict[str, float | None]:
    """Return the stable result shape for invalid input."""
    return {**{name: None for name in EMOTIONS}, "dominant_emotion": None}


def emotion_detector(text_to_analyze: str | None) -> dict[str, Any]:
    """Return five emotion scores and their dominant label for input text.

    Empty input and the service's HTTP 400 response map to a result with
    ``None`` values. Network, HTTP, and malformed-response errors are raised
    for the Flask layer to handle explicitly.
    """
    if not isinstance(text_to_analyze, str) or not text_to_analyze.strip():
        return _empty_result()

    response = requests.post(
        SERVICE_URL,
        headers={"grpc-metadata-mm-model-id": MODEL_ID},
        json={"raw_document": {"text": text_to_analyze}},
        timeout=10,
    )
    if response.status_code == 400:
        return _empty_result()
    response.raise_for_status()

    payload = response.json()
    emotion_scores = payload["emotionPredictions"][0]["emotion"]
    scores = {name: float(emotion_scores[name]) for name in EMOTIONS}
    return {**scores, "dominant_emotion": max(scores, key=scores.get)}
