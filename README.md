# IELTS Master Hub — AI Powered IELTS Preparation Platform

**IELTS Master Hub** is a production-ready, full-stack web application designed for comprehensive IELTS exam preparation. The platform is localized in **Uzbek (Latin alphabet)** with optional English support and features artificial intelligence integration (via Google Gemini AI) for Writing and Speaking evaluation.

---

## Key Features

- **Authentication System**: User registration, login, logout, remember me, password hashing (Werkzeug), role-based authorization (User vs Admin), and profile customization.
- **Modern Uzbek Dashboard**: Real-time current estimated IELTS Band, target score indicator, interactive Chart.js weekly progress graphs, study streak counter, today's checklist, and recent activity logs.
- **Reading Module**: Reading passages filtered by difficulty (Easy, Medium, Hard), 20-minute countdown timer, interactive text highlighter tool, answer submission auto-grading, and detailed answer explanations.
- **Listening Module**: Interactive audio player, section filter, audio transcript viewer, timed questions, auto-scoring, and review mode.
- **Writing AI Module**: Task 1 (Visual chart description) & Task 2 (Discursive essay) live writing workspace, real-time word counter, timer, draft autosave, and AI examiner scoring returning detailed Uzbek feedback across 4 criteria (TR/TA, CC, LR, GRA), mistake corrections, and improved Band 8.0+ model essays.
- **Speaking AI Module**: Part 1, Part 2 (Cue Card), and Part 3 prompts, browser-based Web Audio MediaRecorder recording/upload, AI analysis for fluency, vocabulary, grammar, pronunciation, band score, and sample responses.
- **Grammar Course**: 8 core IELTS grammar topics (Tenses, Passive, Conditionals, Relative Clauses, Articles, Prepositions, Linking Words, Complex Sentences) with theory, IELTS examples, and interactive AJAX exercise checking.
- **Vocabulary Module**: Academic Word List (AWL) cards, flip flashcards interface, spaced repetition status tracking, quiz mode, and personal student vocabulary notebook.
- **Full Mock Exam Simulation**: 4-skill timed IELTS simulation, automated band score calculation, detailed result breakdown, and downloadable ReportLab PDF score certificates.
- **AI Mentor Chat**: Interactive AI study assistant answering IELTS queries in Uzbek.
- **Personalized Study Planner**: Target exam date and target band score setup, daily hours configuration, and automated task checklist.
- **Analytics & Leaderboard**: Skills radar charts, weak/strong area breakdown, weekly/monthly student rankings, and streak leaderboards.
- **Subscription Management**: Free vs. Premium plan comparison and Click/Payme checkout simulation.
- **Admin Control Panel**: System dashboard, user management (role/subscription toggle), content management for test passages and prompts.

---

## Technology Stack

- **Backend**: Python 3.10+, Flask 3.0, PyMongo, Flask-Login, Werkzeug, python-dotenv
- **Database**: MongoDB (Local instance or MongoDB Atlas)
- **Frontend**: HTML5, Vanilla CSS3 (Custom Design System with Dark/Light mode), JavaScript (ES6+), Bootstrap 5.3, Chart.js 4, FontAwesome / Bootstrap Icons
- **PDF Generation**: ReportLab
- **AI Integration**: Google Gemini API (`google-generativeai`) with realistic offline Uzbek AI evaluator fallback

---

## Project Folder Structure

```
ielts_master_hub/
│
├── app.py                  # Main Flask application entrypoint & blueprint registration
├── config.py               # Application configuration and environment loader
├── seed_db.py              # Automated database seeder with sample IELTS practice data
├── requirements.txt        # Python package dependencies
├── .env                    # Environment variables configuration
├── README.md               # Documentation and execution instructions
│
├── utils/
│   ├── db.py               # PyMongo connection wrapper and Flask-Login User model
│   ├── ai_helper.py        # Gemini AI evaluator for Writing, Speaking, and AI Mentor
│   ├── pdf_generator.py    # ReportLab PDF certificate & score report generator
│   └── helpers.py          # Band score converters and Uzbek date formatting
│
├── routes/
│   ├── auth.py             # Login, register, logout handlers
│   ├── dashboard.py        # Overview dashboard and progress chart API
│   ├── reading.py          # Reading passages and auto-grading
│   ├── listening.py        # Listening audio exercises
│   ├── writing.py          # Writing Task 1 & Task 2 AI evaluation
│   ├── speaking.py         # Audio recording and Speaking AI scoring
│   ├── grammar.py          # 8 Grammar lessons and interactive exercises
│   ├── vocabulary.py       # Academic Word List, flashcards, and notebook
│   ├── mock_exam.py        # Full IELTS simulation test and PDF export
│   ├── ai.py               # AI Mentor interactive chat
│   ├── planner.py          # Study planner generator
│   ├── analytics.py        # Performance statistics and radar charts
│   ├── leaderboard.py      # Student rankings and streak leaders
│   ├── subscription.py     # Free vs Premium plans and checkout
│   ├── profile.py          # User profile and achievement badges
│   └── admin.py            # Admin management control panel
│
├── static/
│   ├── css/
│   │   └── style.css       # Custom design system CSS with dark mode variables
│   ├── js/
│   │   ├── main.js         # Dark mode toggle, drawer menu, alert timers
│   │   ├── recorder.js     # Web Audio API MediaRecorder script
│   │   └── charts.js       # Chart.js weekly progress graph
│   └── uploads/            # Secure upload folder for audio files and reports
│
└── templates/              # Jinja2 HTML templates organized by blueprint module
```

---

## Quick Start Guide

### 1. Prerequisites
Ensure you have the following installed on your machine:
- **Python 3.10+**
- **MongoDB Server** (Running locally on `mongodb://localhost:27017` or a MongoDB Atlas URI)

### 2. Installation
Navigate to the project root directory and install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Environment Setup
Check the `.env` file in the root directory:
```env
SECRET_KEY=ielts_master_hub_super_secret_key_2026_uzbekistan
MONGO_URI=mongodb://localhost:27017/ielts_master_hub
GEMINI_API_KEY=your_gemini_api_key_here
```
*(Note: If `GEMINI_API_KEY` is left blank, the app automatically runs in realistic offline AI evaluator mode so all features work seamlessly during development).*

### 4. Seed Database
Run the seed script to populate sample Reading passages, Listening scripts, Writing prompts, Grammar lessons, and Academic Vocabulary words into MongoDB:
```bash
python seed_db.py
```

Default Accounts created:
- **Admin Account**: Email: `admin@ielts.uz` | Password: `admin123`
- **Demo User Account**: Email: `user@ielts.uz` | Password: `user123`

### 5. Run Application
Start the Flask development server:
```bash
python app.py
```
Open your browser and navigate to: **`http://127.0.0.1:5000`**
