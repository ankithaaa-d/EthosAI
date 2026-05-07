# EthosAI — The Ethical Firewall for AI Agents 🛡️🤖

**EthosAI** is a high-performance, AI-powered middleware platform that acts as an ethical layer between AI agents and the web. It ensures that automated systems interact with websites in compliance with legal terms, `robots.txt` instructions, and ethical standards.

---

## 🛑 The Problem
As AI agents (LLMs, crawlers, and autonomous bots) increasingly navigate the web, they often ignore the "rules of the road." 
- **Legal Risk**: Bots frequently violate Terms of Service (ToS), leading to potential litigation.
- **Ethical Gaps**: Standard scrapers don't understand the *intent* of a website's restrictions.
- **Complexity**: Manually parsing `robots.txt` and legal jargon is impossible for agents in real-time.
- **Data Privacy**: Sending policy data to external clouds for analysis creates a secondary privacy risk.

## 💡 The Solution
EthosAI provides a real-time **Ethical Firewall** that translates complex legal and technical policies into a simple, actionable **Compliance Score**.
- **OpenCLAW Integration**: Uses the Open Compliance Legal Analysis Workflow for precision.
- **ML-Powered**: Leverages PyTorch-based classifiers to detect restrictive patterns.
- **Explainable AI (XAI)**: Generates natural language reasoning using local Llama 3 via Ollama, explaining *why* an action is allowed or denied.
- **Privacy First**: All processing is local. Your browsing/scraping intent never leaves your infrastructure.

---

## ⚙️ Setup

### Prerequisites
- **Python**: Version 3.9 or higher.
- **Ollama**: Required for local reasoning. [Download Ollama here](https://ollama.com/).
  - After installing, run: `ollama pull llama3`

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/EthosAI.git
cd EthosAI
```

### 2. Backend Configuration
```bash
cd ethosai
python -m venv .venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

### 3. Frontend Configuration
The frontend is a lightweight, high-performance dashboard. No installation is required; it connects directly to your local backend.

---

## 📖 Instructions

### Running the Backend
Start the FastAPI server using Uvicorn:
```bash
cd ethosai
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
The API documentation will be available at `http://localhost:8000/docs`.

### Launching the Dashboard
Open the management interface to monitor AI agent compliance in real-time:
1. Navigate to the `ethosai_frontend` folder.
2. Open `index.html` in any modern web browser (Chrome, Firefox, or Edge).

---

## 🚀 Usage

### Integrating with AI Agents
AI agents can query EthosAI before performing any web action.

**Endpoint**: `POST /analyze`  
**Auth**: `X-Ethos-Key: your_api_key`

#### Example Request
```bash
curl -X POST http://localhost:8000/analyze \
     -H "X-Ethos-Key: ethos_default_dev_key" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com"}'
```

#### Example Response
```json
{
  "url": "https://example.com",
  "status": "RESTRICTED",
  "score": 0.2,
  "reasoning": "The website's terms of service explicitly prohibit AI training and commercial scraping. Robots.txt disallows all user-agents from the /data/ directory.",
  "timestamp": "2024-05-07T23:13:26Z"
}
```

---
*Built for a transparent, ethical, and agent-friendly web.*
