def get_prompt_by_name(name):
    # set up the prompt
    with open("./prompts/prompt." + name + ".txt", "r") as file:
        prompt = file.read()
    return prompt.replace("\n", " ")

def get_prompt_by_name_character(name,character):
    # set up the prompt
    with open("./prompts/prompt." + name + ".txt", "r") as file:
        prompt = file.read()
        # Check if character is not "预设" and not empty
    if character and character.name != "预设":
        prompt = character.prompt + " " +prompt
    return prompt.replace("\n", " ")