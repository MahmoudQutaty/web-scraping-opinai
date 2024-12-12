from dotenv import load_dotenv
import os
import openai


load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Function to generate a chatbot response based on scraped data and user input
def create_chatbot_response(scraped_data, user_input):
    messages = [
        {"role": "system", "content": "You are an assistant that provides concise and accurate responses."},
        {"role": "user", "content": f"Here is some information scraped from a website: {scraped_data}\n\nUser Question: {user_input}"}
    ]

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Updated to a conversational model
            messages=messages,
            max_tokens=200,  # Increase token limit for longer responses
            temperature=0.7
        )
        answer = response['choices'][0]['message']['content'].strip()
        return answer
    except Exception as e:
        return f"Error generating chatbot response: {e}"
