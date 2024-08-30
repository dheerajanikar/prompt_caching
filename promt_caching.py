import anthropic
import os


# Set your API key
os.environ["ANTHROPIC_API_KEY"] = ""

client = anthropic.Anthropic(
    api_key = os.environ["ANTHROPIC_API_KEY"]
)

# Load the paper content from a file

try:
    with open('llama3_1.txt', 'r', encoding='utf-8', errors='ignore') as file:
        paper_content = file.read()
except UnicodeDecodeError:
    # If UTF-8 fails, try reading with 'latin-1' encoding
    with open('llama3_1.txt', 'r', encoding='latin-1') as file:
        paper_content = file.read()



system_messages = [
        {
                "type": "text",
                "text": "You are an AI assistant specializing in explaining the Llama 3.1 paper."
        },
        {
                "type": "text",
                "text": f"Here's the full text of the Llama 3.1 paper:\n\n{paper_content}",
                "cache_control": {"type": "ephemeral"}
        } 
]

messages = [
    {
        "role": "user",
        "content": "Provide a brief summary of the key points in this paper."
    }
]

print("Chat about Llama 3.1 paper. Type 'quit' to exit.")


while True:
    try:
        response = client.beta.prompt_caching.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=2048,  # Increased token limit
            system=system_messages,
            messages=messages
        )

        if response.content:
            ai_response = response.content[0].text
            print("\nAI:", ai_response)
            messages.append({"role": "assistant", "content": ai_response})
        else:
            print("\nAI: No response received.")

    except anthropic.APIError as e:
        print(f"An error occurred: {e}")
        continue

    # Get user input
    user_input = input("\nYou: ")

    if user_input.lower() == 'quit':
        break

    messages.append({"role": "user", "content": user_input})

print("Chat ended.")