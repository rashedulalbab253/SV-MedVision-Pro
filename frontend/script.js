const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const imagePreview = document.getElementById('imagePreview');
const analyzeBtn = document.getElementById('analyzeBtn');
const reportContent = document.getElementById('reportContent');
const loader = document.getElementById('loader');
const downloadBtn = document.getElementById('downloadBtn');
const confidenceValue = document.getElementById('confidenceValue');
const confidenceFill = document.getElementById('confidenceFill');
const metricsCard = document.getElementById('metricsCard');

let currentFile = null;
let pdfBase64 = null;

// Handle File Selection
dropZone.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', (e) => {
    handleFile(e.target.files[0]);
});

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('active');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('active');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    handleFile(e.dataTransfer.files[0]);
});

function handleFile(file) {
    if (file && file.type.startsWith('image/')) {
        currentFile = file;
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            imagePreview.classList.remove('hidden');
            analyzeBtn.disabled = false;
        };
        reader.readAsDataURL(file);
    }
}

// Execute Analysis
analyzeBtn.addEventListener('click', async () => {
    const apiKey = document.getElementById('apiKey').value;
    if (!apiKey) {
        alert('Please enter your Groq API Key');
        return;
    }

    // UI Feedback
    analyzeBtn.disabled = true;
    reportContent.classList.add('hidden');
    loader.classList.remove('hidden');
    metricsCard.classList.add('hidden');

    const formData = new FormData();
    formData.append('file', currentFile);
    formData.append('api_key', apiKey);
    formData.append('model_id', document.getElementById('modelSelect').value);
    formData.append('focus', document.getElementById('focusSelect').value);

    try {
        const response = await fetch('http://localhost:8000/analyze', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            displayReport(data);
        } else {
            alert(`Error: ${data.detail || 'Analysis Failed'}`);
        }
    } catch (err) {
        alert('Could not connect to the Backend server. Ensure FastAPI is running.');
    } finally {
        analyzeBtn.disabled = false;
        loader.classList.add('hidden');
        reportContent.classList.remove('hidden');
    }
});

function displayReport(data) {
    // Convert markdown (basic support)
    const formattedBody = data.report.replace(/\n/g, '<br>').replace(/\[([^\]]+)\]/g, '<strong>$1</strong>');
    reportContent.innerHTML = `<div class="fade-in">${formattedBody}</div>`;

    // Metrics
    metricsCard.classList.remove('hidden');
    confidenceValue.innerText = `${data.confidence}%`;
    confidenceFill.style.width = `${data.confidence}%`;

    // PDF
    pdfBase64 = data.pdf_base64;
    downloadBtn.classList.remove('hidden');
}

// Download PDF
downloadBtn.addEventListener('click', () => {
    const link = document.createElement('a');
    link.href = `data:application/pdf;base64,${pdfBase64}`;
    link.download = `SV_MedVision_Report_${Date.now()}.pdf`;
    link.click();
});
