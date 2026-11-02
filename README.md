## Demo

Watch the form score a lead and send it to Telegram:
[https://drive.google.com/file/d/FILE_ID/view?usp=sharing](https://drive.google.com/file/d/1ea6ogVciv0fULwUbOiVHov5thTShh2OG/view?usp=drive_link)

# AI Lead Qualification Workflow

A free, production-ready AI workflow automation project.

## What it does

1. Receives a new lead from a webhook (website form, Telegram, etc.)
2. AI scores the lead (Hot / Warm / Cold)
3. Saves the lead into a local SQLite database
4. Sends a notification to your Telegram
5. Sends an automatic reply to the lead

## Tech Stack (100% Free)

- **n8n** → Workflow engine (self-hosted, free)
- **Python** → Lead qualification logic
- **OpenRouter / Groq** → Free LLM models
- **SQLite** → Database
- **Telegram Bot** → Notifications

## Project Structure

```
ai-workflow-automation/
├── n8n/
│   └── lead-pipeline.json      # n8n workflow export
├── python/
│   ├── qualify_lead.py         # AI scoring script
│   └── crm_writer.py           # Save to SQLite
├── data/
│   └── leads.db                # SQLite database (created automatically)
├── .env.example
├── docker-compose.yml
└── README.md
```

## Quick Start

### 1. Clone & Setup

```bash
cd ai-workflow-automation
cp .env.example .env
# Edit .env and add your free API keys
```

### 2. Install Python dependencies

```bash
pip install -r python/requirements.txt
```

### 3. Run n8n with Docker

```bash
docker compose up -d
```

Open http://localhost:5678

### 4. Import the workflow

- Go to n8n → Workflows → Import from File
- Select `n8n/lead-pipeline.json`

### 5. Test

Send a POST request to the webhook URL that n8n gives you.

---

## Free API Keys you need

| Service     | Free Tier                  | Get it from                  |
|-------------|----------------------------|------------------------------|
| OpenRouter  | Free models available      | https://openrouter.ai        |
| Groq        | Very fast free models      | https://console.groq.com     |
| Telegram    | Completely free            | @BotFather                   |

