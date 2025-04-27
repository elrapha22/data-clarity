# 🧹 Data Clarity

**Built Data Clarity to help HR teams clean messy datasets using plain English — no coding required.**

---

## 🚀 Project Goal

Enable users to upload messy HR datasets and use **plain English** to:
- Merge data
- Remove duplicates
- Drop null-heavy columns
- Standardize formats  
All **without writing code**—and with step-by-step logs they can trust.

---

## 🧠 Key Innovation

Natural Language = SQL + Python replacement.  
Type:  
> “Merge these files by employee_id and drop columns with more than 40% missing.”

And receive:
- Cleaned data
- Transparent log of everything that happened
- Visual insights (coming soon)

---

## 🛠️ Tech Stack

| Component   | Tool        |
|-------------|-------------|
| Frontend    | Streamlit   |
| Backend     | Python, Pandas |
| LLM Assist  | OpenAI API  |
| Hosting     | Streamlit Cloud or Fly.io |
| Storage     | Local CSV (no login needed for MVP) |

---

## 📅 Build Roadmap

| Week | Focus                              |
|------|------------------------------------|
| 1    | UI + File Upload + Prompt Input    |
| 2    | Backend Logic + Domain Cleaning    |
| 3    | Smart Suggestions + Visual QA      |
| 4    | Final Polish + Demo + Launch       |

---

## 👤 Who It's For
- HR Analysts
- People Ops teams
- Bootcamp students
- Junior data folks  
…who want results without the technical overwhelm.

---

## 📈 Current Status

✅ Project initialized  
✅ Folder structure created  
🔜 Next: Build UI + file upload interface

---

## 🧪 Sample Use Case (Coming Soon)

| Dataset | Prompt | Result |
|--------|--------|--------|
| `hr_raw.csv` | “Drop rows with null job title and merge with bonus data by employee_id” | Cleaned HR dataset in seconds |

---

### ⚙️ Setup Instructions

```bash
git clone https://github.com/elrapha22/data-clarity.git
cd data-clarity
pip install -r requirements.txt
streamlit run app/app.py
