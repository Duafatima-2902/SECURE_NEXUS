# SecureNexus

SecureNexus is a comprehensive cybersecurity tool built with FastAPI that provides:

- **AI Code Analyzer:** Analyze source code to detect security vulnerabilities and suggest fixes.
- **Phishing Detector:** Detect whether an email or message is phishing or not using AI-based analysis.
- **Web Vulnerability Scanner:** Perform automated web vulnerability scanning using OWASP ZAP and generate PDF scan reports.

---

## Features

- **Code Security Analysis:**  
  Paste your code to receive a detailed AI-generated security assessment.

- **Phishing Detection:**  
  Paste email or message content to check for phishing risks with AI.

- **Website Vulnerability Scanning:**  
  Enter a website URL to scan for common vulnerabilities using OWASP ZAP, with downloadable detailed PDF reports.

- **User Interface:**  
  Responsive, modern UI with syntax-highlighted code output and clear result displays.

---

## How It Works

- **AI Integration:**  
  Utilizes Google Gemini API (via `google.generativeai` library) for code and phishing analysis.

- **OWASP ZAP Integration:**  
  Uses ZAP’s API for automated web vulnerability scanning.

- **Asynchronous & Threaded Execution:**  
  Runs long-running scans in background threads to maintain server responsiveness.

- **PDF Report Generation:**  
  Generates detailed PDF reports summarizing scan results for easy sharing and documentation.

- **Clean UI:**  
  Built with FastAPI’s Jinja2 templates and modern CSS for a polished user experience.

---

## Setup and Installation

### Prerequisites

- Python 3.8 or higher
- OWASP ZAP installed and running locally with API enabled
- Google Gemini API key (or equivalent AI API key)
- `pip` package manager

### Installation Steps

1. **Clone the repository:**

   git clone https://github.com/yourusername/SecureNexus.git
   cd SecureNexus
Create and activate a virtual environment (recommended):

python -m venv venv
source venv/bin/activate    # On Windows use `venv\Scripts\activate`

2. Install Python dependencies:
pip install -r requirements.txt

3. Configure environment variables:
Create a .env file in the project root containing:

4. Gemini_API_KEY=your_google_gemini_api_key_here
5. ZAP_API_KEY=your_zap_api_key_if_set
  ZAP_PROXY=http://127.0.0.1:8080
6. Start OWASP ZAP:
Ensure OWASP ZAP is running locally with API access enabled at the proxy URL (default: http://127.0.0.1:8080).

7. Run the FastAPI app:
uvicorn main:app --host 127.0.0.1 --port 8080 --reload
8. Access the app in your browser:
-> Navigate to http://127.0.0.1:8080

Project Structure
1. main.py — FastAPI application entry point; API routes and HTML rendering
2. code_analyzer.py — AI-powered code security analysis logic
3. phishing_detector.py — AI-based phishing detection logic
4. web_vuln_scanner.py — OWASP ZAP API wrapper for website scanning
5. zap_connection.py — Utility to verify ZAP API availability
6. report_gen.py — PDF report generation for scan results
7. templates/ — Jinja2 HTML templates for UI pages
9. static/ — CSS and JavaScript files for frontend
10. .env — Environment variables file (not committed to repo)
11. requirements.txt — Python dependencies list

Usage
-Code Analyzer:
Paste or upload your source code, then click Analyze to view vulnerability reports.

-Phishing Detector:
Paste email or message content to determine phishing risk.

-Web Scanner:
Enter a URL and run a web vulnerability scan. Download the generated PDF report upon completion.

-Important Notes
- OWASP ZAP: Must be running locally with API enabled for web scanner functionality.
- API Keys: Ensure all API keys are valid and set correctly in the .env file.
- Scan Duration: Web vulnerability scans may take several minutes depending on target site size.
- Report Storage: PDF reports are temporarily stored in the system’s temporary directory.

_____________________________________________________________________________________________
- SECURE NEXUS
<img width="1078" height="567" alt="image" src="https://github.com/user-attachments/assets/d19c3072-6d1c-4e93-90ef-973410fbca46" />

- SECURE CODE ANALYSIS
<img width="676" height="802" alt="image" src="https://github.com/user-attachments/assets/5242dbde-c854-47de-873e-204d81362ded" />

- PHISHING DETECTION ANALYSIS
<img width="695" height="807" alt="image" src="https://github.com/user-attachments/assets/7a6c9f80-d19a-469c-acca-e15378ca17bf" />

- WEB VULNERABILITY SCANNER
<img width="455" height="402" alt="image" src="https://github.com/user-attachments/assets/5a87dd2b-34da-4698-b10d-8e5d686b527c" />

