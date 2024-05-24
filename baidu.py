import os
from http import HTTPStatus

import qianfan
import yaml


config = yaml.safe_load(open("dojo.yaml"))

class PokkoaBaidu:
    def __init__(self, model="ERNIE-LITE-8K"):
        self.model = model
        self.model_namespace = "pokkoa.dojo.baidu"
        self.system_rule = {"role": "system",
                            "content": "你是一个只解释易经卦像的bot，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。"}
        os.environ["QIANFAN_ACCESS_KEY"] = config["baidu"]["all"]["acesskey"]
        os.environ["QIANFAN_SECRET_KEY"] = config["baidu"]["all"]["secretkey"]

    def completion(self, prompt, temperature=0.3, top_p=0.8, presence_penalty=0, frequency_penalty=1.1):
        print(self.model_namespace, " with model", self.model)
        messages = [
                    {'role': 'user', 'content': prompt}]
        api_key = os.environ["QIANFAN_ACCESS_KEY"]
        secret_key = os.environ["QIANFAN_SECRET_KEY"]

        chat_comp = qianfan.ChatCompletion()

        # 指定特定模型
        qfresponse = chat_comp.do(model=self.model,
                                  system=self.system_rule["content"],
                                  messages=messages,
                                  stream=False)
        if qfresponse.code == HTTPStatus.OK:
            return qfresponse.body["result"]
        else:
            return ('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                qfresponse.body["id"], qfresponse.code,
                qfresponse.code, qfresponse
            ))
