from openai import OpenAI
import yaml

config = yaml.safe_load(open("dojo.yaml"))


class PokkoaDeepSeek:
    def __init__(self, model="deepseek-chat"):
        self.model = model
        self.model_namespace = "pokkoa.dojo.deepseek"
        self.system_rule = {"role": "system",
                            "content": "你是一个只解释易经卦像的bot，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。"}

        self.client = OpenAI(
            api_key=config["deepseek"]["apikey"],
            base_url="https://api.deepseek.com/",
        )

    def completion(self, prompt, temperature=0.3, top_p=1.0, presence_penalty=0, frequency_penalty=0):
        print(self.model_namespace, " with model", self.model)
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[self.system_rule, {"role": "user", "content": prompt}
                          ],
                temperature=temperature,
                top_p=top_p,
                presence_penalty=presence_penalty,
                frequency_penalty=frequency_penalty
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"An error occurred: {e}"

