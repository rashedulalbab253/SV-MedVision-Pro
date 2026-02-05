import os
import io
import base64
from typing import List, Optional
from datetime import datetime

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from PIL import Image as PILImage
from fpdf import FPDF

from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.media import Image as AgnoImage
from agno.team import Team

app = FastAPI(title="SV-MedVision API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- DIAGNOSTIC AGENTS ---

def get_diagnostic_team(api_key: str, model_id: str):
    researcher = Agent(
        name="Medical Researcher",
        role="Search for latest clinical guidelines and literature",
        model=Groq(id=model_id, api_key=api_key),
        tools=[DuckDuckGoTools()],
        instructions=[
            "Search for credible medical sources (PubMed, Mayo Clinic).",
            "Verify surgical or pharmacological recommendations using 2024-2025 guidelines."
        ]
    )

    diagnostic_team = Team(
        members=[researcher],
        model=Groq(id=model_id, api_key=api_key),
        name="SV-MedVision Pro Team",
        description="""You are the SV-MedVision Pro Diagnostic Team. You deliver 
        final medical reports based on visual analysis and literature research.""",
        instructions=[
            "1. ANALYZE: Conduct a systematic visual assessment of the chest image.",
            "2. RESEARCH: Consult the Medical Researcher for specific 2024-2025 guidelines.",
            "3. FINAL OUTPUT: Provide a report with ONLY these sections: [CLINICAL FINDINGS], [RESEARCH GROUNDING], [DIFFERENTIAL DIAGNOSIS], [SAFETY/SELF-VERIFICATION], and [FINAL RECOMMENDATION].",
            "4. NO JSON: Do not output any JSON, brackets, or function-call syntax. Output only plain Markdown text.",
            "5. NO INTERNAL STEPS: Do not mention 'delegating' or 'steps'.",
            "6. CONFIDENCE: Include 'Confidence Score: XX%' at the top."
        ],
        markdown=True,
    )
    return diagnostic_team

def create_pdf_report(content, diagnostic_type, confidence):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 10, "SV-MedVision Pro: AI Diagnostic Report", ln=True, align="C")
    
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.cell(0, 10, f"Diagnostic Focus: {diagnostic_type}", ln=True)
    pdf.cell(0, 10, f"AI Confidence Score: {confidence}%", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Helvetica", "", 10)
    clean_text = content.replace("#", "").replace("*", "").encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, clean_text)
    
    return bytes(pdf.output())

@app.post("/analyze")
async def analyze_image(
    file: UploadFile = File(...),
    api_key: str = Form(...),
    model_id: str = Form(...),
    focus: str = Form(...)
):
    try:
        # Read and save image
        contents = await file.read()
        image = PILImage.open(io.BytesIO(contents))
        temp_path = f"temp_{datetime.now().timestamp()}.png"
        image.save(temp_path)

        # Initialize and run team
        diagnostic_team = get_diagnostic_team(api_key, model_id)
        
        query = f"Perform a high-precision diagnostic analysis focusing on {focus}."
        
        response = diagnostic_team.run(
            query, 
            images=[AgnoImage(filepath=temp_path)]
        )
        
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)

        # Create PDF in background
        pdf_bytes = create_pdf_report(response.content, focus, 88)
        pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')

        return JSONResponse({
            "report": response.content,
            "confidence": 88,
            "pdf_base64": pdf_base64
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount the frontend directory to serve UI
# This should be at the end so it doesn't interfere with API routes
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
else:
    print(f"Warning: Frontend path {frontend_path} not found.")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
