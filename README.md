Agent Router
============

## Get Started

1. Copy .env.example to .env:

```shell
cp .env.example .env
```

2. Add your LLM provider API keys in .env

3. Start Agent Router:

```shell
litellm --config config.yaml
```

4. Configure Cline/OpenHands to use the Agent Router:

* Base URL: http://localhost:4000
* API Key: foo
* Model ID: default

## Observability (Optional)

1. Start Langfuse using the provided docker-compose file:

```shell
docker compose -f compose.langfuse.yml -p agentrouter up -d
```

2. Access the Langfuse dashboard at http://localhost:43000

Use the following credentials:
* Email: agentrouter-local@agentrouter.local
* Password: agentrouter-local
