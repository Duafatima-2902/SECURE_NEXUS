import google.generativeai as genai

model = genai.GenerativeModel("gemini-2.0-flash")

def check_phishing(message: str) -> str:
    prompt = f"""
You are a phishing detection expert. Your task is to analyze the following email or text message to determine if it is a phishing attack.

--- 
TEXT TO ANALYZE:
\"\"\"
{message}
\"\"\"

---

Your analysis must include the following:

1. **Is this a phishing message?** (Yes / No)
2. **Suspicious Elements:**  
   - Identify any red flags like urgent language, tone, suspicious links, fake sender names, grammatical errors, or requests for personal/financial information.
3. **Reasoning:**  
   - Explain why the message is (or is not) considered phishing.
4. **Safety Recommendations:**  
   - If it's phishing, advise on what action the user should take (e.g., delete the message, report it, don’t click links, etc.)
5. **Future Awareness Tips:**  
   - Give at least 3 tips to help the user avoid phishing attacks like this in the future.

⚠️ RULES:
- Never click links or download attachments from unknown or suspicious sources.
- Be cautious of emails pretending to be from banks, tech companies, or government organizations.
- Look for spelling/grammar mistakes, urgency, or strange email addresses.
"""


    response = model.generate_content(prompt)
    return response.text.strip()