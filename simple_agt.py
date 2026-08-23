import os
import subprocess
from pathlib import Path

from google import genai
from google.genai import types
from playwright.sync_api import sync_playwright


# ============================================================
# CONFIGURATION
# ============================================================

MODEL = "gemini-3.6-flash"

WORKSPACE = Path.cwd().resolve()


# ============================================================
# TOOL 1: LIST DIRECTORY
# ============================================================

def list_directory(directory_path: str = ".") -> str:
    """List files and folders inside the workspace."""

    try:
        path = (WORKSPACE / directory_path).resolve()

        if not str(path).startswith(str(WORKSPACE)):
            return "Error: Access outside workspace is not allowed."

        items = []

        for item in path.iterdir():
            if item.is_dir():
                items.append(f"[DIR]  {item.name}")
            else:
                items.append(f"[FILE] {item.name}")

        return "\n".join(items) if items else "Directory is empty."

    except Exception as e:
        return f"Error: {e}"


# ============================================================
# TOOL 2: READ FILE
# ============================================================

def read_file(filepath: str) -> str:
    """Read a text file inside the workspace."""

    try:
        path = (WORKSPACE / filepath).resolve()

        if not str(path).startswith(str(WORKSPACE)):
            return "Error: Cannot access outside workspace."

        if not path.exists():
            return f"File not found: {filepath}"

        return path.read_text(encoding="utf-8")[:12000]

    except Exception as e:
        return f"Error reading file: {e}"


# ============================================================
# TOOL 3: WRITE FILE
# ============================================================

def write_to_file(filepath: str, content: str) -> str:
    """Create or overwrite a file inside the workspace."""

    try:
        path = (WORKSPACE / filepath).resolve()

        if not str(path).startswith(str(WORKSPACE)):
            return "Error: Cannot write outside workspace."

        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

        return f"Successfully wrote {filepath}"

    except Exception as e:
        return f"Error writing file: {e}"


# ============================================================
# TOOL 4: TERMINAL
# ============================================================

def run_terminal_command(command: str) -> str:
    """Run a terminal command inside the workspace."""

    print(f"\n[Tool] Running: {command}")

    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=WORKSPACE,
            capture_output=True,
            text=True,
            timeout=15
        )

        output = result.stdout

        if result.stderr:
            output += "\n" + result.stderr

        return output[:8000]

    except subprocess.TimeoutExpired:
        return "Error: Command timed out."

    except Exception as e:
        return f"Command failed: {e}"


# ============================================================
# TOOL 5: WEB BROWSER
# ============================================================

def browse_webpage(url: str) -> str:
    """Open a webpage and return visible text."""

    print(f"\n[Tool] Browsing: {url}")

    try:
        with sync_playwright() as p:

            browser = p.chromium.launch(headless=True)

            page = browser.new_page()

            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=15000
            )

            content = page.inner_text("body")

            browser.close()

            return content[:8000]

    except Exception as e:
        return f"Browser error: {e}"


# ============================================================
# MAIN AGENT
# ============================================================

def main():

    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        print("ERROR: GEMINI_API_KEY is not set.")
        return

    client = genai.Client(api_key=api_key)

    chat = client.chats.create(
        model=MODEL,

        config=types.GenerateContentConfig(

            tools=[
                list_directory,
                read_file,
                write_to_file,
                run_terminal_command,
                browse_webpage
            ],

            system_instruction="""
You are an autonomous coding agent.

You work inside the current project workspace.

You can:

1. List files
2. Read files
3. Create or modify files
4. Run terminal commands
5. Browse webpages

Before modifying an existing file:
- Inspect it first.
- Understand the existing code.
- Make the required change.
- Run a test when possible.

For Python:
- Run the program after creating it.

For Verilog/SystemVerilog:
- Create synthesizable RTL.
- Create a testbench when requested.
- Run a simulator if available.

Complete the user's task using the available tools.
Explain what you changed after completing the task.
""",

            temperature=0.1
        )
    )

    print("=" * 55)
    print("              SIMPLE CODING AGENT")
    print("=" * 55)
    print(f"Workspace : {WORKSPACE}")
    print(f"Model     : {MODEL}")
    print("=" * 55)

    while True:

        task = input("\nAsk Agent : ")

        if task.strip().lower() in ["exit", "quit"]:
            print("Agent stopped.")
            break

        if not task.strip():
            continue

        print("\nAgent is thinking and acting...\n")

        try:

            response = chat.send_message(task)

            print("\nFinal Answer:")
            print(response.text)

        except Exception as e:

            print("\n[!] Agent Error:")
            print(e)


# ============================================================
# START AGENT
# ============================================================

if __name__ == "__main__":
    main()
