# SV-MedVision Pro: Agentic Multi-modal Grounding for Autonomous Radiology 🏥
### Advanced Multi-Agent Clinical Diagnostic System

**Developed by: Rashedul Albab**  
**GitHub:** [rashedulalbab253](https://github.com/rashedulalbab253)  
**Docker Hub:** [rashedulalbab1234](https://hub.docker.com/u/rashedulalbab1234)

---

## 🌟 Overview
SV-MedVision Pro is a high-performance, full-stack medical AI platform designed for automated diagnostic imaging analysis. It utilizes a **Multi-Agent Orchestration** architecture to provide grounded, verified clinical reports from X-rays, MRIs, and CT scans.

### 🔬 Key Features
- **Agentic Diagnostic Team**: A collaborative hierarchy consisting of a Lead Radiologist and a specialized Medical Researcher.
- **Real-Time Clinical Grounding**: Uses RAG to consult 2024-2025 clinical literature (PubMed, Mayo Clinic) before finalizing reports.
- **Flash Inference**: Powered by **Groq LPUs** (Llama 4 Scout) for near-instant analysis.
- **Professional PDF Export**: Generates timestamped, clinical-grade reports automatically.
- **Modern UI**: A premium 'Midnight Cyber' dashboard built for professional clinical environments.

## 🏗️ Architecture
- **Backend**: FastAPI (Python)
- **AI Framework**: Agno (Phidata)
- **Frontend**: High-fidelity HTML5/CSS3/Vanilla JS
- **Containerization**: Docker & GitHub Actions CI/CD

## 🚀 Getting Started

### Local Setup
1. **Clone the repository**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Backend**:
   ```bash
   uvicorn backend.main:app --reload
   ```
4. **Access the UI**: Open `http://localhost:8000`

### Docker Setup
```bash
docker pull rashedulalbab1234/sv-medvision-pro:latest
docker run -p 8000:8000 rashedulalbab1234/sv-medvision-pro:latest
```

---
*PhD Level Portfolio Project | Research Interest: Multi-modal AI & Clinical Safety.*