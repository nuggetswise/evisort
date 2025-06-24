# 🧭 Workday PM Role Demo - Contract Intelligence

A comprehensive Streamlit application that demonstrates deep understanding of the Workday Contract Intelligence Product Manager role and simulates an Evisort-style contract intelligence product powered by AI components.

## 🎯 Overview

This app showcases:
- **Role Analysis**: Deep understanding of the Workday PM position requirements
- **Product Simulation**: Evisort-style contract intelligence capabilities
- **AI Copilot**: Strategic PM assistant for decision-making
- **Personal Fit**: Experience alignment and strategic recommendations

## 🚀 Features

### 📋 Section 1: Role Decoder
- Parse and analyze the Workday job posting
- Extract core responsibilities, AI/ML focus areas, and required skills
- Identify key metrics and success indicators
- Assess role complexity and challenges

### 📄 Section 2: Contract AI Simulator
- Upload and analyze contract documents (PDF, DOCX, TXT)
- Simulate AI-powered clause extraction and metadata identification
- Risk assessment and compliance checking
- Performance analytics and benchmarking

### 🧠 Section 3: Agent Copilot
- AI-powered PM assistant for strategic questions
- Quick questions for common PM scenarios
- Custom question input for specific challenges
- Strategic insights and market analysis

### 💼 Section 4: My Fit for the Role
- Experience overview and skills alignment
- Strategic narrative connecting background to role requirements
- Gap analysis with mitigation strategies
- Key achievements and metrics demonstration

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd workday-pm-demo
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:8501`

### Optional: API Keys Setup

For enhanced AI capabilities, you can add API keys to `st.secrets` or environment variables. The app uses providers in this priority order:

1. **OpenAI** (GPT-4) - Primary choice
2. **Cohere** - Fast, reliable alternative
3. **Groq** - Ultra-fast inference
4. **Gemini** - Google's AI model

```bash
# Environment variables
export OPENAI_API_KEY="your-openai-key"
export COHERE_API_KEY="your-cohere-key"
export GROQ_API_KEY="your-groq-key"
export GEMINI_API_KEY="your-gemini-key"
```

Or create a `.streamlit/secrets.toml` file:
```toml
openai_api_key = "your-openai-key"
cohere_api_key = "your-cohere-key"
groq_api_key = "your-groq-key"
gemini_api_key = "your-gemini-key"
```

**Note**: The app works in demo mode without API keys, using mock responses for demonstration purposes.

## 📁 Project Structure

```
workday-pm-demo/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── DEPLOYMENT.md         # Deployment guide
├── components/           # App components
│   ├── __init__.py
│   ├── role_decoder.py   # Role analysis component
│   ├── contract_simulator.py  # Contract AI simulator
│   ├── agent_copilot.py  # AI PM assistant
│   └── fit_analyzer.py   # Personal fit analysis
└── utils/               # Utility modules
    ├── __init__.py
    ├── config.py        # Configuration management
    └── llm_client.py    # AI client management
```

## 🎨 Key Features

### AI-Powered Analysis
- **Multi-provider support**: OpenAI, Cohere, Groq, Gemini
- **Priority-based fallback**: Tries providers in order of preference
- **Fallback system**: Mock responses when APIs unavailable
- **Context-aware responses**: Tailored to contract intelligence domain

### Interactive UI
- **Tabbed navigation**: Clean, organized interface
- **Real-time processing**: Live contract analysis
- **Visual analytics**: Charts and metrics visualization
- **Responsive design**: Works on desktop and mobile

### Document Processing
- **Multi-format support**: PDF, DOCX, TXT files
- **Text extraction**: Automatic content parsing
- **Structured output**: Organized analysis results

## 🔧 Customization

### Adding New Components
1. Create a new Python file in the `components/` directory
2. Implement a class with a `render()` method
3. Import and add to the main app in `app.py`

### Modifying AI Responses
Edit the `_generate_mock_response()` method in `utils/llm_client.py` to customize demo responses.

### Styling Changes
Modify the CSS in the `app.py` file or add custom stylesheets.

## 🚀 Deployment

### Local Development
```bash
streamlit run app.py
```

### Streamlit Cloud
1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Deploy with environment variables for API keys

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

## 📊 Demo Mode

The app includes comprehensive demo functionality:
- **Mock contract analysis**: Sample contract with realistic AI output
- **Simulated conversations**: Pre-built PM scenarios
- **Sample metrics**: Realistic performance data
- **Strategic insights**: Market analysis and recommendations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is for demonstration purposes. Please respect the terms of use for any third-party APIs or services.

## 🆘 Support

For issues or questions:
1. Check the demo mode functionality
2. Verify API key configuration
3. Review the console for error messages
4. Ensure all dependencies are installed

---

**Note**: This is a demonstration application. All AI-generated content is for illustrative purposes and should not be used for actual legal or business decisions. 