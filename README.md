# Pokkoa DOJO

## Overview

This repository contains code for fine-tuning a pre-trained GPT (Generative Pre-trained Transformer) model on a specific dataset or task.

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
