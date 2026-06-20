import requests

def fetch_crypto_module():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            btc = data.get('bitcoin', {}).get('usd', 'N/A')
            eth = data.get('ethereum', {}).get('usd', 'N/A')
            return {"btc": f"${btc:,}", "eth": f"${eth:,}"}
    except Exception as e:
        print(f"Crypto API Error: {e}")
    return {"btc": "N/A", "eth": "N/A"}