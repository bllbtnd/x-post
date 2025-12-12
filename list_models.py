import google.generativeai as genai
import os

# Configure with API key
api_key = os.environ.get('GEMINI_API_KEY')
if not api_key:
    print("Error: GEMINI_API_KEY not found in environment")
    exit(1)

genai.configure(api_key=api_key)

print("\nAvailable Gemini Models:")
print("=" * 60)

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"\nModel: {m.name}")
        print(f"Display Name: {m.display_name}")
        print(f"Input Token Limit: {m.input_token_limit:,}")
        print(f"Output Token Limit: {m.output_token_limit:,}")
