# MCP SMS Server (Philippines)

A Model Context Protocol (MCP) server that provides SMS capabilities (via a free API) and a local contacts management system.

## Setup

1.  **Prerequisites**: Python 3.10+, [uv](https://docs.astral.sh/uv/)
2.  **Install Dependencies**:
    ```bash
    uv sync
    # OR if managing manually:
    uv pip install mcp[cli] httpx pydantic pydantic-settings python-dotenv sqlmodel
    ```
3.  **Configure Environment**:
    
    Obtain your API key from [https://sms-api-ph.netlify.app](https://sms-api-ph.netlify.app).
    
    Create a `.env` file in the root directory:
    ```env
    SMS_API_KEY=your_actual_api_key_here
    SMS_API_BASE_URL=https://sms-api-ph-gceo.onrender.com
    DB_PATH=sqlite:///data/app.db
    LOG_LEVEL=INFO
    ```

## Running the Server

### 1. Manual Testing (Script)
To verify the database and API logic without the full MCP server:
```bash
uv run test_manual.py
```
This will create a test contact and attempt a dry-run SMS send.

### 2. Run via CLI (MCP)
To start the standard IO server (mainly for debugging or piping):
```bash
uv run main.py
```
*Note: This will appear to hang as it waits for JSON-RPC input.*

### 3. Run with MCP Inspector (Web UI)
If you have `npx` installed:
```bash
npx @modelcontextprotocol/inspector uv run main.py
```

## Integration with Claude Desktop

To use this server with Claude Desktop, add the following to your config file:

**Windows Config Path**: `%APPDATA%\Claude\claude_desktop_config.json`  
(Usually `C:\Users\YOUR_USER\AppData\Roaming\Claude\claude_desktop_config.json`)

```json
{
  "mcpServers": {
    "sms-ph": {
      "command": "uv",
      "args": [
        "run",
        "--with", "mcp[cli]",
        "--with", "httpx",
        "--with", "pydantic",
        "--with", "pydantic-settings",
        "--with", "python-dotenv",
        "--with", "sqlmodel",
        "d:/User/path-to-your-mcp/mcp-ph-sms/main.py"
      ],
      "cwd": "d:/User/path-to-your-mcp/mcp-ph-sms",
      "env": {
        "SMS_API_KEY": "your_key_here"
      }
    }
  }
}
```

**Alternative (if project is already synced via `uv sync`)**:
```json
{
  "mcpServers": {
    "sms-ph": {
      "command": "d:/User/path-to-your-mcp/mcp-ph-sms/.venv/Scripts/python.exe",
      "args": [
        "run",
        "d:/User/path-to-your-mcp/mcp-ph-sms/main.py"
      ],
      "cwd": "d:/User/path-to-your-mcp/mcp-ph-sms",
      "env": {
        "SMS_API_KEY": "your_key_here"
      }
    }
  }
}
```

**Important**:
- Ensure `uv` is in your system PATH.
- `cwd` ensures `uv` picks up the `.env` and `pyproject.toml` from the correct directory.
- You can omit `env` in the JSON if you have the `.env` file correctly set up.

## Available Tools

### Contacts
- **`contacts_list`**: List contacts with filtering options.
  - Arguments: `limit` (default: 50), `tag` (optional), `q` (search query).
- **`contacts_get`**: Get a specific contact by ID.
  - Arguments: `contact_id`.
- **`contacts_create`**: Create a new contact.
  - Arguments: `name`, `phone`, `tags` (optional list), `notes` (optional).
- **`contacts_update`**: Update an existing contact.
  - Arguments: `contact_id`, and any of `name`, `phone`, `tags`, `notes`.
- **`contacts_delete`**: Delete a contact by ID.
  - Arguments: `contact_id`.

### SMS
- **`sms_send`**: Send an SMS message.
  - Arguments: `recipient` (phone number or name), `message`, `dry_run` (boolean, default: False).
  - *Note: Throttled to 1 message per 10 seconds.*
- **`sms_history`**: View SMS sending history.
  - Arguments: `limit` (default: 20), `contact_id` (optional filter).

### Prompts
- **`compose_sms`**: Helper prompt to draft an SMS based on a topic.

