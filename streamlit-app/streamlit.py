import streamlit as st
from plan_tool_workflow import ToolAgent, process_query  # Make sure this is the correct import

def main():
    # Set background color using custom CSS
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #ffe6f0;  /* Light pink background */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("AI Task Processor")
    st.write("Enter your query and let the AI process it into actionable tasks.")

    # Input query from the user
    query = st.text_area("Enter your query:")

    # Get API keys from Streamlit secrets
    weather_api_key = st.secrets["WEATHER_API_KEY"]
    news_api_key = st.secrets["NEWS_API_KEY"]
    alpha_vantage_api_key = st.secrets["ALPHA_VANTAGE_API_KEY"]
    wolfram_api_key = st.secrets["WOLFRAM_API_KEY"]
    
    tool_agent = ToolAgent(weather_api_key, news_api_key, alpha_vantage_api_key, wolfram_api_key)

    # When the user clicks the "Process Query" button
    if st.button("Process Query"):
        if query:
            try:
                # Display a loading spinner while processing the query
                with st.spinner('Processing your query...'):
                    # Process the query
                    results = process_query(query, tool_agent)

                # Display the results
                st.write("### Results:")
                for result in results:
                    st.write(result)
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.write("Please enter a query to process.")

if __name__ == "__main__":
    main()
