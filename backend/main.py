from fastapi import FastAPI, Form
import requests

app = FastAPI()

def query_llama(prompt: str):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "llama2", "prompt": prompt, "stream": False}
    )
    return response.json()["response"].strip()

@app.post("/extract/")
def extract_medical_info(note: str = Form(...)):
    prompt = (
         f"Extract the following information from the doctor's note and return ONLY a JSON object with these exact keys:\n"
        f'{{"symptoms": "list of symptoms", "diagnosis": "diagnosis", "medications": "list of medications"}}\n\n'
        f"Doctor's note: {note}\n\n"
        f"Return only the JSON object, no other text:"
    )
    structured_data = query_llama(prompt)
    import re
    json_match = re.search(r'\{.*\}', structured_data, re.DOTALL)
    if json_match:
        structured_data = json_match.group()
    print(f"LLM Response: {structured_data}")
    return {"structured": structured_data}