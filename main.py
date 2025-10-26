import os
from openai import OpenAI
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", "")
client = OpenAI()
# List models (lightweight metadata call; fails fast if key invalid)
models = client.models.list()
for model in models.data:
    print("Model ID:", model.id)
print("OK: OpenAI reachable, model count:", len(models.data))