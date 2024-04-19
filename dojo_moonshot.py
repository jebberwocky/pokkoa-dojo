import csv
import itertools
import time

from moonshot import Moonshot

# set up Moonshot
moonshot = Moonshot()

# set up the prompt
with open("prompt.txt", "r") as file:
    prompt = file.read()

# set up the parameters
temperature = [0.1, 0.3, 0.5, 1]
top_p = [1.0]
presence_penalty = [2.0, 0, -2.0]
frequency_penalty = [2.0, 0, -2.0]
combinations = itertools.product(temperature, top_p, presence_penalty, frequency_penalty)

output = []
# Test each combination
for temperature, top_p, presence_penalty, frequency_penalty in combinations:
    # run moonshot
    print(f"Moonshot with {temperature}, {top_p}, {presence_penalty}, {frequency_penalty}")
    start_time = time.time()
    content = moonshot.completion(prompt,
                                  temperature, top_p, presence_penalty, frequency_penalty)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Execution time: {elapsed_time:.6f} seconds")
    print(content)
    output.append([temperature, top_p, presence_penalty, frequency_penalty, elapsed_time, content])

with open('./out/data_output.csv', 'w') as f:
    write = csv.writer(f, quoting=csv.QUOTE_ALL)
    write.writerows(output)
