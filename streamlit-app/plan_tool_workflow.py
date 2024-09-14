from transformers import pipeline
import requests
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
# function to integrate both agents in the same workflow 
def process_query_with_feedback(query, tool_agent, max_iterations=3):
    # plan agent is used to process the query 
    plan_agent = PlanAgent(query)
    # query is split into all the tasks 
    sub_tasks = plan_agent.split_q()
    results = []

    iteration = 0
    while iteration < max_iterations and sub_tasks:
        new_sub_tasks = []
        for task in sub_tasks:
            # Tool Agent processes each sub task 
            result = tool_agent.solve_task(task)
            tool_agent.reflect(task, result)
            results.append(result)

            # feedback is done by checking if it needs any refinement 
            if "could not" in result.lower():
                # if result shows failure another try is made 
                refined_task = f"Reattempt: {task}"
                new_sub_tasks.append(refined_task)
            else:
                # follow up tasks if it is successful
                pass
        
        sub_tasks = new_sub_tasks
        iteration += 1

    return results

class ToolAgent:
    def __init__(self, weather_api_key, news_api_key, alpha_vantage_api_key, wolfram_api_key):
        # all the api keys are stored in the secrets 
        self.weather_api_key = weather_api_key
        self.news_api_key = news_api_key
        self.alpha_vantage_api_key = alpha_vantage_api_key
        self.wolfram_api_key = wolfram_api_key
        self.summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
        # pipeline is used for orderly processing of the queries / subtasks 

    def solve_task(self, task):
        # tool agent can do the following tasks there is future scope for more 
        if "weather" in task.lower():
            return self.get_weather(task)
        elif "summarize" in task.lower() or "news" in task.lower():
            return self.summarize_news(task)
        elif "stock" in task.lower() or "prices" in task.lower():
            return self.get_stock_price(task)
        elif "calculate" in task.lower():
            return self.calculate_expression(task)
        else:
            return f"No specific tool found for the task: '{task}'"

    def get_weather(self, task):
        # to get the weather report 
        loc = task.split("in")[-1].strip() # used to extract location from the query 
        url = f"http://api.openweathermap.org/data/2.5/weather?q={loc}&appid={self.weather_api_key}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather = data['weather'][0]['description']
            temp = data['main']['temp'] # temperature found using api 
            return f"The weather in {loc} is {weather} with a temperature of {temp}°C."
        else:
            return f"Could not fetch weather data for {location}. Please try again later"

    def summarize_news(self, task):
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={self.news_api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            if articles:
                txt = articles[0].get('content') or articles[0].get('description', '')
                if txt: # article text is used to summarize 
                    summary = self.summarizer(txt, max_length=50, min_length=25, do_sample=False)
                    return summary[0]['summary_text']
                else:
                    return "The fetched news article did not contain any text to summarize."
            else:
                return "No news articles available to summarize."
        else:
            return f"Could not fetch news articles."

    def get_stock_price(self, task):
        company_to_symbol = {'Apple': 'AAPL', 'Google': 'GOOGL', 'Microsoft': 'MSFT'}
        company_name = task.split("of")[-1].strip().split()[0]
        symbol = company_to_symbol.get(company_name, company_name)
        # using symbols to convert since the api doesnt actually use the company names 
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={self.alpha_vantage_api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            try:
                latest_time = list(data['Time Series (1min)'].keys())[0]
                price = data['Time Series (1min)'][latest_time]['1. open']
                return f"The current stock price of {company_name} is ${price}."
            except KeyError:
                return f"Could not find stock symbol {company_name}."
        else:
            return f"Could not fetch stock data for {company_name}."

    def calculate_expression(self, task):
        expression = task.split("Calculate")[-1].strip()
        url = f"http://api.wolframalpha.com/v2/query"
        params = {
            'input': expression,
            'format': 'plaintext',
            'output': 'JSON',
            'appid': self.wolfram_api_key
        }
        # convert the textual interpretation to numerical to obtain the results 
        response = requests.get(url, params=params)
        if response.status_code == 200:
            try:
                data = response.json()
                for pod in data['queryresult']['pods']:
                    if pod['title'] == 'Result' or 'Decimal approximation' in pod['title']:
                        result = pod['subpods'][0]['plaintext']
                        return f"Result of {expression}: {result}"
                return "Could not understand the mathematical expression."
            except (KeyError, IndexError):
                return "Could not understand the mathematical expression."
        else:
            return f"Could not fetch the result for the mathematical expression."

    def reflect(self, task, result):
        print(f"Reflection on task '{task}': {result}")

# main function to integrate the workflow 
def main():
    # api keys 
    weather_api_key = "YOUR_OPENWEATHERMAP_API_KEY"
    news_api_key = "YOUR_NEWSAPI_KEY"
    alpha_vantage_api_key = "YOUR_ALPHA_VANTAGE_API_KEY"
    wolfram_api_key = "YOUR_WOLFRAM_ALPHA_API_KEY"
    
    tool_agent = ToolAgent(weather_api_key, news_api_key, alpha_vantage_api_key, wolfram_api_key)
    # sample query i used for debugging 
    query = "Find the weather in New York. Summarize the top news headlines. Check the stock prices of Apple. Calculate the square root of 16."
    
    results = process_query(query, tool_agent)

    for result in results:
        print(result)

if __name__ == "__main__":
    main()
