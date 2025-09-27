from fastapi import FastAPI, UploadFile, File, Form
from PIL import Image
import pytesseract, spacy
import actions

app = FastAPI(title="Intelligent Data→Action")

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Initialize DB on startup
@app.on_event("startup")
def startup_event():
    actions.init_db()

# Create a task from text
@app.post("/create_task")
async def create_task_route(text: str = Form(...)):
    doc = nlp(text)
    structured = {"text": text, "tokens": [token.text for token in doc]}
    return actions.create_task(structured)

# Create an invoice from image
@app.post("/create_invoice")
async def create_invoice_route(file: UploadFile = File(...)):
    img = Image.open(file.file)
    text = pytesseract.image_to_string(img)
    structured = {"text": text}
    return actions.create_invoice(structured)

# Create a note
@app.post("/create_note")
async def create_note_route(text: str = Form(...)):
    structured = {"text": text}
    return actions.create_note(structured)

# Create an issue
@app.post("/create_issue")
async def create_issue_route(text: str = Form(...)):
    structured = {"text": text}
    return actions.create_issue(structured)
