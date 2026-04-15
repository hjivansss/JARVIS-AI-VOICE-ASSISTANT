from google import genai

client = genai.Client(api_key="AIzaSyAUAKiDGJWGRY1BI1cKzdKDV9WK_8MdYQY")

models = client.models.list()

for m in models:
    print(m.name)