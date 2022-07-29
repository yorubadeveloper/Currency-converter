# Currency Converter with FastAPI

### Main features

* currencies are updated every day
* source data is fetched via [http://openexchange.org](http://openexchange.org)


### Endpoints

|Method| URL                         | Path Params                       | Description                               |
|------|-----------------------------|-----------------------------------|-------------------------------------------|
|**GET**| `/api/v1/currencies` |                                   | Gets all currencies and their codes       |
|**GET**| `/api/v1/currencies/convert` | `base/to/amount` _(all required)_ | Converts `base` currency to `to` currency |

### Prerequisites

* Python3.6+
* Redis


### Installation

1. Get a free API Key at [http://openexchangerates.org](http://openexchangerates.org)
2. Clone the repo
3. Create a `.env` file to hold credentials
4. Add the following in your `.env` file
    ```shell
   EXCHANGE_API_KEY=API_Provider_key
    EXCHANGE_URL=API_Provider_URL
    REDIS_URL=redis_url (e.g 'redis://127.0.0.1:6379')
    APP_API_KEY=API_KEY for authentication (e.g 12345)
    ```
5. Create a virtual environment and install necessary packages. Run:
    ```shell
    pip install -r requirements.txt
    ```
6. After successfully completing the above. Run the application:
    ```shell
    python main.py
    ```

### Usage
- Get currencies
    ```shell 
    curl -X GET "$HOST/api/v1/currencies" -H  "accept: application/json" -H "api_key: API_KEY"
    ```
- Convert currencies
    ```shell 
    curl -X GET "$HOST/api/v1/currencies/convert/{base}/{to}/{amount}" -H  "accept: application/json" -H "api_key: API_KEY"
    ```

#### Example request
- Get currencies
    ```shell 
    curl -X GET "http://0.0.0.0:8000/api/v1/currencies" -H  "accept: application/json" -H "api_key: 12345"
    ```
  ##### Response (Code 200)

    ```json
    {
      "currency": {
        "CAD": "Canadian Dollar",
        "EUR": "Euro",
        "NGN": "Nigerian Naira",
        "USD": "United States Dollar"
      }
   }
    ```
- Convert currencies
    ```shell script
    curl -X GET "http://0.0.0.0:8000/api/v1/currencies/convert/USD/EUR/123" -H  "accept: application/json" -H "api_key: 12345"
    ```

    ##### Response (Code 200)
    
    ```json
    {
      "base": "USD",
      "to": "EUR",
      "amount": 10,
      "exchange_rate": 0.981,
      "result": 9.81
    }
    ```

### Documentation
Visit /docs or /redoc to see a Swagger or ReDoc API Documentation