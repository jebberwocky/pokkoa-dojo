import csv
import itertools
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

running_model = models[5]

# set up the prompt
with open("prompt.txt", "r") as file:
    prompt = file.read()

# set up the parameters
temperature = [0.1, 0.3, 0.5, 1]
top_p = [0.8]
presence_penalty = [2.0, 0, -2.0]
frequency_penalty = [2.0, 0, -2.0]
combinations = itertools.product(temperature, top_p, presence_penalty, frequency_penalty)

output = [["temperature", "top_p", "presence_penalty", "frequency_penalty", "s", "content"]]
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

with open('./out/'+str(running_model.model_namespace)+'.'+running_model.model+'.data_output.csv', 'w') as f:
    write = csv.writer(f, quoting=csv.QUOTE_ALL)
    write.writerows(output)
