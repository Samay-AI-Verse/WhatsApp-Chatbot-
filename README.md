# 💬 WhatsApp AI Chatbot with FastAPI, Groq & Twilio 

A premium, conversational WhatsApp AI chatbot representing **Team Samay**, built using **FastAPI**, **Groq LLM** (Llama 3.1), and **Twilio API**. It supports structural menus, dynamic interactive sessions, AI general chat, and is fully containerized using **Docker** for seamless local testing and deployment on **Render**.

---

## 🚀 Features
* **Interactive Menu System:** Direct options to navigate AI services, full-stack services, contact details, and general chat.
* **Smart AI Chat:** Integrated with Groq's high-speed Llama-3.1 model.
* **Session Persistence:** Remembers user conversation history across messages.
* **Fully Dockerized:** Consistent environments locally and in production (e.g. Render).
* **Auto-Port Mapping:** Adaptable command layer mapping automatically to Render's custom port allocation.

---

## 🛠️ Step 1: Fork and Clone the Repository

To get this codebase onto your machine:

### 1. Fork the Repository
Click the **Fork** button at the top-right of the GitHub repository page to create a copy of the repository under your own GitHub account.

### 2. Clone the Forked Repository
Open your terminal (PowerShell, Command Prompt, or bash) and run:
```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/whatsapp_chatbot.git
cd whatsapp_chatbot
```
*(Replace `YOUR_GITHUB_USERNAME` with your actual GitHub username).*

---

## 🔑 Step 2: Environment Configuration

The chatbot requires a few API keys to function. 

1. Create a file named `.env` in the root of the project:
   ```powershell
   # On Windows (PowerShell):
   New-Item .env
   ```
2. Copy the following variables into your `.env` file and replace the placeholder values with your credentials:
   ```env
   # Groq LLM API Key (Get one for free at console.groq.com)
   GROQ_API_KEY=your_groq_api_key_here
   GROQ_MODEL=llama-3.1-8b-instant

   # Twilio Configuration (Get these from your Twilio Console)
   TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
   TWILIO_AUTH_TOKEN=your_twilio_auth_token_here
   TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
   TWILIO_MENU_TEMPLATE_SID=
   ```

*Note: The `.env` file is ignored by git (configured in `.dockerignore` and `.gitignore`) to protect your private keys from being exposed.*

---

## 🐳 Step 3: Run Locally Using Docker (Step-by-Step Lesson)
 
Using Docker ensures the project runs identically on your machine and on Render.
 
### Prerequisites:
* Install and open **Docker Desktop** on your machine. Ensure the whale icon in the bottom-left corner is **Green** (indicating the engine is running).
 
---
 
### 📦 Phase 1: Build the Docker Image
Tell your students: *"First, we will package our code and dependencies into a reusable image."*
 
**Run this command:**
```powershell
docker build -t whatsapp-chatbot .
```
**What to tell students:**
* `-t whatsapp-chatbot` assigns a name (tag) to our image.
* The `.` at the end tells Docker to look for the `Dockerfile` in the current folder.
 
---
 
### 🚀 Phase 2: Run the Container
Tell your students: *"Now, we will launch our container (an active instance of the image) and pass our API keys."*
 
**Run this command:**
```powershell
docker run -d -p 8000:8000 --env-file .env --name chatbot-container whatsapp-chatbot
```
**What to tell students:**
* `-d` (Detached mode) runs the container in the background so it doesn't block the terminal.
* `-p 8000:8000` maps port `8000` of your computer to port `8000` inside the container.
* `--env-file .env` automatically imports your Groq and Twilio API keys.
* `--name chatbot-container` gives it an easy name so we can stop it later.
 
---
 
### 🔍 Phase 3: Verify & Test Locally
Tell your students: *"Let's check if our container is running and test it by sending a fake message."*
 
**1. Check if the container is active:**
```powershell
docker ps
```
 
**2. Check the container logs (important for debugging crashes):**
```powershell
docker logs chatbot-container
```
 
**3. Test the chatbot API (send a request to `/whatsapp`):**
```powershell
(Invoke-WebRequest -Uri "http://localhost:8000/whatsapp" -Method Post -Body @{Body="hi"}).Content
```
*(This will print the exact XML response from Twilio, showing the welcome menu!)*
 
---
 
### 🧹 Phase 4: Stop and Clean Up
Tell your students: *"Always clean up your local space after testing so it doesn't block ports."*
 
**1. Stop the running container:**
```powershell
docker stop chatbot-container
```
 
**2. Remove the container:**
```powershell
docker rm chatbot-container
```
 
---
 
## ☁️ Step 4: Deploy to Render (Phase 5)
 
Once students see this works perfectly locally, they are 100% ready to deploy to Render:
 
1. **Commit and Push your changes** to your GitHub fork (excluding `.env`):
   ```powershell
   git add .
   git commit -m "Configure Docker for Render"
   git push origin main
   ```
2. **Create Web Service on Render:**
   * Go to [dashboard.render.com](https://dashboard.render.com) and sign in.
   * Click **New > Web Service**.
   * Connect your GitHub repository.
3. **Configure Service Details:**
   * **Name:** `whatsapp-chatbot` (or any name you prefer)
   * **Runtime:** Select **Docker** (Render will automatically look for the `Dockerfile`).
   * **Instance Type:** Select **Free**.
4. **Add Environment Variables:**
   * Click the **Advanced** or **Environment** tab.
   * Add the following environment variables (matching your local `.env` values):
     * `GROQ_API_KEY`
     * `TWILIO_ACCOUNT_SID`
     * `TWILIO_AUTH_TOKEN`
     * `TWILIO_WHATSAPP_NUMBER`
     * `TWILIO_MENU_TEMPLATE_SID`
5. **Deploy:**
   * Click **Deploy Web Service**.
   * Once the deployment is complete, Render will provide a public URL (e.g. `https://whatsapp-chatbot-xyz.onrender.com`).
 
---
 
## 📲 Step 5: Connect Twilio Sandbox Webhook
 
To route WhatsApp messages to your deployed chatbot:
 
1. Go to your **Twilio Console > Messaging > Try it out > Send a WhatsApp Message**.
2. Under **Sandbox Settings**, find the field **"When a message comes in"**.
3. Enter your Render service URL + `/whatsapp` (e.g. `https://whatsapp-chatbot-xyz.onrender.com/whatsapp`).
4. Set the HTTP method to **POST**.
5. Save the settings.
6. Send a message like `hi` or `menu` to your Twilio Sandbox number to test!
