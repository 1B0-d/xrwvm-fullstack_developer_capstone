"""Unit tests for emotion scoring and invalid inputs."""

import unittest
from unittest.mock import Mock, patch

import requests

from EmotionDetection.emotion_detection import emotion_detector


class EmotionDetectorTests(unittest.TestCase):
    """Exercise parsing without contacting the remote service."""

    def _mock_response(self, dominant_emotion):
        """Build a Watson-shaped response with one dominant emotion."""
        scores = {name: 0.01 for name in ("anger", "disgust", "fear", "joy", "sadness")}
        scores[dominant_emotion] = 0.90
        response = Mock()
        response.status_code = 200
        response.json.return_value = {
            "emotionPredictions": [{"emotion": scores}]
        }
        return response

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_required_statements_have_expected_dominant_emotions(self, post):
        """Check all five assignment phrases without network dependencies."""
        examples = (
            ("I am glad this happened", "joy"),
            ("I am really mad about this", "anger"),
            ("I feel disgusted just hearing about this", "disgust"),
            ("I am so sad about this", "sadness"),
            ("I am really afraid that this will happen", "fear"),
        )
        for statement, expected_emotion in examples:
            with self.subTest(statement=statement):
                post.return_value = self._mock_response(expected_emotion)
                result = emotion_detector(statement)
                self.assertEqual(result["dominant_emotion"], expected_emotion)
                self.assertAlmostEqual(result[expected_emotion], 0.90)

        self.assertEqual(post.call_count, len(examples))

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_empty_input_does_not_call_service(self, post):
        """Return the stable invalid-input shape without a network call."""
        result = emotion_detector("  ")
        self.assertIsNone(result["dominant_emotion"])
        post.assert_not_called()

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_service_bad_request_returns_empty_result(self, post):
        """Treat the service's 400 response as invalid text."""
        response = Mock(status_code=400)
        post.return_value = response
        result = emotion_detector("invalid")
        self.assertEqual(result["dominant_emotion"], None)

    @patch("EmotionDetection.emotion_detection.requests.post")
    def test_network_failure_is_visible_to_caller(self, post):
        """Leave transport failures for the Flask layer to handle."""
        post.side_effect = requests.Timeout("timeout")
        with self.assertRaises(requests.Timeout):
            emotion_detector("I am worried")


if __name__ == "__main__":
    unittest.main()
