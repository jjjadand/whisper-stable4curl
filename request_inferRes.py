import requests
import time

def get_result():
    url = "http://127.0.0.1:8080/result"
    try:
        r = requests.get(url, timeout=5)

        if r.status_code == 204:
            print("[…] No content yet")
            return

        if r.status_code != 200:
            print(f"[x] HTTP {r.status_code}: {r.text}")
            return

        ctype = r.headers.get("Content-Type", "")
        # 只在明确是 JSON 时才 parse
        if "application/json" in ctype:
            try:
                data = r.json()
                print("[✓] JSON:", data)
            except ValueError as e:
                print(f"[x] JSON decode failed: {e}\nRaw body: {r.text!r}")
        else:
            print(f"[i] Non-JSON response (Content-Type={ctype}): {r.text!r}")

    except requests.RequestException as e:
        print(f"[x] Connection error: {e}")

if __name__ == "__main__":
    while True:
        get_result()
        time.sleep(5)

