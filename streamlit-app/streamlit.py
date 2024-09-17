import streamlit as st
from plan_tool_workflow import PlanAgent, ToolAgent

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
            #  PlanAgent splits the user query into sub-queries or smaller tasks using lang graph
            graph = plan_agent.create_graph(user_query)

            # each sub query processed seperayely 
            for node in graph.nodes:
             
                Answer = tool_agent.execute(node.content)
                # refinement of the answer 
                plan_agent.refine(node, Answer)

      
        st.header("Results:")
        for node in graph.nodes:
            st.write(node.content)
    else:
        st.write("Please enter a query to start the workflow.")
