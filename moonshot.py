from pathlib import Path

from openai import OpenAI
import yaml

config = yaml.safe_load(open("dojo.yaml"))


class Moonshot:
    def __init__(self,model="moonshot-v1-8k"):
        self.model = model
        self.model_namespace = "pokkoa.dojo.moonshot"
        self.system_rule = {"role": "system",
                            "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"}

        self.client = OpenAI(
            api_key=config["moonshot"]["apikey"],
            base_url="https://api.moonshot.cn/v1",
        )

    def completion(self,prompt,temperature=0.3, top_p=1.0, presence_penalty=0, frequency_penalty=0 ):
        print(self.model_namespace," with model", self.model)
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
    def completion_with_filecontent(self,prompt,content,temperature=0.3, top_p=1.0, presence_penalty=0, frequency_penalty=0 ):
        print(self.model_namespace," with model", self.model)
        prompt = prompt+" 并参考zhouyi.txt内容"
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[self.system_rule,
                      {"role":"system", "content":content},
                      {"role": "user", "content": prompt}
                      ],
            temperature=temperature,
            top_p=top_p,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty
        )
        return completion.choices[0].message.content

    def uploadfile(self,filepath):
        file_object = self.client.files.create(file=Path(filepath), purpose="file-extract")
        print("file object:", file_object)
        return file_object

#FileDeleted(id='cpbkohr5cfuldv34ipm0', deleted=True, object='file')
    def filecontent(self,file_object_id):
        file_content = self.client.files.content(file_id=file_object_id).text
        print("file content:",file_content)
        return file_content

    def file_list(self):
        file_list = self.client.files.list()
        return file_list

    def delete_file(self, id):
        r = self.client.files.delete(id)
        return r
