Agent Router
============

Quickly set up litellm proxy and langfuse locally for use with Cline/OpenHands/BrowserUse etc.

## Get Started

1. Copy .env.example to .env:

```shell
cp .env.example .env
```

2. Add your LLM provider API keys in .env

3. Install dependencies:

```shell
poetry install
```  
  
4. Start Agent Router:

```shell
poetry run poe start
```

5. Configure Cline/OpenHands/BrowserUse to use the router:

For Anthropic models:
* API Provider: Anthropic
* Custom Base URL: http://localhost:54000/anthropic
* API Key: any non-empty string
* Model ID: agentrouter.dev

For other models:
* API Provider: OpenAI Compatible
* Custom Base URL: http://localhost:54000
* API Key: any non-empty string
* Model ID: agentrouter.dev

## Using Langfuse for observability

1. Start Langfuse using the provided docker-compose file:

```shell
docker compose -f compose.langfuse.yml -p agentrouter up -d
```

2. Access the Langfuse dashboard at http://localhost:53000

Use the following credentials:
* Email: agentrouter-local@agentrouter.local
* Password: agentrouter-local
