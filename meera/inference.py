import os
from groq import Groq
from dotenv import load_dotenv
from typing import Any

load_dotenv()
class GroqModels:
    def __init__(self):
        self.grok_key = os.environ.get("GROQ_API_KEY")
        self.client = Groq(
            # This is the default and can be omitted
            api_key=self.grok_key
        )

    def infer(self,
              query_str:str,
              context: Any,
            model_name:str="llama-3.3-70b-versatile"
              )->str:
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "you are an extraction expect, you answer questions based on a giving context."
                },
                {
                    "role": "user",
                    "content": f"""
                    given this context: {context}
                    ANSWER this:
                    QUESTION : {query_str}
                
                    """,
                }
            ],
            model=model_name,
        )
        return chat_completion.choices[0].message.content

if __name__ == "__main__":
    groq_gateway = GroqModels()
    print(groq_gateway.infer("Hello how are you ?",context=""))