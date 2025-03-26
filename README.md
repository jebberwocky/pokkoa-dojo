# Pokkoa DOJO

![dojo](https://github.com/jebberwocky/pokkoa-dojo/blob/main/pokkoa-dojo.jpg?raw=true)

## Overview

This repository contains code for evaluating the reasoning capabilities of different large language models (LLMs) using various prompts.

## Getting Started


configure the settings in the provided configuration file - dojo.yaml

### dojo
- run dojo.py to get result fro each llms

### dojo.yaml
```
moonshot:
    apikey: --masked--
groq:
    apikey: --masked--
datascope:
    apikey: --masked--
deepseek:
    apikey: --masked--
baidu:
  pokkoa:
    apikey: --masked--
    secretkey: --masked--
  all:
    acesskey: --masked--
    secretkey: --masked--
```

### ./prompts/prompt.{name}.txt
test prompts goes here
```
Write me a python script example. 给我写诗
```

### output
```
output to ./out/{dojo name}/
```
### dojo setup
```
dojo_setup_simple = {
    "name": "simple", //dojo name
    "prompt": get_prompt_by_name("simple"), //./prompts/using prompt.simple.txt
    "temperature": [0.1, 0.3, 0.5, 1],
    "top_p": [0.8],
    "presence_penalty": [2.0, 0, -2.0],
    "frequency_penalty": [2.0, 0, -2.0],
    "models": [moonshot,pokkoa_qwen]
}
```

### util/character.py
```
class GPTToneConfig:
    def __init__(self, name, temperature, top_p, frequency_penalty=0, presence_penalty=0):
        self.name = name
        self.temperature = temperature
        self.top_p = top_p
        self.frequency_penalty = frequency_penalty
        self.presence_penalty = presence_penalty

    def __str__(self):
        return f"{self.name}: Temperature: {self.temperature}, Top-p: {self.top_p}, Frequency Penalty: {self.frequency_penalty}, Presence Penalty: {self.presence_penalty}"

class Character:
    def __init__(self, name, role, personality, tone_config, prompt):
        self.name = name
        self.role = role
        self.personality = personality
        self.tone_config = tone_config
        self.prompt = prompt

    def __str__(self):
        return f"角色: {self.name} ({self.role})\n性格: {self.personality}\n语气设置: {self.tone_config}\n提示词: {self.prompt}"

# 定义语气设置
encouraging = GPTToneConfig("鼓励", temperature=0.8, top_p=0.9, frequency_penalty=0.4, presence_penalty=0.3)

default = Character(
    "预设",
    "你是一个只解释易经卦像的bot",
    "你是一个只解释易经卦像的bot",
    encouraging,
    "你是一个只解释易经卦像的bot"
)

characters = [default]
```

### run huamn scoring
- make sure setup the prompt_name in hasher.py and scorer.py
- run hasher.py to create csv files for scoring
- ./human_dojo_text contains scorable csv files
- put scored csv files in ./human_result
- run scorer.py to get complete scoring

## Reference
- https://help.aliyun.com/zh/dashscope/developer-reference/model-square/?spm=a2c4g.11186623.0.0.b0909b6e8qemG9

## Contact
liuzhiyuan@pokkoa.cc

## Open Dataset
- 🤗 https://huggingface.co/pokkoa
