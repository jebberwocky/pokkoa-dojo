import json
from datetime import datetime
from moonshot import Moonshot

moonshot = Moonshot()
running_model = moonshot
prompt_text_file = 'prompt2'
output_directory = './out'


def safe_concat_fields(data, fields):
    """Efficiently concatenate existing fields from the data dictionary."""
    return " ".join(
        ", ".join(map(str, data[key])) if isinstance(data[key], list)
        else str(data[key])
        for key in fields if key in data
    )


def replace_template(filename, replacements):
    """Read template and replace placeholders with values."""
    with open(filename, 'r', encoding='utf-8') as file:
        template = file.read()

    fields_to_concat = ["特殊标签", "运势", "问题", "不存在的字段", "建议优先级", "需要注意的领域"]

    return template.format(
        chineseZodiac=replacements.get("chineseZodiac", ""),
        keypoints=safe_concat_fields(replacements, fields_to_concat)
    )


def main():
    """Main function to process zodiac predictions."""
    with open('zodiac-predictions.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    for key, value in data.items():
        if 'metadata' not in key:
            result = replace_template(prompt_text_file+".txt", value)
            print(result)
            content = running_model.completion(result)
            #print("\n\n")
            #print(content)
            #print("\n\n")
            # Generate timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            # Construct the filename
            filename = f"{output_directory}/{value['chineseZodiac']}_{prompt_text_file}_{timestamp}.txt"
            # Save the content to the file
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
                print("write file:", filename)

if __name__ == "__main__":
    main()