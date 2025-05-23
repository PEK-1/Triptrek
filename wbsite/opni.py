from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())  # read local .env file

client = OpenAI(
    api_key=os.environ.get('OPENAI_API_KEY'),
)

def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [
        {
            "role": "system",
            "content": '''You are a skilled travel organizer. 
            I need your expert travel planning skills! I've got a blank slate for my upcoming trip, and 
            I want it packed with fun activities and hidden gems. But here's the twist: 
            I also need you to consider the weather conditions in each location so that my plans aren't spoiled by rain or scorching heat. 
            Can you craft the ultimate itinerary for me, making sure each day is filled with adventure and excitement while also being weather-appropriate? and
            I also don't want you to write anything after last day. not even enjoy your trip'''
        },
        {"role": "user", "content": prompt}
    ]
    
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    
    return response.choices[0].message.content

# Function to prepare the prompt based on user input data
def prepare_promp(place, visit_date, days, requirements):
    prompt = f"Plan a trip to {place} starting on {visit_date} for {days} days. "
    if requirements:
        prompt += f"Special requirements: {requirements}. "
    prompt += "Make sure to include activities that are suitable for the weather during that time."
    
    return prompt

def prepare_prompt(location, temp, time):
    prompt = f"Create a detailed plan for the remainder of the day for a visitor in {location}, considering the current temperature of {temp}°C and the local time of {time}."
    prompt+=f"Create a simple and comfortable plan for the rest of the day, including 3-4 options such as shopping, a beach visit, enjoying a delicious meal, or sightseeing—anything that can enhance their day and make it more enjoyable."
    prompt+=f"importantly- do not give the reply in bold letters"
    return prompt

# Main function to be called from views.py
def generate_itinerary(place, visit_date, days, requirements):
    prompt = prepare_promp(place, visit_date, days, requirements)
    return get_completion(prompt)

def generate_day_plan(location, temp, time):
    prompt = prepare_prompt(location,temp, time)
    return get_completion(prompt)
