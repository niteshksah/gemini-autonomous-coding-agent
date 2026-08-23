# 🤖 Gemini Autonomous Coding Agent

> An AI-powered coding agent that can inspect files, write code,
> execute terminal commands, browse the web, and debug projects.

[Python] [Gemini] [Playwright] [GitHub] [AI Agent]

## 🚀 Features

✅ Autonomous tool selection
✅ File & directory management
✅ Terminal command execution
✅ Code generation
✅ Automatic debugging
✅ Web browsing
✅ Python development
✅ Verilog / RTL development

## 🏗️ Architecture

User
 ↓
Gemini LLM
 ↓
Agent Decision
 ↓
┌───────────────┬──────────────┬──────────────┐
│ File Tools    │ Terminal     │ Web Browser  │
└───────────────┴──────────────┴──────────────┘
 ↓
Project Workspace

## 💻 Example

Ask:

"Create a 4-bit ALU in Verilog and generate a testbench."

Agent:

1. Creates alu.v
2. Creates alu_tb.v
3. Runs simulation
4. Detects errors
5. Fixes RTL
6. Reports result

## 🛠️ Tech Stack

Python
Google Gemini API
Google GenAI SDK
Playwright
Git
GitHub
Verilog

## 📂 Project Structure

...
