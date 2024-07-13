import csv
import itertools
import os
import time

from deepseek import PokkoaDeepSeek
from moonshot import Moonshot
from pokkoagroq import PokkoaGroq
from datascope import PokkoaDataScope
from baidu import PokkoaBaidu
from util.character import boyfriend, characters, motivational_sister, best_friend, therapist, poison_tongue
from util.prompt import get_prompt_by_name, get_prompt_by_name_character

# set up Moonshot
moonshot = Moonshot()

# set up Groq
pokkoa_llama3 = PokkoaGroq("llama3-8b-8192")
pokkoa_mixtral = PokkoaGroq("mixtral-8x7b-32768")
pokkoa_gemma = PokkoaGroq("gemma-7b-it")
pokkoa_qwen = PokkoaDataScope("qwen-turbo")
pokkoa_qwen_72b = PokkoaDataScope("qwen-72b-chat")
pokkoa_deepseek = PokkoaDeepSeek("deepseek-chat")
pokkoa_baidu = PokkoaBaidu("ERNIE-LITE-8K")

# models
models = [moonshot,
          pokkoa_llama3,
          pokkoa_mixtral,
          pokkoa_gemma,
          pokkoa_qwen,
          pokkoa_qwen_72b,
          pokkoa_deepseek
          ]


def character_to_params(character, name, models):
    return {
        "name": name,
        "prompt": get_prompt_by_name_character(name, character),
        "temperature": [character.tone_config.temperature],
        "top_p": [character.tone_config.top_p],
        "presence_penalty": [character.tone_config.presence_penalty],
        "frequency_penalty": [character.tone_config.frequency_penalty],
        "models": models,
        "character": character
    }


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
    "top_p": [0.9],
    "presence_penalty": [0],
    "frequency_penalty": [0],
    "models": [moonshot, pokkoa_deepseek]
}

dojo_setup_refine1_pokkoa_qwen = {
    "name": "refine1",
    "prompt": get_prompt_by_name("refine1"),
    "temperature": [0.3],
    "top_p": [0.9],
    "presence_penalty": [0],
    "frequency_penalty": [0],
    "models": [pokkoa_qwen]
}

dojo_setup_simple_deepseek = {
    "name": "simple",
    "prompt": get_prompt_by_name("simple"),
    "temperature": [0.3],
    "top_p": [0.9],
    "presence_penalty": [0],
    "frequency_penalty": [0],
    "models": [pokkoa_deepseek]
}

dojo_setup_refine1_baidu = {
    "name": "refine1",
    "prompt": get_prompt_by_name("refine1"),
    "temperature": [0.3],
    "top_p": [0.9],
    "presence_penalty": [0],
    "frequency_penalty": [0],
    "models": [pokkoa_baidu]
}

dojo_setup_refine3 = {
    "name": "refine3",
    "prompt": get_prompt_by_name("refine3"),
    "temperature": [0.3],
    "top_p": [0.9],
    "presence_penalty": [0],
    "frequency_penalty": [0],
    "models": [moonshot, pokkoa_deepseek, pokkoa_qwen, pokkoa_baidu]
}

dojo_character_refine3 = character_to_params(boyfriend, "refine3",
                                             [moonshot, pokkoa_deepseek, pokkoa_qwen, pokkoa_baidu])

dojo_character_refine3s = []
for character in [motivational_sister, best_friend, therapist,poison_tongue]:
    dojo_character_refine3s.append(character_to_params(character, "refine3",  [moonshot, pokkoa_deepseek, pokkoa_qwen, pokkoa_baidu]))


dojo_setup_robot = {
    "name": "straightforwardRobot",
    "prompt": get_prompt_by_name("straightforwardRobot"),
    "temperature": [0.3],
    "top_p": [0.9],
    "presence_penalty": [0],
    "frequency_penalty": [0],
    "models": [moonshot, pokkoa_deepseek, pokkoa_qwen, pokkoa_baidu]
}
dojo_character_robot = []
for character in [poison_tongue]:
    dojo_character_robot.append(character_to_params(character, "straightforwardRobot",  [moonshot, pokkoa_deepseek, pokkoa_qwen, pokkoa_baidu]))


# dojo_test_set = dojo_setup_refine1_baidu#dojo_setup_refine3#dojo_setup_refine1_baidu#dojo_setup_refine1
def run_dojo_test(dojo_test_set):
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
        output = [["temperature", "top_p", "presence_penalty", "frequency_penalty", "s", "content"]]
        # set up the parameters
        combinations = itertools.product(dojo_test_set["temperature"],
                                         dojo_test_set["top_p"],
                                         dojo_test_set["presence_penalty"],
                                         dojo_test_set["frequency_penalty"])

        for temperature, top_p, presence_penalty, frequency_penalty in combinations:
            # run model
            print(
                f"{dojo_test_set['character']},{running_model.model_namespace} with {temperature}, {top_p}, {presence_penalty}, {frequency_penalty}")
            start_time = time.time()
            content = running_model.completion(prompt,
                                               temperature,
                                               top_p,
                                               presence_penalty,
                                               frequency_penalty)

            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Execution time: {elapsed_time:.6f} seconds")
            print(content.replace("\n", " "))
            output.append([temperature, top_p, presence_penalty, frequency_penalty, elapsed_time, content])
        print("done with:" + running_model.model_namespace)

        with open(f"{dir_path}{dojo_test_set['character'].name}."
                  f"{dojo_test_set['name']}."
                  f"{running_model.model_namespace}."
                  f"{running_model.model}.data_output.csv", 'w') as f:
            write = csv.writer(f, quoting=csv.QUOTE_ALL)
            write.writerows(output)


for test_case in dojo_character_robot:# dojo_character_refine3s:
    run_dojo_test(test_case)
