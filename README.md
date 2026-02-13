# Oppstarter - מערכת ניתוח הזדמנויות

מערכת ניתוח נתונים לסוכני ביטוח ופנסיה, שמזהה שינויים בתיק הלקוח והופכת אותם למשימות והזדמנויות מכירה, שירות ושימור — בצורה חכמה ומדורגת לפי עדיפות.

## 🚀 התחלה מהירה

### התקנה מקומית

```bash
cd opportunity-engine
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

### הרצה עם Docker

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### הרצה עם Docker (ללא docker-compose)

```bash
docker build -t oppstarter .
docker run -p 8501:8501 oppstarter
```

## 📦 מבנה הפרויקט

```
oppstarter/
├── opportunity-engine/       # אפליקציית מנוע ההזדמנויות
│   ├── app.py                # אפליקציית Streamlit ראשית
│   ├── core/                 # לוגיקת הליבה
│   │   ├── ai_client.py      # אינטגרציה עם Gemini AI
│   │   ├── config.py         # קונפיגורציה
│   │   ├── data_loader.py    # טעינת נתונים מ-Excel
│   │   ├── opportunities.py  # הרכבת הזדמנויות
│   │   ├── quality.py        # בדיקת איכות נתונים
│   │   ├── rules.py          # מנוע חוקים
│   │   ├── scoring.py        # חישוב ציונים
│   │   └── security.py       # הגנה על PII
│   ├── sample_data/          # יצירת נתוני דמו
│   ├── tests/                # בדיקות יחידה
│   ├── requirements.txt      # תלויות Python
│   └── README.md             # תיעוד מפורט
├── .github/workflows/        # CI/CD workflows
├── Dockerfile                # הגדרת Docker
├── docker-compose.yml        # תצורת Docker Compose
└── README.md                 # הקובץ הזה
```

## 🔄 CI/CD

הפרויקט כולל pipeline אוטומטי:

- **Test**: רץ על כל push ו-PR
  - התקנת תלויות
  - הרצת בדיקות (pytest)
  - יצירת נתוני דמו
  - בדיקת syntax

- **PR Checks**: בדיקות אוטומטיות לכל Pull Request
  - אימות מבנה ה-PR
  - בדיקת תיאור ו-commits
  - סימון מוכן לסקירה

- **Deploy**: פריסה אוטומטית ל-Render על main branch
  - בנייה וטסט של Docker image
  - פריסה אוטומטית ל-production
  - Health checks ומעקב

📘 למידע מפורט על תהליך ה-PR והפריסה, ראה [DEPLOYMENT.md](DEPLOYMENT.md)

## 📋 דרישות

- Python 3.11+
- Docker (אופציונלי, להרצה בקונטיינר)

## 🧪 בדיקות

```bash
cd opportunity-engine
pytest -v
```

## 🔐 קונפיגורציה

צור קובץ `.env` בתיקיית `opportunity-engine`:

```env
AI_ENABLED=true
GEMINI_API_KEY=your-api-key-here
```

## 📊 שימוש

1. העלה קובץ Excel עם הטאבים: `Customers`, `Accounts`, `Events`
2. המערכת תנתח את הנתונים ותיצור הזדמנויות
3. סקור את ההזדמנויות הממוינות לפי עדיפות
4. ייצא לקובץ CSV לפי צורך

## 🤝 תרומה

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 רישיון

This project is open source and available under standard terms.

## 📞 תמיכה

לשאלות ובעיות, פתח Issue ב-GitHub.
