import os
from dotenv import load_dotenv
from zapv2 import ZAPv2

load_dotenv()

ZAP_API_KEY = os.getenv("ZAP_API_KEY")
ZAP_PROXY = os.getenv("ZAP_PROXY", "http://127.0.0.1:8080")

proxies = {"http": ZAP_PROXY, "https": ZAP_PROXY}
zap = ZAPv2(apikey=ZAP_API_KEY, proxies=proxies)

def test_zap_connection():
    try:
        version = zap.core.version
        print(f"✅ Connected to ZAP API. Version: {version}")
        return True
    except Exception as e:
        print("❌ Could not connect to ZAP API.")
        print(f"Error: {e}")
        print("\nTroubleshooting tips:")
        print(" - Make sure ZAP is running on the host+port in ZAP_PROXY.")
        print(" - Confirm the API key matches ZAP (Tools → Options → API).")
        print(" - Make sure no firewall blocks localhost:8080.")
        return False  # Return False on failure

if __name__ == "__main__":
    test_zap_connection()
