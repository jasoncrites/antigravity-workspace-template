"""
Vertex AI Gemini wrapper to work alongside google.genai
"""
import os
import vertexai
from vertexai.generative_models import GenerativeModel


class VertexGeminiClient:
    """
    Wrapper to make Vertex AI Gemini compatible with google.genai.Client interface
    """

    def __init__(self, project_id=None, location=None):
        self.project_id = project_id or os.getenv('GOOGLE_CLOUD_PROJECT', 'truckerbooks-mvp-prod')
        self.location = location or os.getenv('GOOGLE_CLOUD_REGION', 'us-central1')

        vertexai.init(project=self.project_id, location=self.location)
        self.models = self._Models()

    class _Models:
        def generate_content(self, model, contents):
            """Generate content using Vertex AI Gemini"""
            # Convert model name to Vertex AI format
            vertex_model = GenerativeModel(model)
            response = vertex_model.generate_content(contents)

            # Wrap response to match genai.Client interface
            class _Response:
                def __init__(self, text):
                    self.text = text

            return _Response(response.text)


def get_gemini_client():
    """
    Get a Gemini client, preferring Google AI Studio but falling back to Vertex AI
    """
    from src.config import settings

    # Try Google AI Studio first (requires API key)
    if settings.GOOGLE_API_KEY and settings.GOOGLE_API_KEY != "your_api_key_here":
        try:
            from google import genai
            return genai.Client(api_key=settings.GOOGLE_API_KEY)
        except Exception as e:
            print(f"⚠️ Failed to init Google AI Studio client: {e}")

    # Fall back to Vertex AI (uses GCP credentials)
    print("🔄 Using Vertex AI Gemini (via GCP credentials)")
    return VertexGeminiClient()
