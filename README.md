---

## 📄 ATS Resume Analyzer

An **AI-powered ATS (Applicant Tracking System) Resume Analyzer** that allows users to upload resumes and receive detailed scoring, feedback, and match insights based on a selected job description. Built using **Streamlit**, **LangChain**, and **LLM (Google Gemini)**, this app enhances resume quality and increases job-fit precision.

---

### 🚀 Features

* 📄 Upload resume (PDF)
* 💼 Paste or upload job description
* ⚙️ AI-based resume scoring (out of 10)
* ✍️ Detailed section-wise feedback
* 🤖 Gemini/GPT-based resume analysis agent
* 📥 Downloadable feedback PDF report
* 🔒 Local file processing (No cloud upload)
* 🌐 Easy-to-use web UI with Streamlit

---

### 🛠 Tech Stack

| Layer        | Technology                      |
| ------------ | ------------------------------- |
| Frontend     | Streamlit                       |
| Backend      | Python, LangChain               |
| LLM          | Google Gemini (via LangChain)   |
| PDF Handling | PyPDF2, ReportLab               |
| Others       | dotenv, Streamlit Session State |

---

### 🧰 Setup Instructions

#### 1. Clone your GitHub repo

```bash
git clone https://github.com/your-username/ats-resume-analyzer.git
cd ats-resume-analyzer
```

#### 2. Create virtual environment (optional but recommended)

```bash
python -m venv .venv
source .venv/bin/activate       # On Windows: .venv\Scripts\activate
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

#### 4. Create `.env` file

```bash
touch .env
```

Inside `.env` add your API key:

```
GOOGLE_API_KEY=your_google_api_key
```

#### 5. Run the app

```bash
streamlit run main.py
```

---

### 📌 Example Use Case

1. User uploads a PDF resume.
2. User pastes or uploads a job description.
3. AI compares both and generates:

   * Resume match score
   * Suggestions for improvement
   * PDF report to download

---

### 📚 License

MIT License. You are free to use, modify, and distribute this project with proper attribution.

---

### 🤝 Contributions

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.


