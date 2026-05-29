# 🤖 Multi-Capability AI Assistant

A smart assistant that can write emails, summarize text,
answer questions, and use multiple tools — all from a 
simple chat interface.

---

## 🚀 Installation

1. Clone the repository
2. Install dependencies:
   pip install -r requirements.txt
3. Copy the env template:
   cp .env.example .env
4. Add your OpenAI API key to .env:
   OPENAI_API_KEY=your-key-here
5. Run the assistant:
   python assistant.py

---

## 💡 Capabilities

### 📧 Email Writer
Writes professional emails on any topic.
Researches the topic before writing if needed.
Supports formal, friendly, and casual tones.
Example: "write an email about meeting postponement"

### 📝 Smart Summarizer
Summarizes any text with analytics.
Shows word count and reduction percentage.
Supports short, medium, and detailed styles.
Example: "summarize: your text here"

### 💬 Chat Assistant
General purpose chat with conversation memory.
Remembers previous messages in the session.
Can answer follow-up questions naturally.
Example: just type anything!

---

## 🛠️ Tools

| Tool         | What it does                        | Example                        |
|--------------|-------------------------------------|--------------------------------|
| Calculator   | Accurate math calculations          | "what is 15% of 200"          |
| Web Search   | Search for current information      | "search for AI trends"        |
| Data Analyzer| Sum, average, max, min of numbers   | "average of [10, 20, 30]"     |
| Weather      | Get weather for a city              | "weather in karachi"          |
| Translator   | Translate text to another language  | "translate hello to french"   |

---

## 💬 Commands

| Command | Action                  |
|---------|-------------------------|
| help    | Show the help menu      |
| exit    | Quit the assistant      |

---

## 📁 File Structure

my-ai-assistant/
├── assistant.py       # Main program
├── README.md          # Documentation
├── requirements.txt   # Dependencies
├── .env               # Your API key (not on GitHub)
├── .env.example       # API key template
└── examples.txt       # Example interactions