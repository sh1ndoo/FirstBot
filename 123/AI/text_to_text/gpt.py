
from g4f.client import AsyncClient
from g4f.Provider import Blackbox, Airforce, ChatGptEs, PollinationsAI

def gpt(msg: list, img=None):
  client = AsyncClient()
  response = client.chat.completions.create(
      model="gpt-4o",
      messages=msg,
      web_search = True,
      provider=Blackbox,
      image=img
  )
  return response


def trim_history(history, max_length=4096):
  current_length = sum(len(message["content"]) for message in history)
  print(current_length)
  while history and current_length > max_length:
    removed_message = history.pop(1)
    current_length -= len(removed_message["content"])
  return history


def image_gen(msg, model):
    print(model)
    client = AsyncClient()
    response = client.images.generate(
        model=model,
        provider=PollinationsAI,
        prompt=msg,
        response_format="url"
    )

    return response





