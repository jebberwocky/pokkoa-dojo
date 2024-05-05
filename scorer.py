import csv
import os
import pandas as pd

data = []
def process_csv_files(input_directory, output_directory):
    os.makedirs(output_directory, exist_ok=True)
    for filename in os.listdir(input_directory):
        if filename.endswith('.csv'):
            input_file = os.path.join(input_directory, filename)
            with open(input_file, 'r') as file:
                reader = csv.reader(file)
                header = next(reader)
                print("header:", header)
                for row in reader:
                    hash = row[0]
                    score = row[1]
                    data.append({"hashkey":hash, "score":score})

directory_path = './human_result'
ouptput_directory = './score'
process_csv_files(directory_path,ouptput_directory)
# df1
csv_file_path = './human_dojo_text/hashed_all.csv'
df1 = pd.read_csv(csv_file_path)
# df2
df2 = pd.DataFrame(data)
# merge and move column
key_column = 'hashkey'
merged_df = pd.merge(df1, df2, on=key_column, how='outer')
merged_df.insert(1, 'score', merged_df.pop('score'))
# merged_df = merged_df.sort_values(by="model")
merged_df = merged_df.sort_values(by="score",ascending=False)
merged_df.to_csv("./human_score_all/human_scored.csv")
print(merged_df)

