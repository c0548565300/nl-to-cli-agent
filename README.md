NL-to-CLI Agent
An AI-driven bridge between Natural Language and Windows Command Line.

ממשק אינטליגנטי הממיר הוראות בשפה חופשית לפקודות CMD מדויקות, תוך שימוש במודלי שפה מתקדמים ושמירה על סטנדרטים גבוהים של אבטחת מידע.

🌟 Key Features
Zero-Shot Translation: המרה מיידית משפה טבעית לסינטקס CLI תקין.

Security Guardrails: מנגנון מובנה למניעת הרצת פקודות הרסניות (Destructive Commands).

Robust Architecture: טיפול בשגיאות API וניהול משתני סביבה מאובטח.

Modern UX: ממשק Gradio מעוצב הכולל תמיכה ב-RTL וכפתור העתקה מהיר.

🛠 Tech Stack
Engine: OpenAI GPT-4o-mini

UI Framework: Gradio

Backend: Python 3.10+

Security: Dotenv (Environment Isolation)

⚙️ Quick Start
Clone & Install:

Bash

git clone https://github.com/your-username/nl-to-cli-agent.git
pip install -r requirements.txt
Config:
צור קובץ .env והזן את ה-OPENAI_API_KEY שלך.

Launch:

Bash

python app.py
🔒 Security Note
הפרויקט כולל שכבת Safety Prompting קשיחה המסננת פקודות כגון format, del ו-shutdown כדי להבטיח סביבת עבודה בטוחה.