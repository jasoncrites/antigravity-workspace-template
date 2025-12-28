#!/usr/bin/env python3
"""
Quick Gemini CLI Demo
"""
import vertexai
from vertexai.generative_models import GenerativeModel

def main():
    print("=" * 60)
    print("GEMINI 2.0 FLASH CLI - READY TO USE")
    print("=" * 60)
    print("\n✓ Using: gemini-2.0-flash-exp via Vertex AI")
    print("✓ Project: truckerbooks-mvp-prod")
    print("✓ Region: us-central1")
    print("\nType 'exit' to quit\n")

    # Initialize Vertex AI
    vertexai.init(project="truckerbooks-mvp-prod", location="us-central1")
    model = GenerativeModel("gemini-2.0-flash-exp")

    while True:
        try:
            # Get user input
            user_input = input("\n🤖 You: ")

            if user_input.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Goodbye!")
                break

            if not user_input.strip():
                continue

            # Generate response
            print("\n💭 Gemini: ", end='', flush=True)
            response = model.generate_content(user_input)
            print(response.text)

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
