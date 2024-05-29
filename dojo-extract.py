from moonshot import Moonshot


def get_prompt_by_name(name):
    # set up the prompt
    with open("./prompts/prompt." + name + ".txt", "r") as file:
        prompt = file.read()
    return prompt.replace("\n", " ")

# set up Moonshot
moonshot = Moonshot()

file_path = "data_in/渊海子平.pdf"

#object_id = moonshot.uploadfile(file_path)
#file_content = moonshot.filecontent("cpbkohr5cfuldv34ipm0")
file_list = moonshot.file_list()

for file in file_list.data:
    print(file)


