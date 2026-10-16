
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

key = os.getenv("GROQ_API_KEY")
model = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

if not key:
    print("ERROR: GROQ_API_KEY was not found in .env")
else:
    try:
        client = Groq(api_key=key, timeout=20)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": "Reply with: Groq connection works!"
                }
            ],
            max_completion_tokens=100,
        )
        print("SUCCESS:", response.choices[0].message.content)

    except Exception as e:
        print("ERROR TYPE:", type(e).__name__)
        print("ERROR DETAILS:", str(e))
