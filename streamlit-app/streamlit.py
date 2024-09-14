import streamlit as st
from plan_tool_workflow import ToolAgent, process_query  # imports from the file 

def main():
    # customizing the ui
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #ffe6f0;  
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Agentic Workflow Implementation using Langgraph")
    st.write("Enter your query and let us try to find the answers !!!")

    query = st.text_area("Enter your query:")

    # API keys from secrets 
    weather_api_key = st.secrets["WEATHER_API_KEY"]
    news_api_key = st.secrets["NEWS_API_KEY"]
    alpha_vantage_api_key = st.secrets["ALPHA_VANTAGE_API_KEY"]
    wolfram_api_key = st.secrets["WOLFRAM_API_KEY"]
    
    tool_agent = ToolAgent(weather_api_key, news_api_key, alpha_vantage_api_key, wolfram_api_key)
    # upon click of the process button 
    if st.button("Process Query"):
        if query:
            try:
            
                with st.spinner('Processing your query...'):
                # feedback loop
                    results = process_query_with_feedback(query, tool_agent)

                st.write("### Results:")
                for result in results:
                    st.write(result)
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.write("Please enter a query to process.")

if __name__ == "__main__":
    main()
