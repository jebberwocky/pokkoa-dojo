import csv
import itertools
import os
import time

from deepseek import PokkoaDeepSeek
from moonshot import Moonshot
from pokkoagroq import PokkoaGroq
from datascope import PokkoaDataScope
from baidu import PokkoaBaidu
from util.character import boyfriend,default_calendar, characters,default, motivational_sister, best_friend, therapist, poison_tongue,straightforwardrobot,cbttherapist,mindfulnesshealer
from util.prompt import get_prompt_by_name, get_prompt_by_name_character

# set up Moonshot
moonshot = Moonshot()

# set up Groq
pokkoa_llama3 = PokkoaGroq("llama3-8b-8192")
pokkoa_mixtral = PokkoaGroq("mixtral-8x7b-32768")
pokkoa_gemma = PokkoaGroq("gemma-7b-it")
pokkoa_qwen = PokkoaDataScope("qwen-turbo")
pokkoa_qwen_72b = PokkoaDataScope("qwen-72b-chat")
pokkoa_dataScopeDeepseek = PokkoaDataScope("deepseek-v3")
pokkoa_deepseek = PokkoaDeepSeek("deepseek-chat")
pokkoa_baidu = PokkoaBaidu("ERNIE-Lite-8K-0922")
pokkoa_qwen_baize = PokkoaDataScope("qwen2-7b-instruct-lora-ft-202502071835-caf2")

# models
models = [moonshot,
          pokkoa_llama3,
          pokkoa_mixtral,
          pokkoa_gemma,
          pokkoa_qwen,
          pokkoa_qwen_72b,
          pokkoa_deepseek,
          pokkoa_dataScopeDeepseek
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
for character in [straightforwardrobot]:
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

dojo_setup_robot2 = {
    "name": "straightforwardRobot2",
    "prompt": get_prompt_by_name("straightforwardRobot2"),
    "temperature": [0.3],
    "top_p": [0.9],
    "presence_penalty": [0],
    "frequency_penalty": [0],
    "models": [moonshot, pokkoa_deepseek, pokkoa_qwen, pokkoa_baidu],
    "character":straightforwardrobot
}

dojo_setup_robot3 = {
    "name": "straightforwardRobot3",
    "prompt": get_prompt_by_name("straightforwardRobot3"),
    "temperature": [0.3],
    "top_p": [0.9],
    "presence_penalty": [0],
    "frequency_penalty": [0],
    "models": [moonshot, pokkoa_deepseek, pokkoa_qwen, pokkoa_baidu],
    "character":straightforwardrobot
}
dojo_character_robot = []
#for character in [straightforwardrobot]:
#    dojo_character_robot.append(character_to_params(character, "straightforwardRobot",  [moonshot, pokkoa_deepseek, pokkoa_qwen, pokkoa_baidu]))

dojo_character_cbtrobot = []
for character in [cbttherapist]:
    dojo_character_cbtrobot.append(character_to_params(character, "refine3",  [moonshot, pokkoa_deepseek, pokkoa_qwen, pokkoa_baidu]))


dojo_daily_test_bot = []
for character in [default_calendar]:
    dojo_daily_test_bot.append(character_to_params(character, "choicemaker",  [moonshot, pokkoa_deepseek, pokkoa_qwen, pokkoa_baidu]))

dojo_setup_refine7 = []
for character in [default, motivational_sister, best_friend, therapist, poison_tongue,straightforwardrobot,cbttherapist]:
    dojo_setup_refine7.append(character_to_params(character, "refine7",  [moonshot, pokkoa_deepseek, pokkoa_qwen, pokkoa_baidu]))

dojo_setup_refine7_2 = []
for character in [default, motivational_sister, best_friend, therapist, poison_tongue,straightforwardrobot,cbttherapist]:
    dojo_setup_refine7_2.append(character_to_params(character, "refine7_2",  [moonshot, pokkoa_deepseek, pokkoa_qwen, pokkoa_baidu]))

dojo_setup_refine7_3 = []
for character in [default, motivational_sister, best_friend, therapist, poison_tongue,straightforwardrobot,cbttherapist]:
    dojo_setup_refine7_3.append(character_to_params(character, "refine7_3",  [moonshot, pokkoa_deepseek, pokkoa_qwen, pokkoa_baidu]))

dojo_setup_refine7_4 = []
for character in [default, motivational_sister, best_friend, therapist, poison_tongue,straightforwardrobot,cbttherapist]:
    dojo_setup_refine7_4.append(character_to_params(character, "refine7_4",  [moonshot, pokkoa_deepseek, pokkoa_qwen, pokkoa_baidu]))

dojo_setup_refine8_0 = []
for character in [default, motivational_sister, best_friend, therapist, poison_tongue,straightforwardrobot,cbttherapist]:
    dojo_setup_refine8_0.append(character_to_params(character, "refine8_0",  [moonshot, pokkoa_deepseek, pokkoa_qwen, pokkoa_baidu]))

dojo_setup_refine8_1 = []
for character in [default, motivational_sister, best_friend, therapist, poison_tongue,straightforwardrobot,cbttherapist]:
    dojo_setup_refine8_1.append(character_to_params(character, "refine8_1",  [moonshot, pokkoa_deepseek, pokkoa_qwen, pokkoa_baidu]))


dojo_setup_refine8_0_qwen_baize = []
for character in [default, straightforwardrobot]:
    dojo_setup_refine8_0_qwen_baize.append(character_to_params(character, "refine8_0",  [pokkoa_qwen_baize]))


dojo_character_mindfulnesshealert = []
for character in [mindfulnesshealer]:
    dojo_character_mindfulnesshealert.append(character_to_params(character, "refine3",  [moonshot, pokkoa_deepseek, pokkoa_qwen, pokkoa_baidu]))

dojo_moonshot_debug = []
for character in [default]:
    dojo_moonshot_debug.append(character_to_params(character, "debug",[moonshot]))

dojo_shorten = []
for character in [default]:
    dojo_shorten.append(character_to_params(character, "refine8_1_shorten",[moonshot, pokkoa_deepseek, pokkoa_qwen, pokkoa_baidu]))


dojo_calendar = []
for character in [default]:
    dojo_calendar.append(character_to_params(character, "daily.personal.simple0",[moonshot]))

dojo_pre_simple = []
for character in [default]:
    dojo_pre_simple.append(character_to_params(character, "pre.simple",[moonshot, pokkoa_deepseek, pokkoa_qwen, pokkoa_baidu]))

dojo_pre_simple2 = []
for character in [default]:
    dojo_pre_simple2.append(character_to_params(character, "pre.simple2",[moonshot, pokkoa_deepseek, pokkoa_qwen, pokkoa_baidu]))

dojo_pre_simple3 = []
for character in [default]:
    dojo_pre_simple3.append(character_to_params(character, "pre.simple3",[moonshot, pokkoa_deepseek, pokkoa_qwen, pokkoa_baidu]))

dojo_setup_refine9_datascope_deepseek = []
for character in [default]:
    dojo_setup_refine9_datascope_deepseek.append(character_to_params(character, "refine9_0",[pokkoa_dataScopeDeepseek,moonshot, pokkoa_deepseek, pokkoa_qwen, pokkoa_qwen_baize]))

dojo_calendar_personal = []
for character in [default]:
    dojo_calendar_personal.append(character_to_params(character, "daily.personal.simple2",[pokkoa_dataScopeDeepseek,moonshot, pokkoa_deepseek, pokkoa_qwen, pokkoa_qwen_baize]))

dojo_setup_refinex_0 = []
for character in [default, motivational_sister, best_friend, therapist, poison_tongue,straightforwardrobot,cbttherapist]:
    dojo_setup_refinex_0.append(character_to_params(character, "refinex_0",  [moonshot, pokkoa_deepseek, pokkoa_qwen, pokkoa_baidu]))


dojo_setup_wylq = []
for character in [default]:
    dojo_setup_wylq.append(character_to_params(character, "wylq0",  [moonshot, pokkoa_deepseek, pokkoa_qwen, pokkoa_baidu]))


running_dojo = dojo_setup_wylq#dojo_setup_refine9_datascope_deepseek#dojo_setup_refine8_0_qwen_baize# dojo_pre_simple3

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


for test_case in running_dojo:# dojo_setup_refine8_1:# dojo_moonshot_debug:# dojo_setup_refine8_0:# dojo_setup_refine7_4:# dojo_character_mindfulnesshealert:#dojo_setup_refine7_3:# dojo_character_refine3s:# dojo_character_cbtrobot:#dojo_daily_test_bot:#dojo_character_robot:# dojo_character_refine3s:
    run_dojo_test(test_case)
