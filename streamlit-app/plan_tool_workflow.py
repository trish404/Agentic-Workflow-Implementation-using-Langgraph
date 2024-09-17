import openai
import streamlit as st
from langgraph import LangGraph, Node  # Assuming langgraph is installed

class ToolAgent:
    def __init__(self):
        # api key in the secrets 
        openai.api_key = st.secrets["openai"]["api_key"]

    def execute(self, task):
        try:
            answer = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a knowledgeable assistant."}, # defining the role of the AI 
                    {"role": "user", "content": task}
                ],
                max_tokens=100,       
                temperature=0.7       # randomness in output
            )

            return answer.choices[0].message['content'].strip()
        except Exception as e:
            return f"Error executing sub-task: {str(e)}"

class PlanAgent:
    def create_graph(self, query):
        # language graph from the query
        graph = LangGraph()
        # query into sub-tasks and turned into nodes
        sub_tasks = self.split(query)
        for task in sub_tasks:
            # each sub-task as a node in the graph
            graph.add_node(Node(task))
        return graph

    def split(self, query):
        # basic NLP sentence tokenozation
        sub_tasks = query.split('. ')
        return [task.strip() for task in sub_tasks if task.strip()]

    def refine(self, node, answer):
        quality = self.analyze_quality(answer)
        
        if quality == "good":
            node.content += f" (Refined with good feedback: {answer})"
        elif quality == "missing_info":
            node.content += f". Please provide more details for a better answer. (Refined with feedback: {answer})"
        elif quality == "irrelevant":
            node.content = f"Clarify the following for a more accurate answer: {node.content} (Refined with feedback: {answer})"
        else:
            node.content += f" (Refined with feedback: {answer})"
    
    def analyze_quality(self, answer):
        if len(answer.split()) < 10:
            # if answer is too short it might be missing information
            return "missing_info"
        elif "not sure" in answer.lower() or "irrelevant" in answer.lower():
            return "irrelevant"
        else:
            # if it passes both criteria it is considered good
            return "good"
