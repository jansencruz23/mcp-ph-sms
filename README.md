# MCP SMS Server (Philippines)

A Model Context Protocol (MCP) server that provides SMS capabilities (via a free API) and a local contacts management system.

## Setup

1.  **Prerequisites**: Python 3.10+
2.  **Install Dependencies**:
    ```bash
    pip install mcp[cli] httpx pydantic pydantic-settings python-dotenv sqlmodel
    ```
3.  **Configure Environment**:
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
python test_manual.py
```
This will create a test contact and attempt a dry-run SMS send.

### 2. Run via CLI (MCP)
To start the standard IO server (mainly for debugging or piping):
```bash
python main.py
```
*Note: This will appear to hang as it waits for JSON-RPC input.*

### 3. Run with MCP Inspector (Web UI)
If you have `npx` installed:
```bash
npx @modelcontextprotocol/inspector python main.py
```

## Integration with Claude Desktop

To use this server with Claude Desktop, add the following to your config file:

**Windows Config Path**: `%APPDATA%\Claude\claude_desktop_config.json`  
(Usually `C:\Users\YOUR_USER\AppData\Roaming\Claude\claude_desktop_config.json`)

```json
{
  "mcpServers": {
    "sms-ph": {
      "command": "python",
      "args": ["d:/User/Jansen/Self Study/2026 - 02 - FEBRUARY/mcp-ph-sms/main.py"],
      "env": {
        "SMS_API_KEY": "your_key_here"
      }
    }
  }
}
```

**Important**: 
- Use the **absolute path** to your `python` executable if you are using a virtual environment (e.g., `d:/.../.venv/Scripts/python.exe`).
- Use the **absolute path** to the `main.py` script.
- You can omit `env` in the JSON if you have the `.env` file correctly set up and being read, but passing the API key explicitly is safer.

## Features

- **Contacts**: Create, List, Update, Delete contacts with tags and notes.
- **SMS**: Send messages (throttled to 1 per 10s), view history.
- **Tools**: `contacts.list`, `contacts.create`, `sms.send`, etc.
