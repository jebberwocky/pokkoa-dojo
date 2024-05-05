import csv
import itertools
import os
import time
import sys

from moonshot import Moonshot
from pokkoagroq import PokkoaGroq
from datascope import PokkoaDataScope

# set up Moonshot
moonshot = Moonshot()

# set up Groq
pokkoa_llama3 = PokkoaGroq("llama3-8b-8192")
pokkoa_mixtral = PokkoaGroq("mixtral-8x7b-32768")
pokkoa_gemma = PokkoaGroq("gemma-7b-it")
pokkoa_qwen = PokkoaDataScope("qwen-turbo")
pokkoa_qwen_72b = PokkoaDataScope("qwen-72b-chat")

# models
models = [moonshot,
          pokkoa_llama3,
          pokkoa_mixtral,
          pokkoa_gemma,
          pokkoa_qwen,
          pokkoa_qwen_72b]


def get_prompt_by_name(name):
    # set up the prompt
    with open("./prompts/prompt." + name + ".txt", "r") as file:
        prompt = file.read()
    return prompt.replace("\n", " ")


dojo_setup_simple = {
    "name": "simple",
    "prompt": get_prompt_by_name("simple"),
    "temperature": [0.1, 0.3, 0.5, 1],
    "top_p": [0.8],
    "presence_penalty": [2.0, 0, -2.0],
    "frequency_penalty": [2.0, 0, -2.0],
    "models": [models[5]]
}

dojo_setup_refine1 = {
    "name": "refine1",
    "prompt": get_prompt_by_name("refine1"),
    "temperature": [0.3],
    "top_p": [1.0],
    "presence_penalty": [0],
    "frequency_penalty": [0],
    "models": [moonshot,pokkoa_qwen]
}

dojo_test_set = dojo_setup_refine1

# set up the parameters
combinations = itertools.product(dojo_test_set["temperature"],
                                 dojo_test_set["top_p"],
                                 dojo_test_set["presence_penalty"],
                                 dojo_test_set["frequency_penalty"])

output = [["temperature", "top_p", "presence_penalty", "frequency_penalty", "s", "content"]]

# Define output the directory path
dir_path = "./out/" + dojo_test_set["name"] + "/"
# Check if directory exists
if not os.path.exists(dir_path):
    # Create the directory
    os.makedirs(dir_path)
    print("Directory", dir_path, "created successfully!")
else:
    print("Directory", dir_path, "already exists.")
prompt = dojo_test_set["prompt"]
print(f"dojo with prompt: {prompt}")
for running_model in dojo_test_set["models"]:
    # Test each combination
    for temperature, top_p, presence_penalty, frequency_penalty in combinations:
        # run model
        print(f"{running_model.model_namespace} with {temperature}, {top_p}, {presence_penalty}, {frequency_penalty}")
        start_time = time.time()
        content = running_model.completion(prompt,
                                           temperature,
                                           top_p,
                                           presence_penalty,
                                           frequency_penalty)
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Execution time: {elapsed_time:.6f} seconds")
        print(content)
        output.append([temperature, top_p, presence_penalty, frequency_penalty, elapsed_time, content])

    with open(dir_path + dojo_test_set["name"] + '.' + str(
            running_model.model_namespace) + '.' + running_model.model + '.data_output.csv', 'w') as f:
        write = csv.writer(f, quoting=csv.QUOTE_ALL)
        write.writerows(output)
