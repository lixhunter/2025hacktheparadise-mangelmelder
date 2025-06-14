# Setup LLM Host

This document outlines the steps to set up the LLM Host environment.

## Prerequisites

- Ensure Docker is installed on your system.

## Setup Steps

1. **Clone the Repository**:
   ```bash
   git clone git@github.com:lixhunter/2025hacktheparadise-mangelmelder.git
   ```
2. **Navigate to the Directory**:
   ```bash
   cd 2025hacktheparadise-mangelmelder/llm-host
   ```
3. **Start the Docker Container**:
   ```bash
   docker compose up -d
   ```
4. **Check the Status**:
   - Open your web browser and go to `http://localhost:11434` to verify that the LLM Host is running.
5. **Install Llama3**:
   ```bash
   curl -X POST http://localhost:11434/api/pull -d '{"name": "llama3"}'
   ```

## Run a prompt

To run a prompt, you can use the following command:

```bash
curl -s http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Hello, world!"
}' | jq -r '.response' | tr -d '\n'; echo
```
