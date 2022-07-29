import os
import json
import requests
from fastapi import Security, HTTPException
from fastapi.security.api_key import APIKeyHeader
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get('APP_API_KEY')
api_key_header = APIKeyHeader(name="api_key", auto_error=True)
EXTERNAL_API_URL = os.environ.get('EXCHANGE_URL')
EXTERNAL_API_ID = os.environ.get('EXCHANGE_API_KEY')


# Function to fetch all currencies from external API and saves in currencies.json
def fetch_currencies_from_api():
    url = EXTERNAL_API_URL + "currencies.json"
    response = requests.get(url)
    if response.ok:
        currencies = response.json()
        with open('currencies.json', 'w') as f:
            json.dump(currencies, f)


# Function to get all currencies saved in currencies.json
def get_all_currencies():
    with open('currencies.json') as json_file:
        currencies = json.load(json_file)
        return {"currencies": currencies}


# Function to fetch the convert rates for currencies from the external API
def fetch_rates_from_api(base, to):
    url = EXTERNAL_API_URL + "latest.json"
    params = {
        "app_id": EXTERNAL_API_ID,
        "base": base,
    }
    response = requests.get(url, params=params)
    if response.ok:
        rates = response.json()['rates']
        current_rate = rates[to] / rates[base]
        return round(current_rate, 3)


# Function that converts the currencies using data from the exchange rates
def convert_currencies(amount, exchange_rate):
    result = exchange_rate * amount
    return round(result, 3)


# Function that validates the API_KEY
async def get_api_key(
    api_key_header: str = Security(api_key_header),
):
    if api_key_header == API_KEY:
        return api_key_header
    else:
        raise HTTPException(status_code=403)