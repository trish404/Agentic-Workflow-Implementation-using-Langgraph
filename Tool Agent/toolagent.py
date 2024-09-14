# skeletal structure before implementation of API
# -*- coding: utf-8 -*-
"""multiloop_workflow.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZycOvi0Qoa6KMemB8MSxD0Sj-ETGoB-y
"""

!pip install langgraph openai googlesearch-python requests

!pip install transformers flask gunicorn matplotlib graphviz

# plan agent
class PlanAgent:
    def __init__(self, query):
        # initialization of class
        self.query = query
        # user query
        self.sub_tasks = []
        # subtasks of that particular query

    def split_q(self):
        # using NLP sentence tokenization method to divide the query by a full stop
        self.sub_tasks = [job.strip() for job in self.query.split('.') if job.strip()]
        return self.sub_tasks

    def modify_t(self, t_id, new):
        # t_id = task's unique id/ index
        # function to modify already existing tasks in the list
        if 0 <= t_id < len(self.sub_tasks):
            # if a valid task id then it is modified
            self.sub_tasks[t_id] = new
            print(f"Task with id: {t_id}, is modified to: {new}")
        else:
            # else an error is thrown due to wrong indexing
            print("Please enter a valid task ID")

    def delete_t(self, t_id):
        # function to delete an already existing task
        if 0 <= t_id < len(self.sub_tasks):
            deleted_task = self.sub_tasks.pop(t_id) # popping from list since we use a stack like structure
            print(f"Task with id: {t_id}, is deleted: {deleted_task}")
        else:
            print("Please enter a valid task ID")

    def add_t(self, new_task):
        # function to add a new task
        self.sub_tasks.append(new_task)
        print(f"Added new task: {new_task}")

query = "Book a flight to San Francisco. Find the best Italian restaurants nearby. Schedule a meeting with the marketing team. Calculate the monthly budget for the project."
plan_agent = PlanAgent(query)
sub_tasks = plan_agent.split_q()
print("Initial Sub-tasks:", sub_tasks)
plan_agent.modify_t(0, "Find and book a flight to San Francisco for next Monday")
plan_agent.add_t("Look up the weather forecast for San Francisco")
plan_agent.delete_t(1)
print("Final Sub-tasks:", plan_agent.sub_tasks)

class ToolAgent:
    def __init__(self):
        pass

    def solve_task(self, task):
        # placeholder function for using some type of API to be used to obtain the result
        print(f"Solving task: {task}")
        # placeholder result for testing before integrating API
        result = f"Result for '{task}'"
        return result

    def feedback_integrate(self, task, result):
        # used to incorporate the feedback recieved from the workflow loop
        # simulation for testing before API usage to check working
        print(f"Reflection on task '{task}': {result}")

# integrating both Plan Agent and Tool Agent
query = "Book a flight to San Francisco. Find the best Italian restaurants nearby. Schedule a meeting with the marketing team. Calculate the monthly budget for the project."
plan_agent = PlanAgent(query)
sub_tasks = plan_agent.split_q()

tool_agent = ToolAgent()

# each sub-task is solved using the ToolAgent
results = []
for task in sub_tasks:
    result = tool_agent.solve_task(task)
    tool_agent.feedback_integrate(task, result)
    results.append(result)

print("Results:", results)
