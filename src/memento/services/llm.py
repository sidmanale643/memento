from memento.config import config
from openai import OpenAI
from .prompts import summarise_prompt


class LlmFactory:
    def __init__(self):
        
        self.model = config.default_model   
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key= config.OPEN_ROUTER_API_KEY,
            )

    def generate(self, messages, tools=None):

        payload = {
            "messages": messages,
            "model": self.model,
            # "extra_body": {"reasoning": {"enabled": True}},
        }
        if tools:
            payload["tools"] = tools
            payload["tool_choice"] = "auto"

        response = self.client.chat.completions.create(**payload)
        message = response.choices[0].message

        if message.tool_calls:
            return message
        
        return message.content or ""
    
    def summarise(self, text):
        
        messages = [{'role': 'system', 'content': summarise_prompt}, {'role': 'user', 'content': text}]
        payload = {
            "messages": messages,
            "model": self.model,
        }
        response = self.client.chat.completions.create(**payload)
        return response.choices[0].message.content or ""
            
    def extract(self, text):
        
        messages = [{'role': 'system', 'content': "extraction"}, {'role': 'user', 'content': text}]
        payload = {
            "messages": messages,
            "model": self.model,
            
        }
        response = self.client.chat.completions.create(**payload)
        return response.choices[0].message.content or ""
    
