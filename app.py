import os
from fastapi import FastAPI, Form
from fastapi.responses import Response, HTMLResponse
from twilio.twiml.messaging_response import MessagingResponse
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Team Samay | WhatsApp Chatbot Hub</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0b0f19;
            --card-bg: rgba(17, 24, 39, 0.7);
            --border-color: rgba(255, 255, 255, 0.08);
            --accent-primary: #6366f1;
            --accent-secondary: #a855f7;
            --text-primary: #f3f4f6;
            --text-secondary: #9ca3af;
            --success-color: #10b981;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-primary);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow-x: hidden;
            position: relative;
        }

        .bg-glow {
            position: absolute;
            width: 500px;
            height: 500px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(99, 102, 241, 0.15) 0%, rgba(168, 85, 247, 0.05) 50%, transparent 100%);
            z-index: 0;
            pointer-events: none;
        }
        .glow-1 { top: -10%; left: -10%; }
        .glow-2 { bottom: -10%; right: -10%; }

        .container {
            width: 100%;
            max-width: 650px;
            padding: 24px;
            z-index: 1;
        }

        .card {
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border-color);
            border-radius: 24px;
            padding: 40px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        }

        .header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 30px;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 20px;
        }

        .logo-area {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .logo-icon {
            background: linear-gradient(135deg, var(--accent-primary), var(--accent-secondary));
            width: 44px;
            height: 44px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
        }

        h1 {
            font-family: 'Outfit', sans-serif;
            font-size: 24px;
            font-weight: 800;
            background: linear-gradient(to right, #ffffff, #d1d5db);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .status-badge {
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.2);
            color: var(--success-color);
            padding: 6px 14px;
            border-radius: 99px;
            font-size: 13px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .pulse-dot {
            width: 8px;
            height: 8px;
            background-color: var(--success-color);
            border-radius: 50%;
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% {
                transform: scale(0.95);
                box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
            }
            70% {
                transform: scale(1);
                box-shadow: 0 0 0 8px rgba(16, 185, 129, 0);
            }
            100% {
                transform: scale(0.95);
                box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
            }
        }

        .content {
            margin-bottom: 30px;
        }

        .intro-text {
            color: var(--text-secondary);
            font-size: 15px;
            line-height: 1.6;
            margin-bottom: 24px;
        }

        .label {
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--accent-primary);
            margin-bottom: 8px;
            display: block;
        }

        .webhook-box {
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 16px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 24px;
            font-family: 'Courier New', Courier, monospace;
            font-size: 14px;
        }

        .webhook-url {
            color: #38bdf8;
            overflow-x: auto;
            white-space: nowrap;
            width: 85%;
        }

        .copy-btn {
            background: transparent;
            border: none;
            color: var(--text-secondary);
            cursor: pointer;
            padding: 4px 8px;
            border-radius: 6px;
            transition: all 0.2s;
        }

        .copy-btn:hover {
            color: var(--text-primary);
            background: rgba(255, 255, 255, 0.05);
        }

        .steps-container {
            display: flex;
            flex-direction: column;
            gap: 16px;
        }

        .step-item {
            display: flex;
            gap: 16px;
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.03);
            padding: 16px;
            border-radius: 16px;
        }

        .step-num {
            background: rgba(99, 102, 241, 0.1);
            color: var(--accent-primary);
            width: 28px;
            height: 28px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 14px;
            flex-shrink: 0;
        }

        .step-content h3 {
            font-size: 15px;
            font-weight: 600;
            margin-bottom: 4px;
        }

        .step-content p {
            font-size: 13px;
            color: var(--text-secondary);
            line-height: 1.5;
        }

        .footer-logo {
            text-align: center;
            font-size: 12px;
            color: var(--text-secondary);
            margin-top: 30px;
            border-top: 1px solid var(--border-color);
            padding-top: 20px;
        }

        .footer-logo span {
            color: var(--accent-secondary);
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="bg-glow glow-1"></div>
    <div class="bg-glow glow-2"></div>
    
    <div class="container">
        <div class="card">
            <div class="header">
                <div class="logo-area">
                    <div class="logo-icon">🤖</div>
                    <div>
                        <h1>Team Samay</h1>
                        <span style="font-size: 11px; color: var(--text-secondary);">WhatsApp AI Assistant Hub</span>
                    </div>
                </div>
                <div class="status-badge">
                    <span class="pulse-dot"></span>
                    Online
                </div>
            </div>
            
            <div class="content">
                <p class="intro-text">
                    This is your live, production-ready server hosting the Team Samay WhatsApp Chatbot. Copy the webhook URL below and configure it in Twilio to start chatting with your AI assistant.
                </p>
                
                <span class="label">Twilio Webhook URL</span>
                <div class="webhook-box">
                    <div class="webhook-url" id="webhookUrl">Loading...</div>
                    <button class="copy-btn" onclick="copyWebhook()">Copy</button>
                </div>
                
                <span class="label">Quick Start Instructions</span>
                <div class="steps-container">
                    <div class="step-item">
                        <div class="step-num">1</div>
                        <div class="step-content">
                            <h3>Configure Webhook in Twilio</h3>
                            <p>Paste the webhook URL copied above into your Twilio Sandbox Settings under the <strong>"When a message comes in"</strong> section (set to HTTP POST).</p>
                        </div>
                    </div>
                    <div class="step-item">
                        <div class="step-num">2</div>
                        <div class="step-content">
                            <h3>Connect the Sandbox</h3>
                            <p>Send the join code (e.g. <code>join choice-pattern</code>) from your phone to your Twilio WhatsApp number.</p>
                        </div>
                    </div>
                    <div class="step-item">
                        <div class="step-num">3</div>
                        <div class="step-content">
                            <h3>Chat with AI</h3>
                            <p>Send a message like <code>hi</code> or <code>menu</code> to start navigating the chatbot services.</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="footer-logo">
                Designed & Developed by <span>Team Samay</span>
            </div>
        </div>
    </div>

    <script>
        const currentOrigin = window.location.origin;
        document.getElementById('webhookUrl').innerText = `${currentOrigin}/whatsapp`;

        function copyWebhook() {
            const urlText = document.getElementById('webhookUrl').innerText;
            navigator.clipboard.writeText(urlText).then(() => {
                const btn = document.querySelector('.copy-btn');
                btn.innerText = 'Copied!';
                btn.style.color = '#10b981';
                setTimeout(() => {
                    btn.innerText = 'Copy';
                    btn.style.color = '';
                }, 2000);
            });
        }
    </script>
</body>
</html>"""
    return HTMLResponse(content=html_content, status_code=200)

# Initialize Groq client
groq_api_key = os.getenv("GROQ_API_KEY")
groq_model = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
groq_client = None

if groq_api_key and groq_api_key != "your_groq_api_key_here":
    try:
        groq_client = Groq(api_key=groq_api_key)
    except Exception as e:
        print(f"Error initializing Groq client: {e}")

# Initialize Twilio Client for optional native interactive messages
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
whatsapp_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
menu_template_sid = os.getenv("TWILIO_MENU_TEMPLATE_SID")

use_native_templates = False
twilio_client = None

if account_sid and auth_token and whatsapp_number and menu_template_sid:
    # Ensure they are not placeholder values
    if "your_twilio" not in account_sid and "your_twilio" not in auth_token and menu_template_sid.strip():
        try:
            from twilio.rest import Client
            twilio_client = Client(account_sid, auth_token)
            use_native_templates = True
        except Exception as e:
            print(f"Error initializing Twilio client: {e}")

# In-memory session store
# Schema: { phone_number: { "mode": "MENU" | "CHAT" | "AI_SERVICES" | "FULL_STACK", "history": [...] } }
sessions = {}

SYSTEM_PROMPT = """You are a helpful, expert AI assistant representing "Team Samay".
Founder: Samay (Contact Number: 9764096358)
About Team Samay: We are a high-end software development and AI engineering agency.
Services we offer:
1. AI Engineering: Custom LLM integrations, building intelligent AI agents, RAG (Retrieval-Augmented Generation) systems, vector database setups (Pinecone, Chroma, pgvector), fine-tuning, and AI workflow automation.
2. Full-Stack Development: Building modern web and mobile applications from scratch, using technologies like React, Next.js, TailwindCSS, FastAPI, Node.js, PostgreSQL, MongoDB, and Cloud architectures (AWS/GCP).
3. Technical Consulting: Architecture design, database optimization, and scaling software systems.

Guidelines for conversation:
- Adopt a professional, friendly, and expert persona.
- Keep answers relatively concise and easy to read on WhatsApp (use bullet points, emojis, bold text for headings, but keep overall length suitable for mobile screen).
- If the user asks about the founder, say that Samay is an expert AI engineer and full-stack developer who leads a team of top-tier software engineers to build state-of-the-art tech. Share his phone number (9764096358) if they ask for contact details.
- Encourage users to schedule a consultation or ask questions.
- Address the user naturally and refer to the services offered.
- If the user wants to return to the options, tell them they can type *menu* at any time.
"""

WELCOME_MENU = (
    "👋 *Welcome to Team Samay AI Assistant!*\n\n"
    "We help you build state-of-the-art AI solutions and full-stack software applications. "
    "Here are the options you can choose from:\n\n"
    "1️⃣ *AI Engineering Services* (Agents, LLMs, RAG, etc.)\n"
    "2️⃣ *Full-Stack Development* (Web, Mobile, Cloud, APIs)\n"
    "3️⃣ *Contact Founder (Samay)* (Get in touch / Consultation)\n"
    "4️⃣ *Chat with AI* (Ask me anything about technology or our work)\n\n"
    "Please reply with a number (*1*, *2*, *3*, or *4*) or type *menu* at any time to return here."
)

def create_twiml_response(text: str) -> str:
    """Helper to wrap response text in Twilio TwiML format."""
    response = MessagingResponse()
    response.message(text)
    return str(response)

async def get_groq_response(user_id: str, prompt: str) -> str:
    """Send conversation history to Groq and return the AI response."""
    if not groq_client:
        return (
            "🤖 *Team Samay AI Assistant (Demo Mode)*\n\n"
            "The Groq API key is not configured yet. "
            "Please check the `.env` file in the project directory to set `GROQ_API_KEY`.\n\n"
            f"You said: {prompt}"
        )
    
    # Initialize history if not present
    if "history" not in sessions[user_id]:
        sessions[user_id]["history"] = []
        
    # Add user message to history
    sessions[user_id]["history"].append({"role": "user", "content": prompt})
    
    # Limit history to the last 10 messages to manage context size
    history = sessions[user_id]["history"][-10:]
    
    try:
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history
        
        chat_completion = groq_client.chat.completions.create(
            messages=messages,
            model=groq_model,
            max_tokens=512,
            temperature=0.7,
        )
        
        reply = chat_completion.choices[0].message.content.strip()
        # Add assistant reply to history
        sessions[user_id]["history"].append({"role": "assistant", "content": reply})
        return reply
    except Exception as e:
        print(f"Groq API error: {e}")
        return f"Sorry, I encountered an error communicating with the AI. Details: {str(e)}"

@app.post("/whatsapp")
async def whatsapp(
    Body: str = Form(""),
    From: str = Form(""),
    To: str = Form("")
):
    incoming_msg = Body.strip()
    user_id = From

    # 1. Initialize session if new
    if user_id not in sessions:
        sessions[user_id] = {"mode": "MENU", "history": []}

    # 2. Intercept command to return to menu
    if incoming_msg.lower() in ["menu", "help", "hello", "hi", "hey", "start"]:
        sessions[user_id] = {"mode": "MENU", "history": []}
        
        if use_native_templates:
            try:
                twilio_client.messages.create(
                    content_sid=menu_template_sid,
                    from_=To,
                    to=From
                )
                return Response(content=str(MessagingResponse()), media_type="application/xml")
            except Exception as e:
                print(f"Error sending Twilio native template: {e}")
        
        return Response(content=create_twiml_response(WELCOME_MENU), media_type="application/xml")

    # Get current user session
    session = sessions[user_id]
    mode = session.get("mode", "MENU")

    # 3. Handle MENU interactions
    if mode == "MENU":
        if incoming_msg in ["1", "1️⃣"]:
            sessions[user_id]["mode"] = "AI_SERVICES"
            reply = (
                "🤖 *AI Engineering Services by Team Samay*\n\n"
                "We design and build intelligent systems to automate workflows and enhance apps:\n"
                "• *AI Agents & Assistants*: Task planning, tool execution, and automation.\n"
                "• *LLM & RAG Pipelines*: Custom semantic search over your private documentation.\n"
                "• *Vector Databases*: Expertise with Pinecone, pgvector, Qdrant, Chroma.\n"
                "• *Fine-Tuning & Prompting*: Domain-specific optimization.\n\n"
                "Describe the AI application you have in mind! (or reply *menu* to return)"
            )
        elif incoming_msg in ["2", "2️⃣"]:
            sessions[user_id]["mode"] = "FULL_STACK"
            reply = (
                "💻 *Full-Stack Development by Team Samay*\n\n"
                "We craft responsive, scalable, and premium web and mobile applications:\n"
                "• *Frontend*: Next.js, React, TailwindCSS, Outfit/Inter typography.\n"
                "• *Backend*: FastAPI, Node.js/Express, Python, serverless APIs.\n"
                "• *Databases*: High-performance PostgreSQL, MongoDB, Redis.\n"
                "• *DevOps & Cloud*: AWS, GCP, Docker, GitHub Actions CI/CD.\n\n"
                "What platform or system are you planning to build? Tell us about it! (or reply *menu* to return)"
            )
        elif incoming_msg in ["3", "3️⃣"]:
            # Display contact details
            reply = (
                "📞 *Contact Founder (Samay)*\n\n"
                "Get in touch directly with our founder, Samay, for bookings, collaborations, or a direct consultation:\n"
                "• 📱 Phone/WhatsApp: 9764096358\n"
                "• ✉️ Email: samay.founder@example.com\n"
                "• 💼 LinkedIn: linkedin.com/in/samay-founder (placeholder)\n"
                "• 🌐 Website: teamsamay.example.com (placeholder)\n\n"
                "Would you like us to schedule a call? Or type *menu* to go back."
            )
        elif incoming_msg in ["4", "4️⃣"]:
            sessions[user_id]["mode"] = "CHAT"
            reply = (
                "💬 *General Chat Mode Activated*\n\n"
                "You are now chatting with Team Samay's AI Assistant. Ask me anything about how we build software, our tech stack, or describe your project!"
            )
        else:
            # If the user asks a question directly from the menu, switch to chat mode and let Groq answer
            sessions[user_id]["mode"] = "CHAT"
            reply = await get_groq_response(user_id, incoming_msg)

    # 4. Handle other modes (Direct Chat / Service Discussion)
    else:
        # Any subsequent message gets processed by the Groq AI model using session memory
        reply = await get_groq_response(user_id, incoming_msg)

    return Response(content=create_twiml_response(reply), media_type="application/xml")
