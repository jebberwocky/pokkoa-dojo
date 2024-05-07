import random
from http import HTTPStatus

import dashscope
from dashscope import Generation
import yaml

config = yaml.safe_load(open("dojo.yaml"))

class PokkoaDataScope:
    def __init__(self, model="qwen-turbo"):
        self.model = model
        self.model_namespace = "pokkoa.dojo.datascope"
        self.system_rule = {"role": "system",
                            "content": "你是一个只解释易经卦像的bot，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。"}
        dashscope.api_key = config["datascope"]["apikey"]

    def completion(self, prompt, temperature=0.3, top_p=0.8, presence_penalty=0, frequency_penalty=1.1):
        if frequency_penalty < 0.0:
            return " Repetition_penalty should be greater than 0.0"
        print(self.model_namespace, " with model", self.model)
        messages = [self.system_rule,
                    {'role': 'user', 'content': prompt}]
        response = Generation.call(
            model=self.model,
            messages=messages,
            # 设置随机数种子seed，如果没有设置，则随机数种子默认为1234
            seed=random.randint(1, 10000),
            temperature=temperature,
            top_p=top_p,
            repetition_penalty=frequency_penalty,
            # 将输出设置为"message"格式
            result_format='message')
        if response.status_code == HTTPStatus.OK:
            return response.output.choices[0].message.content
        else:
            return ('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            ))

