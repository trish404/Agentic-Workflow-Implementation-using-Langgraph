from transformers import pipeline

class PlanAgent:
    def __init__(self, query):
        self.query = query
        self.sub_tasks = []

    def split_q(self):
        # For simplicity, we split the tasks by period.
        # This can be made more complex using NLP techniques to better understand the query.
        self.sub_tasks = [task.strip() for task in self.query.split('.') if task.strip()]
        return self.sub_tasks

    def modify_t(self, index, new_task):
        if 0 <= index < len(self.sub_tasks):
            self.sub_tasks[index] = new_task

    def add_t(self, new_task):
        self.sub_tasks.append(new_task)

    def delete_t(self, index):
        if 0 <= index < len(self.sub_tasks):
            del self.sub_tasks[index]

# Function to integrate PlanAgent and ToolAgent
def process_query(query, tool_agent):
    # Initialize the PlanAgent with the query
    plan_agent = PlanAgent(query)

    # Split the query into sub-tasks
    sub_tasks = plan_agent.split_q()

    # Process each task using the ToolAgent
    results = []
    for task in sub_tasks:
        result = tool_agent.solve_task(task)
        tool_agent.reflect(task, result)
        results.append(result)

    return results

class ToolAgent:
    def __init__(self, weather_api_key, news_api_key, alpha_vantage_api_key, wolfram_api_key):
        self.weather_api_key = weather_api_key
        self.news_api_key = news_api_key
        self.alpha_vantage_api_key = alpha_vantage_api_key
        self.wolfram_api_key = wolfram_api_key
        self.summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

    def solve_task(self, task):
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
        location = task.split("in")[-1].strip()
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.weather_api_key}&units=metric"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather = data['weather'][0]['description']
            temperature = data['main']['temp']
            return f"The weather in {location} is {weather} with a temperature of {temperature}°C."
        else:
            return f"Could not fetch weather data for {location}. Error: {response.status_code} - {response.text}"

    def summarize_news(self, task):
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={self.news_api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            articles = data.get('articles', [])
            if articles:
                article_text = articles[0].get('content') or articles[0].get('description', '')
                if article_text:
                    summary = self.summarizer(article_text, max_length=50, min_length=25, do_sample=False)
                    return summary[0]['summary_text']
                else:
                    return "The fetched news article did not contain any text to summarize."
            else:
                return "No news articles available to summarize."
        else:
            return f"Could not fetch news articles. Error: {response.status_code} - {response.text}"

    def get_stock_price(self, task):
        company_to_symbol = {'Apple': 'AAPL', 'Google': 'GOOGL', 'Microsoft': 'MSFT'}
        company_name = task.split("of")[-1].strip().split()[0]
        symbol = company_to_symbol.get(company_name, company_name)
        
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={self.alpha_vantage_api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            try:
                latest_time = list(data['Time Series (1min)'].keys())[0]
                price = data['Time Series (1min)'][latest_time]['1. open']
                return f"The current stock price of {symbol} is ${price}."
            except KeyError:
                return f"Could not find stock symbol {symbol}."
        else:
            return f"Could not fetch stock data for {symbol}. Error: {response.status_code} - {response.text}"

    def calculate_expression(self, task):
        expression = task.split("Calculate")[-1].strip()
        url = f"http://api.wolframalpha.com/v2/query"
        params = {
            'input': expression,
            'format': 'plaintext',
            'output': 'JSON',
            'appid': self.wolfram_api_key
        }
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
            return f"Could not fetch the result for the mathematical expression. Error: {response.status_code} - {response.text}"

    def reflect(self, task, result):
        print(f"Reflection on task '{task}': {result}")

# Example usage of the integrated workflow
def main():
    # Initialize ToolAgent with your API keys
    weather_api_key = "YOUR_OPENWEATHERMAP_API_KEY"
    news_api_key = "YOUR_NEWSAPI_KEY"
    alpha_vantage_api_key = "YOUR_ALPHA_VANTAGE_API_KEY"
    wolfram_api_key = "YOUR_WOLFRAM_ALPHA_API_KEY"
    
    tool_agent = ToolAgent(weather_api_key, news_api_key, alpha_vantage_api_key, wolfram_api_key)
    
    query = "Find the weather in New York. Summarize the top news headlines. Check the stock prices of Apple. Calculate the square root of 16."
    
    # Process the query and get results
    results = process_query(query, tool_agent)

    # Print the results
    for result in results:
        print(result)

if __name__ == "__main__":
    main()
