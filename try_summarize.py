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

def create_the_summaries(data):
    file_summaries = {}
    for filename, content in data.items():
        file_summaries[filename] = summarize_file(filename, content)

    return file_summaries


if __name__ == "__main__":
    file_summaries = create_the_summaries(data)
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
