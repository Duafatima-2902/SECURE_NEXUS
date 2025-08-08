import os
import time
import validators
from dotenv import load_dotenv
from zapv2 import ZAPv2
import requests

load_dotenv()

class WebVulnScanner:
    def __init__(self):
        self.api_key = os.getenv("ZAP_API_KEY", "")
        self.proxy = os.getenv("ZAP_PROXY", "http://127.0.0.1:8080")
        self.zap = ZAPv2(apikey=self.api_key, proxies={"http": self.proxy, "https": self.proxy})

    def _wait_for_zap(self, retries=5, delay=3):
        for attempt in range(retries):
            try:
                version = self.zap.core.version
                print(f"✅ Connected to ZAP API. Version: {version}")
                return True
            except Exception as e:
                print(f"❌ Could not connect to ZAP API (attempt {attempt+1}/{retries}): {e}")
                time.sleep(delay)
        print("❌ Failed to connect to ZAP API after multiple attempts.")
        return False

    def scan(self, target):
        if not validators.url(target):
            raise ValueError("Invalid target URL format. Example: http://example.com")

        if not self._wait_for_zap():
            return {"error": "ZAP is not reachable. Please start it and try again."}

        try:
            print(f"Starting spider on {target}...")
            spider_id = self.zap.spider.scan(target)
            while int(self.zap.spider.status(spider_id)) < 100:
                progress = self.zap.spider.status(spider_id)
                print(f"Spider progress: {progress}%")
                time.sleep(5)

            print("Spider complete. Starting active scan...")
            ascan_id = self.zap.ascan.scan(target)
            scan_start = time.time()
            max_scan_duration = 30 * 60  # 30 minutes in seconds

            while int(self.zap.ascan.status(ascan_id)) < 100:
                progress = self.zap.ascan.status(ascan_id)
                print(f"Active scan progress: {progress}%")
                time.sleep(10)

                # If scan runs longer than 30 minutes, stop waiting
                if time.time() - scan_start > max_scan_duration:
                    print("Reached maximum scan duration of 30 minutes. Stopping wait.")
                    break

            print("Scan complete. Gathering alerts...")
            alerts = self.zap.core.alerts(baseurl=target)
            print(f"Total alerts found: {len(alerts)}")
            return alerts

        except requests.exceptions.ProxyError:
            return {"error": "Could not connect to ZAP Proxy. Check if ZAP is running."}
        except Exception as e:
            return {"error": str(e)}

if __name__ == "__main__":
    scanner = WebVulnScanner()
    results = scanner.scan("http://testphp.vulnweb.com")
    print(results)
