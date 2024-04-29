import csv
import hashlib
import os


def generate_hash(row, hash_length=16):
    """
    Generates a unique hash from the specified columns in a row.

    Args:
        row (list): A list representing a row in the CSV file.
        columns (list): A list of column indices to use for generating the hash.
        hash_length (int): The desired length of the shortened hash (default is 16).

    Returns:
        str: The generated hash value.
    """
    # values = [str(row[col]) for col in columns]
    combined_value = ''.join(str(value) for value in row)
    full_hash = hashlib.sha256(combined_value.encode()).hexdigest()
    return full_hash[:hash_length]

def process_csv_files(input_directory, output_directory):
    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(input_directory):
        if filename.endswith('.csv'):
            input_file = os.path.join(input_directory, filename)
            output_file = os.path.join(output_directory, f'hashed_{filename}')
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
                with open(output_file, 'w') as output_file:
                    writer = csv.writer(output_file)

                    # Write the header row with the "hashkey" column added or replaced
                    if hashkey_index is None:
                        writer.writerow(['hashkey']+header)
                    else:
                        writer.writerow([header[i] if i != hashkey_index else "hashkey" for i in range(len(header))])

                    # Process each row and generate the hash
                    for row in reader:
                        hash_value = generate_hash(row)
                        if hashkey_index is None:
                            writer.writerow([hash_value] + row)
                        else:
                            row[hashkey_index] = hash_value
                            writer.writerow(row)
            print(f"Processed file: {filename}")

directory_path = './out'
output_directory = './hashed_out'
process_csv_files(directory_path,output_directory)