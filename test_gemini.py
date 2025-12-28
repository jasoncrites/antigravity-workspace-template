#!/usr/bin/env python3
"""
Quick test script for Gemini API access
"""
import os
import sys

def test_gemini_api():
    """Test Gemini API access with Google API key"""
    try:
        from google import genai
        from src.config import settings

        print("=" * 60)
        print("GEMINI SETUP TEST")
        print("=" * 60)

        # Check configuration
        print(f"\n✓ Model configured: {settings.GEMINI_MODEL_NAME}")
        print(f"✓ API key present: {bool(settings.GOOGLE_API_KEY)}")

        if not settings.GOOGLE_API_KEY:
            print("\n❌ ERROR: GOOGLE_API_KEY not set in .env")
            print("\nTo fix this:")
            print("1. Visit https://aistudio.google.com/app/apikey")
            print("2. Create a free API key")
            print("3. Add to .env: GOOGLE_API_KEY=your_key_here")
            return False

        # Test API connection
        print(f"\n🔄 Testing connection to {settings.GEMINI_MODEL_NAME}...")

        client = genai.Client(api_key=settings.GOOGLE_API_KEY)
        response = client.models.generate_content(
            model=settings.GEMINI_MODEL_NAME,
            contents="Say 'Hello from Gemini!' and nothing else."
        )

        print(f"✓ Response received: {response.text[:100]}")
        print("\n" + "=" * 60)
        print("SUCCESS! Gemini is working correctly.")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("\nPossible issues:")
        print("- Invalid or expired API key")
        print("- Network connectivity")
        print("- Model name incorrect")
        return False

def test_vertex_ai():
    """Test Vertex AI access with GCP credentials"""
    try:
        print("\n" + "=" * 60)
        print("TESTING VERTEX AI (Alternative)")
        print("=" * 60)

        import vertexai
        from vertexai.generative_models import GenerativeModel

        project_id = os.getenv('GOOGLE_CLOUD_PROJECT', 'truckerbooks-mvp-prod')
        location = os.getenv('GOOGLE_CLOUD_REGION', 'us-central1')

        print(f"\n✓ Project: {project_id}")
        print(f"✓ Region: {location}")

        vertexai.init(project=project_id, location=location)

        print(f"\n🔄 Testing Vertex AI Gemini...")

        model = GenerativeModel("gemini-2.0-flash-exp")
        response = model.generate_content("Say 'Hello from Vertex AI Gemini!' and nothing else.")

        print(f"✓ Response: {response.text[:100]}")
        print("\n" + "=" * 60)
        print("SUCCESS! Vertex AI Gemini is working!")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"\n❌ Vertex AI test failed: {str(e)}")
        return False

if __name__ == "__main__":
    # Try Google AI Studio first (free tier)
    success = test_gemini_api()

    # If that fails, try Vertex AI (uses GCP credentials)
    if not success:
        print("\nTrying Vertex AI as alternative...")
        test_vertex_ai()
