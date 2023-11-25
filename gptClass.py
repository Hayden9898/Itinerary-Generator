from openai import OpenAI

"""
To run:
pip install openai

"""

client = OpenAI(api_key="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",
                organization="org-XFRiKEA3bXXTSifH2T4XNFwX")


def stream(message: str, model: str):
  stream = client.chat.completions.create(
    model=model,
    messages = [
      {"role": "system", "content": "You are an AI assistant. You will answer questions, and you are an expert writer."},
      {"role": "user", "content": message},
    ],
    stream=True,
  )
  for part in stream:
    print(part.choices[0].delta.content or "", end="")

stream(message="what is love?", model="gpt-4-1106-preview")