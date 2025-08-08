import google.generativeai as genai

model = genai.GenerativeModel("gemini-2.0-flash")

def code_analysis(code: str) -> str:
    prompt =f"""code analysis assistant trained in OWASP Secure Coding Practices.
Analyze the following code (code could be in any programming language) for security vulnerabilities and provide a secure version of it.

---
TASKS TO PERFORM:
1. Determine whether the code is **secure** or **insecure**.
2. If **insecure**, identify the **vulnerabilities** and **security flaws** present in the code.
3. Explain **why these flaws are dangerous** and which **OWASP principles** they violate.
4. List the **OWASP Secure Coding Practices** that are missing or violated.
5. Describe the **types of attacks** (e.g., SQL Injection, XSS, IDOR, etc.) that could be performed on this insecure code.
6. Provide a **secure version of the code**.
   - Include **clear code comments** to explain which parts were secured.
   - Specify **what libraries, techniques, or patterns** were used to fix it.
7. If the user returns with an issue in the secure code you generated, try to **debug and fix** it.
   - Provide a **short, clear explanation** of the issue.
   - Return a **fixed and working version** of the secure code.

---
⚠️ RESTRICTIONS:
- Do NOT answer questions unrelated to the submitted code or your feature.
- Only respond with the security analysis and improvements of the code as described above.
CODE:
 {code}
---
 RESPONSE FORMAT:

1. **Is the code secure?**  
   Yes / No

2. **Identified Vulnerabilities:**  
   - [List each vulnerability with its name and line reference if applicable]

3. **Explanation of Each Vulnerability:**  
   - [Explain why each is dangerous]

4. **Missing OWASP Secure Coding Practices:**  
   - [List which OWASP practices are not followed and how]

5. **Possible Attacks:**  
   - [List and explain what attacks could exploit the vulnerabilities]

6. **Secure Version of Code (with comments):**  
```python
# [Secure version of the code]"""  
    
    response = model.generate_content(prompt)
    return response.text.strip()
