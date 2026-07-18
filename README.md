# LinkedIn Auto Job Applier 🤖

An automation bot that streamlines job hunting on LinkedIn. It searches for jobs matching your preferences, filters out bad fits, answers Easy Apply application questions, tailors your resume's keywords to each job description using AI, and submits applications — while logging everything it does.

Built on top of the open-source [Auto_job_applier_linkedIn](https://github.com/GodsScion/Auto_job_applier_linkedIn) project, with an added **AI resume keyword tailoring** pipeline (LaTeX + Tectonic) for better ATS matching.

## ✨ Features

- **Automated job search** — runs your configured search terms, locations, and filters (Easy Apply only, experience level, remote/hybrid/on-site, date posted, and more)
- **Smart filtering** — skips jobs by bad words in the description, blacklisted companies, or required experience above your level
- **Easy Apply automation** — fills out multi-step application forms, answering questions from your configured answers
- **AI question answering** — unknown form questions are answered by an LLM using your profile information (OpenAI-compatible APIs, Gemini, DeepSeek, or local models via Ollama/LM Studio; Groq works through the OpenAI-compatible endpoint)
- **AI resume keyword tailoring** *(new)* — rewords your existing resume bullets and skill lines to naturally surface keywords from each job description, then compiles a fresh PDF per job:
  - Facts are locked: names, dates, companies, numbers, and achievements are never changed or invented
  - Template is locked: layout comes from a LaTeX template compiled with [Tectonic](https://tectonic-typesetting.github.io/)
  - Falls back to your default resume if the AI output fails validation
- **External job board support** — collects application links for jobs that redirect off LinkedIn
- **Application history UI** — a local Flask web app to browse everything you've applied to
- **Human-like behavior** — randomized click intervals, optional smooth scrolling, optional undetected-chromedriver stealth mode

## ⚙️ Installation

1. **Python 3.10+** — [python.org/downloads](https://www.python.org/downloads/) (make sure Python is added to PATH)
2. **Google Chrome** — installed in its default location
3. **Python packages**:
   ```
   pip install undetected-chromedriver pyautogui setuptools openai flask flask-cors
   ```
4. **ChromeDriver** — on Windows, run `setup/windows-setup.bat` to install it automatically. (Not needed if you enable `stealth_mode` in `config/settings.py`.)
5. **Tectonic** *(optional, only for resume tailoring)* — install from [tectonic-typesetting.github.io](https://tectonic-typesetting.github.io/) so tailored resume PDFs can be compiled
6. Clone this repo:
   ```
   git clone https://github.com/Ankit-iiitkota/linkedin_auto_bot.git
   ```

## 🔧 Configuration

All configuration lives in the `config/` folder. **These files hold your personal data — fill them in locally and never commit them.**

| File | What goes in it |
|------|-----------------|
| `personals.py` | Name, phone, address, and other application form details |
| `questions.py` | Answers to common application questions, resume path, LinkedIn summary, cover letter, and the profile text the AI uses to answer unknown questions |
| `search.py` | Search terms, location, job filters, blacklists, experience thresholds |
| `secrets.py` | LinkedIn login (optional — can use your browser profile instead) and AI provider URL, API key, and model |
| `settings.py` | Bot behavior: click speed, stealth mode, pause before submit, `tailor_resume_keywords` toggle, etc. |

For resume tailoring, place your files under `all resumes/default/` (this folder is gitignored):

- `resume.pdf` — your default resume, uploaded when tailoring is off or fails
- `resume_template.tex` — LaTeX template with `%%PLACEHOLDER%%` markers
- `resume_data.json` — your structured resume content that fills the template

## 🚀 Usage

Run the bot:

```
python runAiBot.py
```

Browse your application history:

```
python app.py
```

then open `http://localhost:5000`.

## ⚠️ Disclaimer

This tool is for **educational purposes only**. Automating interactions with LinkedIn may violate the [LinkedIn User Agreement](https://www.linkedin.com/legal/user-agreement) and can lead to restrictions or bans on your account. Use it at your own risk. The authors and contributors accept no responsibility for consequences arising from its use.

Recommendations if you use it anyway:

- Enable "pause before submit" until you trust your configured answers
- Keep application volumes reasonable — mass-applying gets accounts flagged
- Review the AI-tailored resume output periodically; the prompt forbids fabrication, but you are responsible for what gets submitted

## 🙏 Credits

This project is based on [Auto_job_applier_linkedIn](https://github.com/GodsScion/Auto_job_applier_linkedIn) by Sai Vignesh Golla and its community contributors. The resume keyword tailoring pipeline and assorted fixes were added in this fork.

## ⚖️ License

Licensed under the [GNU Affero General Public License v3.0](LICENSE) (AGPL-3.0), the same license as the original project. You are free to use, modify, and redistribute this software under the terms of that license.
