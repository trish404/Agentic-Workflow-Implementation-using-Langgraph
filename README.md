# Agentic-Workflow-Implementation-using-Langgraph
The aim is to implement the following workflow using Langgraph
<img width="635" alt="Screenshot 2024-09-14 at 11 10 38 AM" src="https://github.com/user-attachments/assets/6ed63e3f-3562-4ee9-857c-18f8359d3422">


## Plan Agent 
1. A plan agent is used to split the user query into smaller sub tasks to be individually processed by the tool agent
2. It also recieves feedback from the Tool Agent which it modifies / splits to be processed again
3. It then passes on the processed feedback to the User

## Tool Agent 
1. Recieves the sub queries from the plan agent
2. Solves the queries using API's
3. Reflects on the results
4. Uses feedback to improve quality
5. Provides the results to the Plan Agent for it to give it to the user
