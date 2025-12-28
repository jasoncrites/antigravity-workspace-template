#!/usr/bin/env python3
"""
Test the full agent with Gemini via Vertex AI
"""
import sys
import os

# Test that the agent works end-to-end
def test_agent():
    print("=" * 60)
    print("TESTING FULL AGENT WITH GEMINI")
    print("=" * 60)

    try:
        from src.agent import GeminiAgent

        print("\n✓ Importing agent...")
        agent = GeminiAgent()

        print("\n✓ Agent initialized successfully")
        print(f"  - Tools discovered: {len(agent.available_tools)}")
        print(f"  - Model: {agent.settings.GEMINI_MODEL_NAME}")

        # Test a simple query
        print("\n🔄 Testing agent with a simple task...")
        print("   Task: 'What is 2 + 2? Just give me the number.'")

        response = agent.think("What is 2 + 2? Just give me the number.")

        print(f"\n✓ Agent response: {response[:200]}")

        print("\n" + "=" * 60)
        print("SUCCESS! Agent is fully operational with Gemini")
        print("=" * 60)
        return True

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_agent()
