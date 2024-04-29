# Pokkoa DOJO

# GPT Fine-Tuning

This repository contains code for fine-tuning a pre-trained GPT (Generative Pre-trained Transformer) model on a specific dataset or task. Fine-tuning involves further training a pre-trained language model on a targeted dataset, allowing it to adapt and specialize for a particular domain or task.

## Overview

The code in this repository provides a framework for loading a pre-trained GPT model, preprocessing and preparing a dataset, and fine-tuning the model on the provided data. The fine-tuned model can then be saved and used for various natural language processing tasks, such as text generation, summarization, or question answering, tailored to the domain or task it was fine-tuned on.

## Features
TODO

## Getting Started


configure the fine-tuning settings in the provided configuration file
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
Write me a python script example 
```

## Reference
- https://help.aliyun.com/zh/dashscope/developer-reference/model-square/?spm=a2c4g.11186623.0.0.b0909b6e8qemG9

## Contact
liuzhiyuan@pokkoa.cc