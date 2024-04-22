from groq import Groq
import yaml

config = yaml.safe_load(open("dojo.yaml"))


class PokkoaGroq:
    def __init__(self, model="mixtral-8x7b-32768"):
        self.model = model
        self.model_namespace = "pokkoa.dojo.groq"

        self.system_rule = {"role": "system",
                            "content": "专门算周易卦象的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。 必须用使用中文回复. must response in Chinese"}

        self.client = Groq(
            api_key=config["groq"]["apikey"],
        )

    def completion(self,prompt,temperature=0.3, top_p=1.0, presence_penalty=0, frequency_penalty=0 ):
        print(self.model_namespace," with model", self.model)
        prompt += "  必须用使用中文回复! must response in Chinese"
        print("prompt:",prompt)
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
