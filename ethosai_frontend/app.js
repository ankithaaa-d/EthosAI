const API_BASE = "http://localhost:8000";
const DEFAULT_KEY = "ethos_default_dev_key";

const urlInput = document.getElementById('url-input');
const analyzeBtn = document.getElementById('analyze-btn');
const loading = document.getElementById('loading');
const results = document.getElementById('results');
const themeToggle = document.getElementById('theme-toggle');
const themeIcon = document.getElementById('theme-icon');

// ── Theme Management ────────────────────────────────────
let isDarkMode = true;

themeToggle.addEventListener('click', () => {
    isDarkMode = !isDarkMode;
    document.body.classList.toggle('light-mode', !isDarkMode);
    themeIcon.innerText = isDarkMode ? "🌙" : "☀️";
    themeToggle.innerHTML = `<span id="theme-icon">${isDarkMode ? "🌙" : "☀️"}</span> ${isDarkMode ? "Dark Mode" : "Light Mode"}`;
    updateChartTheme();
});

// ── Chart Management ────────────────────────────────────
let usageData = [0, 0, 0, 0, 0, 0, 0]; // Mock labels/data
const ctx = document.getElementById('usageChart').getContext('2d');
let usageChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        datasets: [{
            label: 'API Requests',
            data: usageData,
            backgroundColor: '#00ff88',
            borderColor: '#00ff88',
            borderWidth: 1,
            borderRadius: 4
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' }, border: { display: false } },
            x: { grid: { display: false } }
        },
        plugins: { legend: { display: false } }
    }
});

function updateChartTheme() {
    const color = isDarkMode ? 'rgba(255,255,255,0.05)' : 'rgba(0,0,0,0.05)';
    usageChart.options.scales.y.grid.color = color;
    usageChart.update();
}

function recordUsage() {
    const today = new Date().getDay(); // 0 is Sunday, 1 is Monday...
    // Map Sunday(0) to last index, others to index-1 for Mon start
    const index = today === 0 ? 6 : today - 1;
    usageData[index]++;
    usageChart.update();
}

// ── API Integration ─────────────────────────────────────
const statusDot = document.getElementById('status-dot');
const statusLabel = document.getElementById('status-label');
const reasoningText = document.getElementById('reasoning-text');
const signalPermission = document.getElementById('signal-permission');
const signalRisk = document.getElementById('signal-risk');
const policyContent = document.getElementById('policy-content');

analyzeBtn.addEventListener('click', async () => {
    const url = urlInput.value.trim();
    if (!url) {
        alert("Please enter a valid URL");
        return;
    }

    loading.classList.remove('hidden');
    results.style.display = 'none';

    try {
        const response = await fetch(`${API_BASE}/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Ethos-Key': DEFAULT_KEY
            },
            body: JSON.stringify({ url: url })
        });

        const json = await response.json();

        if (json.success) {
            updateUI(json.data);
            recordUsage();
        } else {
            alert("Error: " + (json.error || "Analysis failed"));
        }
    } catch (err) {
        console.error(err);
        alert("Could not connect to EthosAI Backend.");
    } finally {
        loading.classList.add('hidden');
    }
});

function updateUI(data) {
    results.style.display = 'grid';
    const decision = data.decision?.decision || "unknown";
    statusLabel.innerText = "Compliance: " + decision.toUpperCase();
    
    if (decision === 'allowed') {
        statusDot.style.background = 'var(--risk-low)';
        statusDot.style.boxShadow = '0 0 15px var(--risk-low)';
    } else if (decision === 'conditional') {
        statusDot.style.background = 'var(--risk-med)';
        statusDot.style.boxShadow = '0 0 15px var(--risk-med)';
    } else {
        statusDot.style.background = 'var(--risk-high)';
        statusDot.style.boxShadow = '0 0 15px var(--risk-high)';
    }

    reasoningText.innerText = data.reasoning?.explanation || data.reasoning || "Reasoning unavailable.";
    signalPermission.innerText = data.predictions?.permission?.label || "N/A";
    signalRisk.innerText = (data.decision?.risk_score * 100).toFixed(0) + "%";
    const tos = data.tos?.tos_text || "";
    policyContent.innerText = tos.substring(0, 1000) + (tos.length > 1000 ? "..." : "");
}

// ── Initialization ──────────────────────────────────────
document.getElementById('api-url-display').innerText = API_BASE;
document.getElementById('api-key-display').innerText = DEFAULT_KEY;

document.getElementById('copy-btn').addEventListener('click', () => {
    const code = document.getElementById('quick-start-code').innerText;
    navigator.clipboard.writeText(code);
    const btn = document.getElementById('copy-btn');
    btn.innerText = "Copied!";
    setTimeout(() => btn.innerText = "Copy", 2000);
});

urlInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') analyzeBtn.click();
});
