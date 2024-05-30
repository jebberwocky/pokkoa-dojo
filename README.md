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
