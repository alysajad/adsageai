# AdSageAI (RigtusHuddle)

**AdSageAI** is a cutting-edge, **Multi-Agent Marketing System** designed to optimize social media campaigns using advanced AI personas and real-time data. It leverages Google's Gemini models to simulate a diverse marketing team—Gen Z, Millennial, and Strategist—negotiating the best approach for your content.

---

## 🚀 Key Features

*   **Multi-Persona Agentic Core**: Run parallel analysis using distinct AI personas (Youth vs. Adult) to get diverse feedback on a single campaign.
*   **"Human-in-the-Loop" Logic**: A specialized **Strategist Agent** synthesizes conflicting viewpoints from other agents to propose a balanced, actionable strategy.
*   **Visual Predictive Analysis**: Uses **Gemini Vision (Multimodal)** to "see" your draft images and predict engagement scores, emotional impact, and virality potential before you post.
*   **Dynamic Intelligence**:
    *   **Real-time Hashtag Scraping**: Automatically scrapes live, trending hashtags from the web based on AI-generated search queries (bypassing the knowledge cutoff of LLMs).
    *   **Structured Output**: Enforces strict JSON schemas for UI rendering, turning unstructured AI thoughts into dynamic dashboards.

---

## 🛠️ Technical Architecture

### Backend Stack
*   **Runtime**: Python 3.12+
*   **Framework**: Flask (REST API)
*   **AI Engine**: Google Gemini 1.5 Flash / Pro (via `google-genai` SDK)
*   **Scraping**: `BeautifulSoup4` + `requests` (Targeting best-hashtags.com dynamically)
*   **Image Processing**: `Pillow` (PIL)
*   **API Communication**: RESTful endpoints with CORS enabled.

### Frontend Stack
*   **Framework**: Vanilla JavaScript (ES6+), HTML5, CSS3.
*   **Design**: Custom CSS Grid/Flexbox layout (No heavy framework overhead).
*   **Communication**: `Fetch API` for async non-blocking calls to the backend.

### Project Structure
```bash
RigtusHuddle/
├── backend/
│   └── agent/
│       ├── server.py            # Flask API Entry Point
│       ├── agent_core.py        # Main Agent Orchestrator (The Brain)
│       ├── hashtag_scraper.py   # Real-time Web Scraper Tool
│       ├── prompts/             # System Instructions for Agents
│       │   ├── analyze_campaign.prompt (Youth Persona)
│       │   ├── analyze_campaign_adult.prompt (Adult Persona)
│       │   ├── negotiate_suggestions.prompt (Strategist)
│       │   └── predictive_analysis.prompt (Vision Agent)
│       └── tools/               # Helper modules (Image Gen, LinkedIn API)
├── UI/
│   ├── dashboard.html           # Main User Interface
│   ├── app.js                   # Client-side Logic
│   └── style.css                # Styling
└── requirements.txt             # Python Dependencies
```

---

## 📦 Installation & Setup

### Prerequisites
*   Python 3.10 or higher
*   A Google Cloud API Key (for Gemini)

### 1. Clone the Repository
```bash
git clone https://github.com/alysajad/adsageai.git
cd adsageai/RigtusHuddle
```

### 2. Install Dependencies
It is recommended to use a virtual environment.
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 3. Configure Environment
Create a `.env` file in the `RigtusHuddle` root directory:
```ini
GOOGLE_API_KEY=your_actual_api_key_here
LINKEDIN_CLIENT_ID=optional_for_posting
LINKEDIN_CLIENT_SECRET=optional_for_posting
```

---

## 🚦 Usage Guide

### 1. Start the Backend API
Navigate to the agent directory and run the Flask server:
```bash
cd backend/agent
python server.py
# Server runs on http://localhost:5000
```

### 2. Start the Frontend
Open a new terminal, navigate to the `UI` directory, and start a simple HTTP server:
```bash
cd ../../UI
python -m http.server 8000
# Access dashboard at http://localhost:8000/dashboard.html
```

### 3. Run a Campaign Analysis
1.  Open `http://localhost:8000/dashboard.html`.
2.  **Text Campaign**: Enter a description of your product or campaign idea.
    *   *System Action*: The Youth and Adult agents will analyze it. The Strategist will merge their insights and display a strategy.
3.  **Draft Analysis**: Upload an image and add a caption.
    *   *System Action*: The Vision Agent will predict the "Engagement Score" (1-10) and suggest live hashtags. Note how the hashtags are fetched dynamically from the web!

---

## 🔌 API Reference

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/analyze` | `POST` | Triggers the multi-agent negotiation flow (Youth + Adult + Strategist). |
| `/analyze_draft` | `POST` | Uploads an image for predictive visual analysis & hashtag scraping. |
| `/generate_image_for_post` | `POST` | Generates a new image asset based on a text prompt. |
| `/status` | `GET` | Checks system health and API connections. |

---

## 🤝 Contributing
1.  Fork the repo.
2.  Create your feature branch (`git checkout -b feature/amazing-feature`).
3.  Commit your changes (`git commit -m 'Add amazing feature'`).
4.  Push to the branch (`git push origin feature/amazing-feature`).
5.  Open a Pull Request.

---

**Built with ❤️ for the AI Agent Hackathon.**
