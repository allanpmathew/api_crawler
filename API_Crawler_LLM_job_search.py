import openai
import json
import requests
import os

# Use environment variables for sensitive information such as API keys
openai.api_key = os.getenv('OPENAI_API_KEY')

# This function generates a response from the GPT-4 model
def generate_response(user_prompt):
    try:
        # Create a chat model completion
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user","content": user_prompt}]
        )
        
        # Check if the model has produced a choice, and if so, return its content
        if completion.choices:
            return completion.choices[0].message.content
        else:
            # If the model didn't produce a choice, return a default message
            return "Sorry, I couldn't generate a response to your prompt."
    except Exception as e:
        print(f"Exception occurred: {e}")
        return str(e)

# This function performs a job search and returns the details of the jobs found
def perform_job_search():
    try:
        url = "https://jsearch.p.rapidapi.com/search"
        querystring = {
            "query":"Sustainable finance and energy transition in cities jobs",
            "page":"1",
            "date_posted":"month"
        }
        headers = {
            "X-RapidAPI-Key": os.getenv('RAPID_API_KEY'),
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }

        # Use requests.get() for a more concise way of making a GET request
        response = requests.get(url, headers=headers, params=querystring)

        # Raise an error if the request failed
        response.raise_for_status()

        # The response is already a JSON object, so we don't need to parse it with json.loads()
        query_result = response.json()["data"]
        job_details = []

        for change in query_result:
            # Use f-string formatting for a more efficient and readable way of building the job_details string
            job_details.append({
                "job_title": change['job_title'],
                "job_description": change['job_description'],
                "job_required_skills": change['job_required_skills'],
                "job_city": change['job_city'],
                "job_state": change['job_state'],
                "job_country": change['job_country'],
                "job_latitude": change['job_latitude'],
                "job_longitude": change['job_longitude'],
                "job_min_salary": change['job_min_salary'],
                "job_max_salary": change['job_max_salary'],
                "job_google_link": change['job_google_link']
            })

        print(f"Number of jobs found: {len(job_details)}")
        return job_details
    except Exception as e:
        print(f"Exception occurred: {e}")
        return []

# Get the job list
job_list = perform_job_search()

# Create a prompt for the GPT-4 model
chat_gpt_prompt = f"""
We have found several job postings related to the course 'Sustainable finance and energy transition in cities' which was searched as it is in the job portal. Let's analyze them in depth:
"""

for job in job_list:
    chat_gpt_prompt += f"\nJob Title: {job['job_title']}\n"
    chat_gpt_prompt += f"Job Description: {job['job_description']}\n"
    chat_gpt_prompt += f"Key Skills: {job['job_required_skills']}\n"
    chat_gpt_prompt += f"Location: {job['job_city']}, {job['job_state']}, {job['job_country']}\n"
    chat_gpt_prompt += f"Location Coordinates: ({job['job_latitude']}, {job['job_longitude']})\n"
    chat_gpt_prompt += f"Salary Range: {job['job_min_salary']} - {job['job_max_salary']}\n"
    chat_gpt_prompt += f"Job Link: {job['job_google_link']}\n"
    chat_gpt_prompt += f"-------------------------------\n"

chat_gpt_prompt += """
For each job, please provide an analysis on the following aspects:
1. Job Title: What does the job title tell us about the role?
2. Description: What are the main tasks and responsibilities in this role?
3. Skills: What key skills are required? Are there any unique skills among them?
4. Location: How might the job location impact the role? Are there any noticeable trends in job locations?
5. Coordinates: How can we interpret these in the context of the job?
6. Salary: Analyze the salary range. What does this tell us about the job level and the industry standard?

Based on the analysis, let's identify the common themes and requirements across these job postings. This information will help us understand the market demand and trends related to this course module 'Sustainable finance and energy transition in cities'.

Now, based on our course 'Sustainable finance and energy transition in cities', can we come up with potential job titles that a student of this course might pursue? 

Once we have the potential job titles, let's identify key skills associated with these roles. From these key skills, let's identify the common skills across all these roles. 

Lastly, can we categorize these common skills into technical, soft, and knowledge-based skills? This categorization will provide us a clearer picture of the skillsets a student of the course needs to focus on.
"""

# Generate a response from the GPT-4 model
analysis = generate_response(chat_gpt_prompt)

print(analysis)


