from fastapi import FastAPI, Request, Form, BackgroundTasks, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import uvicorn
import tempfile
import asyncio
from concurrent.futures import ThreadPoolExecutor

import google.generativeai as genai

from code_analyzer import code_analysis
from phishing_detector import check_phishing
from web_vuln_scanner import WebVulnScanner
from zap_connection import test_zap_connection
from report_gen import generate_pdf_report  

load_dotenv()
api_key = os.getenv('Gemini_API_KEY')
if not api_key:
    raise ValueError("Gemini_API_KEY not found in environment variables.")

genai.configure(api_key=api_key)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# ThreadPoolExecutor for blocking scan calls
executor = ThreadPoolExecutor(max_workers=3)

class CodeRequest(BaseModel):
    code: str

class PhishingRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/code-analysis", response_class=HTMLResponse)
async def code_analysis_page(request: Request):
    return templates.TemplateResponse("code_analysis.html", {"request": request})

@app.get("/phishing", response_class=HTMLResponse)
async def phishing_page(request: Request):
    return templates.TemplateResponse("phishing_detector.html", {"request": request})

@app.get("/web-scan", response_class=HTMLResponse)
async def web_scan_page(request: Request):
    return templates.TemplateResponse("web_vuln_scanner.html", {"request": request})

@app.post("/api/analyze")
async def analyze_code_api(request: CodeRequest):
    try:
        result = code_analysis(request.code)
        return {"analysis": result}
    except Exception as e:
        return {"error": str(e)}

@app.post("/api/phishing-check")
async def phishing_check_api(request: PhishingRequest):
    try:
        result = check_phishing(request.message)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@app.post("/scan-web")
async def scan_web_api(url: str = Form(...)):
    if not test_zap_connection():
        return JSONResponse(content={"error": "ZAP is not reachable. Please start ZAP and try again."}, status_code=503)

    scanner = WebVulnScanner()

    try:
        # Run blocking scan in a thread to avoid blocking event loop
        alerts = await asyncio.get_event_loop().run_in_executor(executor, scanner.scan, url)
    except Exception as e:
        return JSONResponse(content={"error": f"Scanning failed: {str(e)}"}, status_code=500)

    if isinstance(alerts, dict) and alerts.get("error"):
        # Scan returned error dict
        return JSONResponse(content={"error": alerts["error"]}, status_code=500)

    # Create PDF report file path in temp directory
    temp_dir = tempfile.gettempdir()
    report_filename = f"SecureNexus_Scan_Report_{abs(hash(url))}.pdf"
    report_path = os.path.join(temp_dir, report_filename)

    try:
        generate_pdf_report(url, alerts, report_path)
    except Exception as e:
        return JSONResponse(content={"error": f"Report generation failed: {str(e)}"}, status_code=500)

    if not os.path.exists(report_path):
        return JSONResponse(content={"error": "Report file not found after generation."}, status_code=500)

    # Return PDF file as a download
    return FileResponse(report_path, media_type="application/pdf", filename="SecureNexus_Scan_Report.pdf")

@app.get("/api/download-report")
async def download_report(path: str):
    temp_dir = tempfile.gettempdir()
    full_path = os.path.join(temp_dir, path)
    if os.path.exists(full_path):
        return FileResponse(full_path, media_type='application/pdf', filename="SecureNexus_Scan_Report.pdf")
    else:
        return JSONResponse(content={"error": "Report file not found."}, status_code=404)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
