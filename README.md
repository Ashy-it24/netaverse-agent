# Politician Activity Analyzer

A free, live data-fetching AI system that analyzes politicians' recent activities, promise fulfillment, and legislative achievements using public information sources.

## Features

- **Real API Data**: Fetches live data from Congress.gov, Wikipedia, Ballotpedia, and NewsAPI
- **AI-Powered Analysis**: Uses Groq LLM to analyze promise fulfillment and activity impact
- **Politician-Specific Data**: Each politician gets unique, real data instead of generic samples
- **Clean UI**: Simple React interface for searching and viewing results
- **Safety First**: Only analyzes publicly available information

## Architecture

```
backend/
├── agents/
│   ├── fetch_agent.py      # Data fetching from public APIs (Congress.gov, Wikipedia, Ballotpedia, NewsAPI)
│   └── reasoning_agent.py  # LLM analysis and promise fulfillment assessment
├── services/
│   └── llm_service.py      # Groq LLM integration
├── main.py                 # FastAPI application
└── requirements.txt

frontend/                   # React search interface
├── src/
│   ├── App.jsx
│   └── App.css
├── package.json
└── vite.config.js
```

## Data Sources

- **Congress.gov API**: Real legislative bills and voting records
- **Wikipedia API**: Politician biographies and political positions
- **Ballotpedia API**: Comprehensive politician profiles and policy positions
- **NewsAPI**: Recent news articles and current activities
- **RSS Feeds**: BBC Politics, Reuters for additional context

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- API Keys: Groq, Congress.gov, NewsAPI (all free tiers available)

### 1. Clone and Setup Environment
```bash
git clone <repository-url>
cd netaverse_mvp

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Backend Setup
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp ../.env.example ../.env  # Copy example env file
# Edit .env with your API keys (see Environment Variables section below)
```

### 3. Frontend Setup
```bash
cd ../frontend

# Install dependencies
npm install
```

### 4. Configure API Keys

Create a `.env` file in the root directory with the following variables:

```bash
# Required: Groq API for LLM analysis (free tier available)
GROQ_API_KEY=your_groq_api_key_here

# Optional: Congress.gov API for legislative data (free)
CONGRESS_API_KEY=your_congress_api_key_here

# Optional: NewsAPI for current activities (free tier available)
NEWSAPI_KEY=your_newsapi_key_here
```

**Get API Keys:**
- **Groq**: https://console.groq.com/ (free tier)
- **Congress.gov**: https://www.congress.gov/ (free)
- **NewsAPI**: https://newsapi.org/ (free tier: 100 requests/day)

### 5. Run the Application

**Option A: Development Mode (Recommended)**
```bash
# Terminal 1: Backend
cd backend
PYTHONPATH=/Users/aswanthb/netaverse_mvp/backend /Users/aswanthb/netaverse_mvp/venv/bin/python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

**Option B: Production Mode**
```bash
# Backend
cd backend
PYTHONPATH=/Users/aswanthb/netaverse_mvp/backend /Users/aswanthb/netaverse_mvp/venv/bin/python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000

# Frontend
cd frontend
npm run build
npm run preview
```

### 6. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Usage

1. Open http://localhost:5173 in your browser
2. Enter a politician's name (e.g., "Joe Biden", "Donald Trump", "Kamala Harris")
3. Click "Analyze" to fetch real data and AI analysis
4. View categorized activities, promise fulfillment status, and legislative achievements

## API Endpoints

- `GET /`: Health check
- `GET /analyze?name=POLITICIAN_NAME`: Analyze politician activities and promises
- `GET /docs`: Interactive API documentation

## Testing the API

Test with curl:
```bash
# Test Joe Biden analysis
curl -s "http://localhost:8000/analyze?name=Joe%20Biden" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print('=== ANALYSIS RESULTS ===')
print('Promises:')
for p in data.get('promises', []):
    print(f'  {p[\"promise\"]} -> {p[\"status\"]}')
print('Bills:')
for b in data.get('bills', []):
    print(f'  {b[\"title\"]} ({b[\"year\"]})')
"
```

## Troubleshooting

### Backend Issues
- **Module not found**: Ensure `PYTHONPATH` is set correctly
- **API key errors**: Check `.env` file and API key validity
- **Port conflicts**: Change port with `--port 8001`

### Frontend Issues
- **Port 5173 busy**: Vite will suggest an alternative port
- **CORS errors**: Backend must be running on port 8000
- **Build errors**: Run `npm install` again

### Common API Issues
- **Congress.gov**: May have rate limits, has fallback to Wikipedia
- **NewsAPI**: Free tier limited to 100 requests/day
- **All APIs**: System falls back gracefully to curated politician-specific data

## Environment Variables

| Variable | Required | Description | Get Key |
|----------|----------|-------------|---------|
| `GROQ_API_KEY` | Yes | LLM analysis | https://console.groq.com/ |
| `CONGRESS_API_KEY` | No | Legislative data | https://www.congress.gov/ |
| `NEWSAPI_KEY` | No | Current activities | https://newsapi.org/ |

## Technologies Used

- **Backend**: FastAPI, Python 3.8+
- **AI**: Groq (Llama 3.1 70B)
- **Frontend**: React 18, Vite
- **APIs**: Congress.gov, Wikipedia, Ballotpedia, NewsAPI
- **Deployment**: Local development (cloud-ready)

## Safety & Ethics

- Only uses publicly available information
- No web scraping of paywalled content
- No training of custom ML models
- Transparent analysis with clear sourcing
- Respects API terms of service and rate limits

## Future Enhancements

- Add more international politician support
- Implement result caching for better performance
- Add export functionality for reports
- Support for additional news sources
- Real-time activity monitoring