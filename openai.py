from openai import OpenAI

client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)
try:
        completion = client.chat.completions.create(
            model="deepseek/deepseek-r1:free",
            messages=[
                {"role": "system", "content": "You are Rafiul.A Data science enthusiastic"},
                {"role": "user", "content": }
            ]
        )
        print(completion.choices[0].message.content)
    except Exception as e:
        print("System error: Neural bridge unstable.)