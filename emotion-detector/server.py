"""Flask web interface for the Emotion Detector course project draft."""

from flask import Flask, render_template, request
import requests

from emotion_detection import emotion_detector

app = Flask(__name__)


@app.get("/")
def render_index_page():
    """Render the emotion detector form."""
    return render_template("index.html")


@app.get("/emotionDetector")
def emotion_detector_route():
    """Analyze query text and return a readable result or client error."""
    text_to_analyze = request.args.get("textToAnalyze", "")
    if not text_to_analyze.strip():
        return "Invalid text! Please try again!", 400

    try:
        result = emotion_detector(text_to_analyze)
    except (requests.RequestException, KeyError, IndexError, TypeError, ValueError):
        app.logger.exception("Emotion service request failed")
        return "Emotion analysis is temporarily unavailable. Please try again.", 502

    dominant = result.get("dominant_emotion")
    if dominant is None:
        return "Invalid text! Please try again!", 400

    emotion_names = ("anger", "disgust", "fear", "joy", "sadness")
    detail = ", ".join(f"'{name}': {result[name]}" for name in emotion_names)
    return (
        f"For the given statement, the system response is {detail}. "
        f"The dominant emotion is {dominant}."
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
