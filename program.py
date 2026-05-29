from openai import OpenAI
from dotenv import load_dotenv

import json
import os
import re

# Load API key from .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("Error: OPENAI_API_KEY not found in .env file")
    print("Copy .env.example to .env and add your key")
    exit(1)

client = OpenAI(api_key=OPENAI_API_KEY)


print("✅ Setup complete!")


def calculate(expression):
    try:
        return json.dumps({"result": eval(expression)})
    except:
        return json.dumps({"error": "Invalid expression"})

def web_search(query):
    results = {
        "ai trends": "Latest AI: Advanced reasoning, multimodal models",
        "technology": "Tech news: AI adoption accelerating",
        "email tips": "Email tips: Clear subject, concise content",
    }
    for keyword in results:
        if keyword in query.lower():
            return json.dumps({"results": results[keyword]})
    return json.dumps({"results": f"No specific results found for: {query}"})

def analyze_data(data_string, operation):
    data = json.loads(data_string)
    if operation == "sum": result = sum(data)
    elif operation == "average": result = sum(data) / len(data)
    elif operation == "max": result = max(data)
    elif operation == "min": result = min(data)
    else: result = None
    return json.dumps({"result": result})

def get_weather(query):
    weather_data = {
        "karachi": "Karachi: 30°C, Sunny",
        "new york": "New York: 22°C, Cloudy",
        "london": "London: 18°C, Rainy"
    }
    for city in weather_data:
        if city in query.lower():
            return json.dumps({"weather": weather_data[city]})
    return json.dumps({"weather": f"Weather info for {query}"})

def translate(text, target_language="spanish"):
    translations = {
        "spanish": {
            "hello": "hola",
            "world": "mundo",
            "good morning": "buenos días"
        },
        "french": {
            "hello": "bonjour",
            "world": "monde",
            "good morning": "bonjour"
        }
    }
    
    lang = target_language.lower()

    if lang not in translations:
        return json.dumps({"translation": f"❌ Language '{target_language}' not supported. Try: spanish or french"})

    lang_dict = translations[lang]
    
    for phrase in lang_dict:
        if phrase in text.lower():
            return json.dumps({"translation": lang_dict[phrase]})
    
    return json.dumps({"translation": f"[{target_language}] Translation of '{text}' not found in dictionary"})

# Tool schema - describes our function to OpenAI

calculator_tool = {
    "type": "function",
    "function": {
        "name": "calculate",
        "description": "Do accurate math calculations",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Math expression like '2+2' or '10*5'"
                }
            },
            "required": ["expression"]
        }
    }
}

print("✅ Calculator tool defined!")

# Tool schema for web search

web_search_tool = {
    "type": "function",
    "function": {
        "name": "web_search",
        "description": "Search for current information",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"}
            },
            "required": ["query"]
        }
    }
}

print("✅ Web search tool defined!")

# Tool schema for data analyzer

data_analyzer_tool = {
    "type": "function",
    "function": {
        "name": "analyze_data",
        "description": "Analyze numeric data",
        "parameters": {
            "type": "object",
            "properties": {
                "data_string": {"type": "string", "description": "JSON list of numbers"},
                "operation": {
                    "type": "string",
                    "enum": ["sum", "average", "max", "min"],
                    "description": "What to calculate"
                }
            },
            "required": ["data_string", "operation"]
        }
    }
}

print("✅ Data analyzer tool defined!")

# Tool schema for weather search

weather_tool = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get weather information for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Name of the city"}
            },
            "required": ["query"]
        }
    }
}

print("✅ Weather tool defined!")

# Tool schema for translator tool

translator_tool = {
    "type": "function",
    "function": {
        "name": "translate",
        "description": "Translate text to another language",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Text to translate"},
                "target_language": {
                    "type": "string",   
                    "description": "Language to translate to (e.g. 'spanish', 'french')"
                }
            },
            "required": ["text"]
        }
    }
}

print("✅ Translator tool defined!")

class SmartSummarizer:
    """
    COMPLETE summarizer with detailed analytics.
    """
    
    def summarize(self, text, style="short"):
        print(f"\n📝 Summarizing ({style} style)...\n")
        
        # Analytics
        word_count = len(text.split())
        sentence_count = text.count('.') + text.count('!') + text.count('?')
        
        # Style instructions
        styles = {
            "short": "1-2 sentences",
            "medium": "A paragraph (3-4 sentences)",
            "detailed": "Multiple paragraphs"
        }
        
        # Get summary
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"Summarize as {styles.get(style, styles['short'])}"},
                    {"role": "user", "content": f"Summarize:\n{text}"}
                ],
                temperature=0.3
            )
            
            summary = response.choices[0].message.content
        except Exception as e:
            print(f"Error occurred while summarizing: {e}")
            return

        summary_words = len(summary.split())
        reduction = ((word_count - summary_words) / word_count * 100)
        
        # Display
        print("=" * 70)
        print("📊 SUMMARY ANALYSIS")
        print("=" * 70)
        print(f"Original: {word_count} words, ~{sentence_count} sentences")
        print(f"Summary: {summary_words} words")
        print(f"Reduction: {reduction:.1f}%")
        print(f"Style: {style.title()}")
        print()
        print("-" * 70)
        print("SUMMARY")
        print("-" * 70)
        print(summary)
        print("-" * 70)

class EnhancedEmailWriter:
    """
    COMPLETE email writer that can research topics.
    """
    
    def __init__(self):
        self.tools = [web_search_tool]
        self.functions = {"web_search": web_search}

    def write(self, description, tone="professional"):
        print(f"\n📧 Writing email: {description}")
        print(f"   Tone: {tone}\n")
        
        system_prompt = f"""You are a professional email writer.
        Write in a {tone} tone.
        If you need current information, use web_search.
        Include subject, greeting, body, closing."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Write email: {description}"}
        ]
        
        # API call
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                tools=self.tools
            )
        except Exception as e:
            print(f"Error occurred while writing email: {e}")
            return
        
        response_message = response.choices[0].message
        
        # Check if AI wants to research
        if response_message.tool_calls:
            messages.append(response_message)
            
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"🔍 Researching: {function_args.get('query', 'N/A')}")
                
                result = self.functions[function_name](**function_args)
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })
            
            # Get final email with research
            try:
                final_response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                )
                return final_response.choices[0].message.content
            except Exception as e:
                print(f"Error occurred while getting final email: {e}")
                return
            
        return response_message.content

class MultiCapabilityAssistant:
    """
    COMPLETE multi-capability assistant.
    
    Features:
    - Chat with memory
    - Enhanced email writer (with research)
    - Smart summarizer (with analytics)
    - Calculator, web search, data analysis, check weather, and translation tools
    
    This is your PROJECT TEMPLATE - customize it!
    """
    
    def __init__(self):
        # All tools
        self.tools = [calculator_tool, web_search_tool, data_analyzer_tool, weather_tool, translator_tool]
        self.functions = {
            "calculate": calculate,
            "web_search": web_search,
            "analyze_data": analyze_data,
            "get_weather": get_weather,
            "translate": translate
        }
        
        # Sub-components
        self.email_writer = EnhancedEmailWriter()
        self.summarizer = SmartSummarizer()
        
        print("✅ Multi-Capability Assistant initialized!")
        print("   Capabilities: Chat, Email, Summarize, Calculate, weather, Search, Analyze, Translate\n")
    
    def route_request(self, request):
        """Decide which capability to use"""
        request_lower = request.lower()
        
        if any(word in request_lower for word in ['email', 'write to', 'compose']):
            return 'email'
        elif any(word in request_lower for word in ['summarize', 'summary']):
            return 'summarize'
        elif any(word in request_lower for word in ['calculate', 'math', 'average', '%', 'percent', 'sum', 'total', 'weather', 'translate']):
            return 'tools'
        else:
            return 'general'
    
    def process(self, request):
        """Process any request intelligently"""
        # print(f"\n{'=' * 70}")
        # print(f"📥 Request: {request}")
        # print("=" * 70)
        
        capability = self.route_request(request)
        # print(f"🎯 Using: {capability.upper()}\n")
        
        if capability == 'email':
            return self.email_writer.write(request)
        elif capability == 'summarize':
            # Check specifically for "summarize:" pattern
            match = re.search(r'summarize\s*:\s*(.+)', request, re.IGNORECASE | re.DOTALL)
            if match:
                text = match.group(1).strip()
            else:
                # No text after summarize — ask the user
                print("📋 Please paste the text you want to summarize:")
                text = input("Text: ").strip()
            
            if not text:
                return "⚠️ Please provide text to summarize. Example: 'summarize: your text here'"
            
            print("📏 Summary style options: short / medium / detailed")
            style = input("Choose style (press Enter for 'short'): ").strip().lower()
            
            if style not in ['short', 'medium', 'detailed']:
                style = 'short'
            
            self.summarizer.summarize(text, style)
            return ""
        elif capability == 'tools':
            return self.use_tools(request)
        else:
            return self.general_assistant(request)
    
    def use_tools(self, query):
        """Use tools to answer query"""
        messages = [{"role": "user", "content": query}]
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                tools=self.tools
            )
            
            response_message = response.choices[0].message
        except Exception as e:
            return f"❌ API Error: {e}"
        
        if not response_message.tool_calls:
            return response_message.content
        
        messages.append(response_message)
        
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            # print(f"🔧 Using {function_name}...")
            
            result = self.functions[function_name](**function_args)
            
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })
        
        final_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        
        return final_response.choices[0].message.content
    
    def general_assistant(self, query):
        """General purpose assistant"""
        messages = [{"role": "user", "content": query}]
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                tools=self.tools
            )
            response_message = response.choices[0].message
        except Exception as e:
            return f"❌ API Error: {e}"
        
        # If no tool call, return content directly
        if not response_message.tool_calls:
            return response_message.content
        
        # Handle tool calls
        messages.append(response_message)
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            result = self.functions[function_name](**function_args)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })
        
        final_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return final_response.choices[0].message.content


def show_help():
    print("""
╔═══════════════════════════════════════════════════════════════════╗
║                    🤖 ASSISTANT HELP MENU                        ║
╠═══════════════════════════════════════════════════════════════════╣
║  CAPABILITIES:                                                    ║
║  📧 Email    → "write an email about..."                         ║
║  📝 Summarize→ "summarize: paste your text here"                 ║
║  💬 Chat     → just type anything!                               ║
║                                                                   ║
║  TOOLS AVAILABLE:                                                 ║
║  🔢 Calculator  → "what is 15% of 200?"                          ║
║  🔍 Web Search  → "search for AI trends"                         ║
║  📊 Data        → "average of [10, 20, 30]"                      ║
║  🌤  Weather    → "weather in karachi"                            ║
║  🌐 Translate   → "translate hello to french"                    ║
║                                                                   ║
║  COMMANDS:                                                        ║
║  help → show this menu                                            ║
║  exit → quit the assistant                                        ║
╚═══════════════════════════════════════════════════════════════════╝
    """)

# Create the assistant
assistant = MultiCapabilityAssistant()



conversation_history = []

print("🤖 Assistant ready! Type 'help' for commands or 'exit' to quit.\n")
show_help()

user_input = input("You: ").strip()

while user_input.lower() != "exit":
    
    # Input validation - reject empty input
    if not user_input:
        print("Please enter something!\n")
        user_input = input("You: ").strip()
        continue

    # ✅ Help command
    if user_input.lower() == "help":
        show_help()
        user_input = input("You: ").strip()
        continue

    # Build history as a single string
    history_text = ""
    for msg in conversation_history:
        role = "User" if msg["role"] == "user" else "Assistant"
        history_text += f"{role}: {msg['content']}\n"
    
    # Inject history into the query itself
    if history_text:
        full_query = f"Previous conversation:\n{history_text}\nNow answer this: {user_input}"
    else:
        full_query = user_input
    
    # Pass to agent as normal — no changes needed in agent
    ai_response = assistant.process(full_query)
    
    # Save original messages to history
    conversation_history.append({"role": "user", "content": user_input})
    conversation_history.append({"role": "assistant", "content": ai_response})
    
    print(f"\nAssistant: {ai_response}\n")
    user_input = input("You: ").strip()


print("👋 Goodbye!")