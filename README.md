# 🔬 LangChain Multi-Agent Research System

> **A sophisticated multi-agent AI research system that autonomously researches topics, gathers information, writes reports, and provides critical feedback using specialized AI agents.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-0.2.0+-green.svg)](https://python.langchain.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Usage](#usage)
- [Pipeline Details](#pipeline-details)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

The **LangChain Multi-Agent Research System** is an intelligent research assistant that leverages multiple specialized AI agents working in concert to produce comprehensive research reports. Each agent has a specific role in the research pipeline:

1. **Search Agent** - Finds recent, reliable information using web search
2. **Reader Agent** - Scrapes and extracts detailed content from web sources
3. **Writer Chain** - Synthesizes findings into a structured research report
4. **Critic Chain** - Evaluates and provides feedback on the report quality

This system demonstrates the power of agentic workflows in combining multiple specialized models and tools to accomplish complex research tasks.

## ✨ Features

- **Multi-Agent Orchestration**: Four specialized agents collaborate seamlessly
- **Prompt-Based Tool Calling**: Custom tool invocation system avoiding API compatibility issues
- **Web Search Integration**: Real-time information retrieval via Tavily API
- **Advanced Web Scraping**: Multiple extraction strategies (trafilatura, readability, BeautifulSoup)
- **Intelligent Synthesis**: LLM-powered report generation and quality assessment
- **Beautiful UI**: Modern Streamlit interface with gradient styling and real-time pipeline visualization
- **Robust Error Handling**: Graceful fallbacks for network and extraction failures
- **Environment Flexibility**: Works with LangChain 1.2.17+ and recent Groq API versions

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER INPUT (Topic)                           │
└────────────────────────────┬────────────────────────────────────┘
                             │
                 ┌───────────▼───────────┐
                 │   SEARCH AGENT        │
                 │  (Web Search via      │
                 │   Tavily API)         │
                 └───────────┬───────────┘
                             │
        ┌────────────────────▼─────────────────┐
        │      Search Results Aggregation      │
        └────────────────────┬─────────────────┘
                             │
                 ┌───────────▼───────────┐
                 │   READER AGENT        │
                 │  (URL Scraping with   │
                 │   Multi-Strategy)     │
                 └───────────┬───────────┘
                             │
        ┌────────────────────▼─────────────────┐
        │      Cleaned Content Extraction      │
        └────────────────────┬─────────────────┘
                             │
             ┌───────────────┴───────────────┐
             │                               │
    ┌────────▼──────────┐        ┌──────────▼──────┐
    │  WRITER CHAIN     │        │  CRITIC CHAIN   │
    │ (Report          │        │  (Evaluation &  │
    │  Synthesis)       │        │   Scoring)      │
    └────────┬──────────┘        └──────────┬──────┘
             │                              │
    ┌────────▼──────────────────────────────▼──┐
    │         Final Research Report +           │
    │              Feedback Score               │
    └───────────────────────────────────────────┘
```

## 🛠️ Tech Stack

### Core Framework
- **[LangChain](https://python.langchain.com/)** - LLM orchestration & agent framework
- **[Groq API](https://console.groq.com/)** - Fast LLM inference (mixtral-8x7b)

### Web & Data Processing
- **[Tavily](https://tavily.com/)** - Real-time web search API
- **[BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)** - HTML/XML parsing
- **[Trafilatura](https://trafilatura.readthedocs.io/)** - Content extraction from web pages
- **[Readability](https://github.com/buriy/python-readability)** - Article extraction algorithm
- **[Requests](https://requests.readthedocs.io/)** - HTTP library

### UI & Visualization
- **[Streamlit](https://streamlit.io/)** - Fast web app framework

### Utilities
- **[python-dotenv](https://github.com/theskumar/python-dotenv)** - Environment variable management
- **[Rich](https://rich.readthedocs.io/)** - Rich text and beautiful formatting

## 📦 Installation

### Prerequisites

- **Python 3.10 or higher**
- **pip** or **conda** package manager
- **Groq API Key** - [Get one here](https://console.groq.com/)
- **Tavily API Key** - [Get one here](https://app.tavily.com/)

### Setup Steps

**1. Clone the repository**
```bash
git clone https://github.com/yourusername/LangChain-Multi-Agent-Research-System.git
cd LangChain-Multi-Agent-Research-System
```

**2. Create a virtual environment**

Using conda:
```bash
conda create -n langagent python=3.10 -y
conda activate langagent
```

Or using venv:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

Create a `.env` file in the project root:
```bash
# Groq API Configuration
LLM_MODEL=mixtral-8x7b-32768
LLM_API_KEY=your_groq_api_key_here

# Tavily Search API Configuration
TAVILY_API_KEY=your_tavily_api_key_here
```

## 🚀 Quick Start

### Command Line Research
```bash
python main.py
```

This will execute the full pipeline for the default topic ("The impact of AI on the job market in 2026") and display results in the terminal.

### Interactive Web UI
```bash
streamlit run app.py
```

This launches a beautiful web interface where you can:
- Enter custom research topics
- Watch real-time pipeline execution
- Download research reports as Markdown
- View detailed pipeline visualization

## 📁 Project Structure

```
LangChain-Multi-Agent-Research-System/
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   └── agents.py          # Agent definitions & SimpleAgent class
│   ├── tools/
│   │   ├── __init__.py
│   │   └── tools.py           # web_search() and scrape_url() tools
│   └── pipelines/
│       ├── __init__.py
│       └── pipeline.py        # Main research pipeline orchestration
├── app.py                      # Streamlit UI
├── main.py                     # CLI entry point
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── README.md                  # This file
└── LICENSE                    # MIT License
```

## ⚙️ Configuration

All configuration is managed through environment variables in the `.env` file:

| Variable | Description | Example |
|----------|-------------|---------|
| `LLM_MODEL` | Groq model ID | `mixtral-8x7b-32768` |
| `LLM_API_KEY` | Groq API authentication token | `gsk_...` |
| `TAVILY_API_KEY` | Tavily search API key | `tvly_...` |

## 💡 Usage

### As a Python Library

```python
from src.pipelines.pipeline import run_research_pipeline

# Run the research pipeline
topic = "Impact of quantum computing on cryptography"
results = run_research_pipeline(topic)

# Access results
print("Search Results:", results["search_results"])
print("Scraped Content:", results["scraped_content"])
print("Report:", results["report"])
print("Feedback:", results["feedback"])
```

### Via Command Line

```bash
# Run with default topic
python main.py

# Edit main.py to change the topic
# Line 3: topic = "Your custom topic here"
```

### Via Streamlit Dashboard

```bash
streamlit run app.py
```

Then navigate to `http://localhost:8501` and enter your research topic in the input box.

## 🔄 Pipeline Details

### Step 1: Search Agent
- **Purpose**: Find recent, reliable information on the topic
- **Tool Used**: Tavily web search API
- **Output**: Aggregated search results with titles, URLs, and snippets
- **Model**: Groq LLM with prompt-guided tool calling

### Step 2: Reader Agent
- **Purpose**: Extract deep, detailed content from top search results
- **Tools Used**: Multiple extraction strategies
  - Trafilatura (best for articles/blogs)
  - Readability (DOM-based extraction)
  - BeautifulSoup (fallback HTML parsing)
- **Output**: Cleaned, readable content from selected URLs
- **Resilience**: Handles 403 errors, timeouts, and parsing failures gracefully

### Step 3: Writer Chain
- **Purpose**: Synthesize search and scraped content into a structured report
- **Structure**:
  - Introduction
  - Key Findings (minimum 3 well-explained points)
  - Conclusion
  - Sources
- **Model**: Groq LLM with structured prompt
- **Output**: Professional research report in Markdown format

### Step 4: Critic Chain
- **Purpose**: Evaluate report quality and provide constructive feedback
- **Evaluation Criteria**:
  - Report quality (1-10 score)
  - Strengths
  - Areas for improvement
  - Overall verdict
- **Model**: Groq LLM
- **Output**: Detailed feedback and quality assessment

## 🛑 Tool Calling Mechanism

This system uses a **prompt-based tool calling approach** instead of native API function calling:

1. Agent receives user input and tool descriptions
2. System prompt instructs model to use structured format: `<TOOL_CALL>tool_name: X parameters: {...}</TOOL_CALL>`
3. Model responds with tool call in structured format
4. Agent regex-extracts and executes the tool
5. Tool results are fed back to model for final synthesis

This approach avoids Groq API incompatibilities with `bind_tools()` and provides better control over tool execution.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit (`git commit -m 'Add amazing feature'`)
5. Push to branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

### Development Setup

```bash
# Install with dev dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Format code
black src/

# Lint code
flake8 src/
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

Created with ❤️ for AI research automation

## 🙏 Acknowledgments

- [LangChain](https://python.langchain.com/) for the agent framework
- [Groq](https://groq.com/) for fast LLM inference
- [Tavily](https://tavily.com/) for web search capabilities
- [Streamlit](https://streamlit.io/) for the UI framework

## 📞 Support

For issues, questions, or suggestions:
- Open an [Issue](https://github.com/yourusername/LangChain-Multi-Agent-Research-System/issues)
- Start a [Discussion](https://github.com/yourusername/LangChain-Multi-Agent-Research-System/discussions)

---

**Made with ⚡ by LangChain enthusiasts**