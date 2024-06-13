import json
json_file_path = './history.json'
output_file_path = './history_1000.json'
def print_first_two_dicts(json_file_path):
    with open(json_file_path, 'r') as file:
        data = json.load(file)
    # Assuming data is a list of dictionaries
    with open(output_file_path, 'w') as output_file:
        json.dump(data[:1000],output_file, indent=4)

# Replace 'your_json_file.json' with your actual JSON file path
if __name__ == '__main__':
    print_first_two_dicts(json_file_path)