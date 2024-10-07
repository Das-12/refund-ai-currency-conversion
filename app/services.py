import requests

def fetch_conversion_rates(to_currency: str):
    api_key = "8a491588a1ecffee111d490c"  # Your API Key
    api_endpoint = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/{to_currency}"
    
    response = requests.get(api_endpoint)
    
    if response.status_code == 200:
        data = response.json()
        return data.get('conversion_rates', {})
    else:
        return None
