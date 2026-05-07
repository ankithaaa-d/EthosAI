# EthosAI — The Ethical Firewall for AI Agents 🛡️🤖

![EthosAI Interaction Flow](https://raw.githubusercontent.com/username/repo/main/artifacts/infographic.png)

EthosAI is an intelligent, AI-powered middleware designed to ensure that AI agents interact with the web ethically and legally. It analyzes website policies, robots.txt, and terms of service in real-time, providing an **"Explainable Compliance Score"** that tells AI agents whether to proceed, stop, or seek a license.

## 🌟 Key Features

- **Intelligence Pipeline**: Combines ML Classifiers (PyTorch) with Semantic Legal Analysis.
- **OpenCLAW Integration**: Uses the Open Compliance Legal Analysis Workflow for high-accuracy policy parsing.
- **Explainable AI (XAI)**: Generates detailed natural language reasoning using a locally hosted Llama 3 model (via Ollama).
- **AI-Ready API**: Fully documented REST API with built-in discoverability for GPT Actions and Claude Tools.
- **Premium Dashboard**: A sleek, glassmorphism-based frontend for human researchers to audit compliance manually.
- **Privacy First**: All legal reasoning is processed locally using Ollama—no data is sent to external clouds.

## 🚀 Tech Stack

- **Backend**: FastAPI, Uvicorn, PyTorch, Transformers (MiniLM).
- **Frontend**: HTML5, Vanilla CSS, JS, Chart.js.
- **Reasoning**: Ollama (Llama 3).
- **Database/Vector**: Scikit-Learn (Cosine Similarity Search).

## 🛠️ Installation

### 1. Prerequisites
- Python 3.9+
- [Ollama](https://ollama.com/) (running `llama3`)

### 2. Setup Backend
```bash
# Clone the repo
git clone https://github.com/yourusername/EthosAI.git
cd EthosAI/ethosai

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Start the server
uvicorn main:app --port 8000 --reload
```

### 3. Setup Frontend
Simply open `ethosai_frontend/index.html` in your browser. No build process required!

## 🔌 API Usage

EthosAI is designed to be called programmatically by AI agents.

**Endpoint**: `POST /analyze`
**Header**: `X-Ethos-Key: your_api_key`

```bash
curl -X POST http://localhost:8000/analyze \
     -H "X-Ethos-Key: ethos_default_dev_key" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://example.com"}'
```

## 📊 Interaction Flow

1. **Input**: User/AI sends a URL.
2. **Extraction**: EthosAI fetches Robots.txt, ToS, and Metadata.
3. **ML Inference**: PyTorch models predict permission levels.
4. **Semantic Analysis**: OpenCLAW reasoning via Llama 3 parses legal nuance.
5. **Decision**: Final action (ALLOW/RESTRICT) + Risk Score returned.

## 📜 License
EthosAI is released under the MIT License. See [LICENSE](LICENSE) for details.

---
Built with ❤️ for a more ethical AI-powered web.
