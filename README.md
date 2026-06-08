# AURON 2.0

AI Powered Desktop Productivity Assistant built using Python and Ollama.

---

## Overview

AURON 2.0 is a locally running AI-powered desktop assistant designed to enhance productivity, automate routine tasks, and provide intelligent assistance directly on Windows systems.

Unlike browser-based AI assistants, AURON integrates deeply with the operating system, allowing voice interaction, task management, productivity tracking, system control, and personalized long-term memory.

---

## Features

### AI Assistant
- AI Chat using Ollama
- Multiple AI Modes
  - General Mode
  - Coding Mode
  - Study Mode
  - System Mode
- Long-Term Conversation Memory
- Vector Memory Retrieval
- Agent Mode
- AI Planning Engine
- AI Code Generation

### Voice Features
- Speech-to-Text
- Text-to-Speech Responses
- Global Hotkey Activation
- Voice Authentication

### Productivity Suite
- Task Manager
- Task Prioritization Engine
- Smart Day Planner
- Daily Summary Generator
- Daily Standup Generator
- Focus Mode
- Pomodoro Mode

### Notes & Reminders
- Notes System
- Reminders System
- Desktop Sticky Notes
- Persistent Sticky Note Storage

### Meeting Assistant
- Meeting Mode
- Automatic Meeting Notes
- Meeting Analysis
- Follow-Up Email Generation

### Email Assistant
- Email Draft Generation
- Leave Email Generator
- Progress Email Generator
- Meeting Follow-Up Email Generator
- Email Reading Support
- Email Sending Support

### Calendar Integration
- Calendar Event Creation
- Calendar Event Management
- Calendar Commands

### Security
- PIN Authentication
- Voice Authentication

### System Utilities
- Application Launcher
- File Search
- System Monitoring
- Battery Monitoring
- Terminal Access
- System Controls
- System Tray Integration

### User Interface
- Modern CustomTkinter Interface
- Overlay Window
- Multiple Themes
- Sticky Note Windows
- Responsive Layout

---

## Technologies Used

- Python
- Ollama
- ChromaDB
- CustomTkinter
- PyInstaller
- SpeechRecognition
- pyttsx3
- PyAudio
- Google Calendar API
- Gmail API

---

## Installation

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/AURON-2.0.git
cd AURON-2.0
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install customtkinter pyttsx3 SpeechRecognition pyaudio chromadb ollama keyboard pystray pillow psutil schedule google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2 beautifulsoup4 requests
```

### Run AURON

```bash
python main.py
```

---

## Build Executable

```bash
pyinstaller --onefile --windowed --icon=assets/auron.ico main.py
```

---

## Project Structure

```text
AURON 2.0
│
├── ai/
├── assets/
├── core/
├── gui/
├── productivity/
├── security/
├── system/
├── voice/
│
├── main.py
├── settings.json
├── README.md
└── requirements.txt
```

---

## Future Enhancements

- Advanced Agent Automation
- Cloud Synchronization
- Mobile Companion App
- Multi-Device Support
- Enhanced Memory System
- Plugin Ecosystem

---

## Author

Krish Desai

Computer Engineering Student  
St. Francis Institute of Technology

---

## License

This project is intended for educational, research, and personal productivity purposes.
