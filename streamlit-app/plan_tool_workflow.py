import openai
import streamlit as st

class ToolAgent:
    def __init__(self):
        # api key present in streamlit secrets 
        openai.api_key = st.secrets["openai"]["api_key"]

    def execute(self, sub_task):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a knowledgeable assistant."}, # letting the ai know its roll 
                    {"role": "user", "content": sub_task}
                ],
                max_tokens=100,       
                temperature=0.7       # to control randomness 
            )

            return response.choices[0].message['content'].strip()
        except Exception as e:
            return f"Error executing sub-task: {str(e)}"

class PlanAgent:
    def __init__(self):
        pass

    def split(self, query):
        # splitting the user query into sub-tasks using basic NLP sentence tokenozation logic 
        sub_tasks = query.split('. ')
        return [task.strip() for task in sub_tasks if task.strip()]

    def refine(self, sub_task, answer):
        # checking the quality of response 
        quality = self.analyze_quality(answer)
        
        if quality == "good":
            return f"{sub_task} (Refined with positive feedback: {answer})"
        elif quality == "less_information":
            new_task = f"{sub_task}. Please provide more details or examples."
            return f"{new_task} (Refined with feedback: {answer})"
        elif quality == "irrelevant":
            new_task = f"Clarify the following: {sub_task}"
            return f"{new_task} (Refined with feedback: {answer})"
        else:
            # default branch
            return f"{sub_task} (Refined with feedback: {answer})"
    
    def analyze_quality(self, answer):
        if len(answer.split()) < 10:
            # shport answers are considered bad 
            return "less_information"
        elif "not sure" in answer.lower() or "irrelevant" in answer.lower():
            # not correct
            return "irrelevant"
        else:
            # default return if it passes the two cases
            return "good"
