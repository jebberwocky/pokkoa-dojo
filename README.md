# Pokkoa DOJO

## Overview

The code in this repository provides a framework for loading a pre-trained GPT model, preprocessing and preparing a dataset, and fine-tuning the model on the provided data. The fine-tuned model can then be saved and used for various natural language processing tasks, such as text generation, summarization, or question answering, tailored to the domain or task it was fine-tuned on.

## Getting Started


configure the fine-tuning settings in the provided configuration file

### dojo
- run dojo.py to get result fro each llms

### output
output to ./out

### dojo.yaml
```
moonshot:
    apikey: --masked--
groq:
    apikey: --masked--
datascope
    apikey: --masked--
```
### prompt.txt
test prompt goes here
```
Write me a python script example. 给我写诗
```

### run huamn scoring
- run hasher.py to create csv files for scoring
- ./human_dojo_text contains scorable csv files
- put scored csv files in ./human_result
- run scorer.py to get complete scoring

## Reference
- https://help.aliyun.com/zh/dashscope/developer-reference/model-square/?spm=a2c4g.11186623.0.0.b0909b6e8qemG9

## Contact
liuzhiyuan@pokkoa.cc