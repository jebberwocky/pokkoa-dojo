import csv
import hashlib
import os
from math import ceil


def generate_hash(row, hash_length=16):
    """
    Generates a unique hash from the specified columns in a row.

    Args:
        row (list): A list representing a row in the CSV file.
        hash_length (int): The desired length of the shortened hash (default is 16).

    Returns:
        str: The generated hash value.
    """
    # values = [str(row[col]) for col in columns]
    # combined_value = ''.join(str(value) for value in row)
    combined_value = row[5]
    full_hash = hashlib.sha256(combined_value.encode()).hexdigest()
    return full_hash[:hash_length]


def check_text(text):
    """
      This function checks if a text is empty, blank, or contains a specific string.

      Args:
          text: The text to be checked.

      Returns:
          False if the text is empty, blank, or contains the specific string, True otherwise.
      """
    return not (not text or text.isspace() or "Repetition_penalty should be greater than 0.0" in text)


def split_list_n(data, n):
    """
  Splits a list into n sublists with (almost) the same number of elements.

  Args:
      data: The list to be split.
      n: The number of sublists to create.

  Returns:
      A list of sublists.
  """
    if n <= 0:
        raise ValueError("Number of sublists (n) must be positive")

    group_size = ceil(len(data) / n)  # Use ceil to ensure enough elements per sublist
    sublists = []
    for i in range(n):
        start_index = i * group_size
        end_index = min(start_index + group_size, len(data))  # Handle potential last sublist
        sublists.append(data[start_index:end_index])
    return sublists


def process_csv_files(input_directory, output_directory, output_directory_short, output_directory_human, split_n):
    os.makedirs(output_directory, exist_ok=True)
    total_count = 0
    total_elements = []
    for filename in os.listdir(input_directory):
        if filename.endswith('.csv'):
            input_file = os.path.join(input_directory, filename)
            output_file = os.path.join(output_directory, f'hashed_{filename}')
            output_file_short = os.path.join(output_directory_short, f'hashed_{filename}')
            # Open the CSV file
            with open(input_file, 'r') as file:
                reader = csv.reader(file)
                header = next(reader)  # Get the header row
                # Specify the columns to use for generating the hash
                # column_indices = [header.index('column1'), header.index('column2'), ...]
                # Check if the "hashkey" column already exists
                if "hashkey" in header:
                    hashkey_index = header.index("hashkey")
                else:
                    hashkey_index = None

                    # Create a new CSV file with the "hashkey" column
                with open(output_file, 'w') as output_file, open(output_file_short, 'w') as output_file_short:
                    writer = csv.writer(output_file)
                    writer2 = csv.writer(output_file_short)

                    # Write the header row with the "hashkey" column added or replaced
                    if hashkey_index is None:
                        writer.writerow(['hashkey'] + header)
                        writer2.writerow(['hashkey', "内容"])
                    else:
                        writer.writerow([header[i] if i != hashkey_index else "hashkey" for i in range(len(header))])
                        writer2.writerow([header[i] if i != hashkey_index else "hashkey" for i in range(len(header))])

                    # Process each row and generate the hash
                    count = 0
                    for row in reader:
                        if check_text(row[5]):
                            count = count + 1
                            hash_value = generate_hash(row)
                            if hashkey_index is None:
                                writer.writerow([hash_value] + row)
                            else:
                                row[hashkey_index] = hash_value
                                writer.writerow(row)
                            writer2.writerow([hash_value, row[5]])
                            total_elements.append([hash_value, row[5]])
                total_count = total_count + count
                print(f"Processed file: {filename}, count: {count}")

    print(f"total count: {total_count}")
    lists = split_list_n(total_elements, split_n)
    for index, l in enumerate(lists):
        output_file_short = os.path.join(output_directory_human, f'hashed_{index}.csv')
        with open(output_file_short, 'w') as output_file_short:
            writer = csv.writer(output_file_short)
            writer.writerow(['标号(请勿修改)', '分数', "内容"])
            writer.writerows(l)
            print(f"Processed file: hashed_{index}.csv, count: {len(l)}")


directory_path = './out'
output_directory = './hashed_out'
output_directory_short = './hashed_out_short'
output_directory_human = './human_dojo_text'
split_n = 3
process_csv_files(directory_path, output_directory, output_directory_short, output_directory_human, split_n)
