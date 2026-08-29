import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found")
    exit()

print("API key found.")
print("Creating Gemini client...")

client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(
        timeout=30000
    )
)

models_to_try = [
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite"
]

for model_name in models_to_try:

    print("\n--------------------------------")
    print("Trying:", model_name)
    print("--------------------------------")

    try:

        response = client.models.generate_content(
            model=model_name,
            contents="Say hello in one short sentence.",
            config=types.GenerateContentConfig(
                thinking_config=types.ThinkingConfig(
                    thinking_level="low"
                ),
                max_output_tokens=100
            )
        )

        if response.text:

            print("\nSUCCESS!")
            print("Model:", model_name)
            print("Response:", response.text)

            break

    except Exception as e:

        print("FAILED")
        print("Error:", type(e).__name__)
        print(str(e))

else:

    print("\n================================")
    print("ALL MODELS FAILED")
    print("================================")
    print("Gemini is currently unavailable.")
    print("Your API key was detected successfully.")