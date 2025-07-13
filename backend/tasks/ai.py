import openai
from django.conf import settings

client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)


def generate_task_description(title):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a productivity assistant helping users write better task descriptions."},
                {"role": "user", "content": f"Write a detailed task description for: '{title}'"}
            ],
            max_tokens=100,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"AI generation failed: {e}")
