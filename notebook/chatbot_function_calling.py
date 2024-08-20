import json
import os
import requests
from vnstock3 import Vnstock
import os
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd
load_dotenv()

client = OpenAI(api_key =os.getenv('OPEN_API_KEY'))

# def get_current_weather(latitude, longitude):
#     """Get the current weather in a given latitude and longitude"""
#     base = "https://api.openweathermap.org/data/2.5/weather"
#     key = os.environ['WEATHERMAP_API_KEY']
#     request_url = f"{base}?lat={latitude}&lon={longitude}&appid={key}&units=metric"
#     response = requests.get(request_url)

#     result = {
#         "latitude": latitude,
#         "longitude": longitude,
#         **response.json()["main"]
#     }

#     return json.dumps(result)

def generate_prompt_with_date(prompt):
    from datetime import datetime
    current_date = datetime.now().strftime("%Y-%m-%d")
    full_prompt = f"{prompt} Today's date is {current_date}."
    return full_prompt


def get_company_information(symbol):
    """Get company information such as overview, profile, shareholders, subsidiaries, and officers."""
    company = Vnstock().stock(symbol=symbol, source='TCBS').company
    
    try:
        overview = company.overview()
        profile = company.profile()  # Assuming profile is another method; adjust if incorrect
        shareholders = company.shareholders()
        subsidiaries = company.subsidiaries()
        officers = company.officers()
        
        result = {
            "overview": overview,
            "profile": profile,
            "shareholders": shareholders,
            "subsidiaries": subsidiaries,
            "officers": officers
        }
    except Exception as e:
        result = {"error": str(e)}
    
    return json.dumps(result)



def get_api_stock(symbols, startday, endday):
    """Get stock data for a given symbol and date range."""
    stock = Vnstock().stock(symbol=symbols, source='TCBS')
    
    try:
        df = stock.quote.history(start=startday, end=endday, interval='1m')
        
        if not df.empty:
            df = df.map(lambda x: x.isoformat() if isinstance(x, (pd.Timestamp, pd.Timestamp)) else x)
            result = df.to_dict(orient='records')
        else:
            result = {"error": "No data found for the given range"}
    
    except Exception as e:
        result = {"error": str(e)}
    
    return json.dumps(result)



def get_api_income_statement(symbols):
    stock = Vnstock().stock(symbol=symbols, source='TCBS')
    try:
        df = stock.finance.income_statement(period='year', lang='en')
        if not df.empty:
            result = df.to_dict(orient='records')
        else:
            result = {"error": "No data found for the given range"}
    except Exception as e:
        result = {"error": str(e)}
    
    return json.dumps(result)

def get_api_balance_sheet(symbols):
    stock = Vnstock().stock(symbol=symbols, source='TCBS')
    try:
        df = stock.finance.balance_sheet(period='year', lang='en')
        if not df.empty:
            result = df.to_dict(orient='records')
        else:
            result = {"error": "No data found for the given range"}
    except Exception as e:
        result = {"error": str(e)}
    
    return json.dumps(result)

def run_conversation(content):
  messages = [
      {
            "role":"system",
            "content": "Base on the information return by function calling to answer question."
        },
      {
          "role": "user", 
          "content": content
        }
          ]
  tools = [
    #   {
    #       "type": "function",
    #       "function": {
    #           "name": "get_current_weather",
    #           "description": "Get the current weather in a given latitude and longitude",
    #           "parameters": {
    #               "type": "object",
    #               "properties": {
    #                   "latitude": {"type": "string", "description": "The latitude of a place"},
    #                   "longitude": {"type": "string", "description": "The longitude of a place"},
    #               },
    #               "required": ["latitude", "longitude"],
    #           },
    #       },
    #   },
      {
          "type": "function",
          "function": {
              "name": "get_company_information",
              "description": "Get company information such as overview, profile, shareholders, subsidiaries, and officers",
              "parameters": {
                  "type": "object",
                  "properties": {
                      "symbol": {"type": "string", "description": "The stock symbol of the company"},
                  },
                  "required": ["symbol"],
              },
          },
      },
      {
          "type": "function",
          "function": {
              "name": "get_api_stock",
              "description": "Get stock data for a given symbol and date range",
              "parameters": {
                  "type": "object",
                  "properties": {
                      "symbols": {"type": "string", "description": "The stock symbol"},
                      "startday": {"type": "string", "description": "Start date in YYYY-MM-DD format"},
                      "endday": {"type": "string", "description": "End date in YYYY-MM-DD format"},
                  },
                  "required": ["symbols", "startday", "endday"],
              },
          },
      },
      {
          "type": "function",
          "function": {
              "name": "get_api_income_statement",
              "description": "Get the income statement for a given symbol",
              "parameters": {
                  "type": "object",
                  "properties": {
                      "symbols": {"type": "string", "description": "The stock symbol"},
                  },
                  "required": ["symbols"],
              },
          },
      },
      {
          "type": "function",
          "function": {
              "name": "get_api_balance_sheet",
              "description": "Get the balance sheet for a given symbol",
              "parameters": {
                  "type": "object",
                  "properties": {
                      "symbols": {"type": "string", "description": "The stock symbol"},
                  },
                  "required": ["symbols"],
              },
          },
      }
  ]
  
  response = client.chat.completions.create(
      model="gpt-3.5-turbo-0125",
      messages=messages,
      tools=tools,
      tool_choice="auto",
  )
  response_message = response.choices[0].message
  tool_calls = response_message.tool_calls

  if tool_calls:
    messages.append(response_message)

    available_functions = {
        # "get_current_weather": get_current_weather,
        "get_company_information": get_company_information,
        "get_api_stock": get_api_stock,
        "get_api_income_statement": get_api_income_statement,
        "get_api_balance_sheet": get_api_balance_sheet,
    }
    for tool_call in tool_calls:
      print(f"Function: {tool_call.function.name}")
      print(f"Params:{tool_call.function.arguments}")
      function_name = tool_call.function.name
      function_to_call = available_functions[function_name]
      function_args = json.loads(tool_call.function.arguments)
      function_response = function_to_call(**function_args)
    #   print(f"API: {function_response}")
      messages.append(
        {
          "tool_call_id": tool_call.id,
          "role": "tool",
          "name": function_name,
          "content": function_response,
        }
      )

    second_response = client.chat.completions.create(
      model="gpt-3.5-turbo-0125",
      messages=messages,
      stream=True
    )
    return second_response

if __name__ == "__main__":
  question = "The current stock situation of VCI today 2024-08-20, what is the index?"
  response = run_conversation(question)
  for chunk in response:
    print(chunk.choices[0].delta.content or "", end='', flush=True)