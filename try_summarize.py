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
import os

# Load JSON data
with open('results/files_data.json', 'r') as file:
    data = json.load(file)

# Initialize the Ollama client
client = ollama.Client()

conversation_history = [

    {"role": "user", "content": "What is the capital of France?"},

    {"role": "assistant", "content": "Paris"}

]

directory = "temp"
if not os.path.exists(directory):
    os.mkdir(directory)
with open("temp/check.txt", 'w') as f:
    pass


def summarize_file(filename, content):
    with open("temp/check.txt", 'a') as f:
        f.write(f"{filename}: doing\n")
    prompt = f"Summarize the following file, in 30 words and only include the actual content don't say that here is a file in 30 words I just need the actual data summary: {filename}:\n\n{content}\n\nSummary:"
    response = client.generate(model='llama3.2:latest', prompt=prompt)
    summary =  response['response'].strip()

    return summary

def summarize_the_entire_thing(content):
    content = str(content)
    prompt = f"Summarize this entire project in detail(don't give unnecessary filler words directly give the summary don't give things like: This is a JSON file): {content}:\n\nSummary"
    response = client.generate(model='llama3.2:latest', prompt=prompt)
    summary =  response['response'].strip()

    return summary


def get_dependencies(content):
    # Start by creating the initial conversation with a system message and the first user prompt
    messages = [
        {
            "role": "system",
            "content": "You are an assistant that specializes in analyzing code projects and providing precise library and framework dependencies."
        },
        {
            "role": "user",
            "content": f"Tell me what are the libraries and frameworks required for this project given in the JSON file: {content}"
        }
    ]

    # Get the first response based on the first prompt
    response1 = client.chat(model='llama3.2:latest', messages=messages)
    # Optionally, capture the assistant's reply
    answer1 = response1['message']['content']
    # print("First response:", answer1)

    # Append the assistant's answer to the conversation history to provide context
    messages.append({
        "role": "assistant",
        "content": answer1
    })

    # Add the second user prompt, which will now include context from the first interaction
    messages.append({
        "role": "user",
        "content": "tell me the libraries and frameworks required for this code"
    })

    # Get the response; the conversation history now contains both prompts to guide the model
    response2 = client.chat(model='llama3.2:latest', messages=messages)
    dependencies = response2['message']['content'].strip()
    print("Final dependencies:", dependencies)

    return dependencies


file_summaries = {}
for filename, content in data.items():
    file_summaries[filename] = summarize_file(filename, content)

# Save summaries to JSON file
with open('results/final_summaries.json', 'w') as f:
    json.dump(file_summaries, f)

with open('results/full_project.txt', 'w') as f:
    f.write(summarize_the_entire_thing(data))

with open('results/dependencies.txt', 'w') as f:
    f.write(get_dependencies(data))
# Print the summaries
for filename, summary in file_summaries.items():
    print(f"File: {filename}\nSummary: {summary}\n")
