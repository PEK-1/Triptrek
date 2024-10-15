from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

client = OpenAI(
    api_key= os.environ.get('OPENAI_API_KEY'),

)

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages=[
    {"role": "system", "content": '''You are a skilled travel orgranized. 
     I need your expert travel planning skills! I've got a blank slate for my upcoming trip, and 
     I want it packed with fun activities and hidden gems. But here's the twist: 
     I also need you to consider the weather conditions in each location so that my plans aren't spoiled by rain or scorching heat. 
     Can you craft the ultimate itinerary for me, making sure each day is filled with adventure and excitement while also being weather-appropriate?'''},
    {"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message.content
# Get completion based on user input
prompt = input("Enter your prompt: ")
response = get_completion(prompt)
print(response)

