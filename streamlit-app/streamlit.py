import streamlit as st
from plan_agent import PlanAgent
from tool_agent import ToolAgent

# Set your OpenAI API key
openai.api_key = 'your-openai-api-key'

# Initialize PlanAgent
plan_agent = PlanAgent()

# Initialize ToolAgent
tool_agent = ToolAgent()

# Streamlit app
st.title("LangGraph Workflow Implementation")

# User query input
user_query = st.text_input("Enter your query:")

if user_query:
    # Step 1: PlanAgent splits the user query into sub-tasks
    st.header("Outer Loop: PlanAgent Execution")
    st.write("Splitting query into sub-tasks...")
    sub_tasks = plan_agent.split(user_query)
    st.write("Sub-tasks:", sub_tasks)

    # Step 2: Iterative Refinement
    refined_sub_tasks = []
    for sub_task in sub_tasks:
        st.write(f"Refining sub-task: {sub_task}")
        
        # Solve each sub-task using ToolAgent
        st.header("Inner Loop: ToolAgent Execution")
        st.write("Agent Dispatch & Tool Retrieval...")
        response = tool_agent.execute(sub_task)
        st.write("Response:", response)
        
        # Modification, Deletion, Addition (if needed)
        st.write("Iterative Refinement (Modification/Deletion/Addition)...")
        refined_sub_task = plan_agent.refine(sub_task, response)
        refined_sub_tasks.append(refined_sub_task)

    # Final results
    st.header("End Result")
    st.write("All done! Refined sub-tasks:")
    st.write(refined_sub_tasks)
else:
    st.write("Please enter a query to start the workflow.")
