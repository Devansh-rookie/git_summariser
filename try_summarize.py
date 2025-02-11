# from llama_cpp import Llama
# import json

# # Load JSON data
# with open('files_data.json', 'r') as file:
#     data = json.load(file)

# # Initialize the LLM (adjust path to your model)
# llm = Llama(model_path="/Users/devansh/Folder_1/mymodels/ollama/sha256-dde5aa3fc5ffc17176b5e8bdc82f587b24b2678c6c66101bf7da77af9f7ccdff.gguf", n_ctx=4096) # Example: "/Users/username/models/llama-2-7b-chat.Q4_K_M.gguf"

# def summarize_file(filename, content):
#     with open("check.txt", 'a') as f:
#         f.write(f"{filename}: doing\n")
#     prompt = f"Summarize the following file, in 30 words: {filename}:\n\n{content}\n\nSummary:"
#     output = llm(prompt, max_tokens=100, stop=["Q:", "\n"], echo=False)
#     return output['choices'][0]['text'].strip()

# file_summaries = {}
# for filename, content in data.items():
#     file_summaries[filename] = summarize_file(filename, content)

# # Print the summaries

# with open('final_summaries.json', 'w') as f:
#     json.dump(file_summaries, f)

# for filename, summary in file_summaries.items():
#     print(f"File: {filename}\nSummary: {summary}\n")


# import ollama

# # Initialize the client
# client = ollama.Client()

# # Generate a response
# response = client.generate(model='llama3.2:latest', prompt='What is the capital of France?')

# print(response['response'])


# import subprocess
# import json

# def run_ollama(prompt, model='llama3.2:latest'):
#     command = ['ollama', 'run', model, prompt]
#     result = subprocess.run(command, capture_output=True, text=True)
#     return result.stdout.strip()

# # Example usage
# response = run_ollama('What is the capital of France?')
# print(response)


import ollama
import json

# Load JSON data
with open('files_data.json', 'r') as file:
    data = json.load(file)

# Initialize the Ollama client
client = ollama.Client()

def summarize_file(filename, content):
    with open("check.txt", 'a') as f:
        f.write(f"{filename}: doing\n")
    prompt = f"Summarize the following file, in 30 words and only include the actual content don't say that here is a file in 30 words I just need the actual data summary: {filename}:\n\n{content}\n\nSummary:"
    response = client.generate(model='llama3.2:latest', prompt=prompt)
    return response['response'].strip()

def summarize_the_entire_thing(content):
    content = str(content)
    prompt = f"Summarize this entire project in detail(don't give unnecessary filler words directly give the summary don't give things like: This is a JSON file): {content}:\n\nSummary"
    response = client.generate(model='llama3.2:latest', prompt=prompt)
    return response['response'].strip()

file_summaries = {}
for filename, content in data.items():
    file_summaries[filename] = summarize_file(filename, content)

# Save summaries to JSON file
with open('final_summaries.json', 'w') as f:
    json.dump(file_summaries, f)

with open('full_project.txt', 'w') as f:
    f.write(summarize_the_entire_thing(data))

# Print the summaries
for filename, summary in file_summaries.items():
    print(f"File: {filename}\nSummary: {summary}\n")
