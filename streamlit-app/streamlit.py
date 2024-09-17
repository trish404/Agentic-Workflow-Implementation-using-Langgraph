import streamlit as st
from plan_tool_workflow import PlanAgent, ToolAgent # importing the agents for the workflow 
# custom pink ui as my preference 
st.markdown("""
    <style>
    .stApp {
        background-color: #ffe6f2; /* Light pink background */
    }
    .stTextInput > div > div > input {
        background-color: #ffffff; /* White background for input field */
        color: #333333; /* Text color */
    }
    .stButton > button {
        background-color: #ff69b4; /* Hot pink button color */
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

plan_agent = PlanAgent()

tool_agent = ToolAgent()

st.title("AI Task Processor")
st.markdown("<h3 style='color: #ff69b4;'>Enter your query and let the AI process it into actionable tasks.</h3>", unsafe_allow_html=True)

user_query = st.text_area("Enter your query:", height=100)

if st.button("Process Query"):
    if user_query:
        # loading spinner used while processing
        with st.spinner("Processing..."):
            # PlanAgent splits the user query into sub-queries or smaller taks 
            sub_tasks = plan_agent.split(user_query)

            # each sub query processed seperayely 
            refined_tasks = []
            for sub_task in sub_tasks:
                # skip empty sub-tasks
                if not sub_task.strip():
                    continue
                
                # solving using Tool Agent 
                response = tool_agent.execute(sub_task)
                
                # refinement of sub-task using feedback loop 
                refined_task = plan_agent.refine(sub_task, response)
                refined_tasks.append(refined_sub_task)

        
        st.header("Results:")
        for idx, task in enumerate(refined_sub_tasks):
            st.write(f"{task}")
    else:
        st.write("Please enter a query to start the workflow.")
