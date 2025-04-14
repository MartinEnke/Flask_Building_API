import requests
import time

URL = "http://127.0.0.1:5019/api/books"  # Adjust if needed
page = 1

for i in range(1, 13):
    response = requests.get(URL)
    status = response.status_code

    if status == 200:
        print(f"✅ Request {i}: Success")
    elif status == 429:
        retry_after = response.headers.get("Retry-After", "unknown")
        print(f"❌ Request {i}: Rate limit exceeded. Retry after {retry_after} seconds.")
    else:
        print(f"⚠️ Request {i}: Unexpected status code {status}")

    time.sleep(1)