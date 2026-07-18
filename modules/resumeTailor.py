'''
Tailors the default resume's keywords/skills to a job description for better ATS matching,
without changing the LaTeX template/layout or any resume facts (names, dates, companies, numbers).

Pipeline: resume_data.json (+ AI reword of bullets/skills only) -> fill resume_template.tex -> compile with Tectonic -> PDF.
'''

import json
import re
import subprocess
from pathlib import Path

from modules.helpers import print_lg, critical_error_log

RESUME_DIR = Path("all resumes/default")
TEMPLATE_PATH = RESUME_DIR / "resume_template.tex"
DATA_PATH = RESUME_DIR / "resume_data.json"
TAILORED_DIR = Path("all resumes/tailored")

_LATEX_SPECIAL = {
    "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
    "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
}
_LATEX_SPECIAL_RE = re.compile("|".join(re.escape(k) for k in _LATEX_SPECIAL))


def _escape_latex(value: str) -> str:
    '''
    Escapes LaTeX special characters in plain-text values so injected content can't break compilation.
    Skips values that already contain a backslash (assumed to be pre-escaped, e.g. "Data Structures \\& Algorithms").
    '''
    if "\\" in value:
        return value
    return _LATEX_SPECIAL_RE.sub(lambda m: _LATEX_SPECIAL[m.group(0)], value)


def load_resume_data() -> dict:
    '''
    Loads the structured resume content (facts) from `resume_data.json`.
    '''
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)


def _placeholders_from_data(data: dict) -> dict[str, str]:
    '''
    Flattens `resume_data` into the exact `%%PLACEHOLDER%%` keys used by `resume_template.tex`.
    '''
    skills = data["skills"]
    return {
        "NAME": data["name"],
        "LOCATION": data["location"],
        "PHONE": data["phone"],
        "EMAIL": data["email"],
        "LINKEDIN_URL": data["linkedin_url"],
        "LINKEDIN_LABEL": data["linkedin_label"],
        "GITHUB_URL": data["github_url"],
        "GITHUB_LABEL": data["github_label"],

        "SCHOOL": data["school"],
        "SCHOOL_DATES": data["school_dates"],
        "DEGREE": data["degree"],
        "SCHOOL_LOCATION": data["school_location"],

        "JOB1_TITLE": data["job1_title"],
        "JOB1_COMPANY": data["job1_company"],
        "JOB1_DATES": data["job1_dates"],
        "JOB1_LOCATION": data["job1_location"],
        "JOB1_BULLET1": data["job1_bullets"][0],
        "JOB1_BULLET2": data["job1_bullets"][1],
        "JOB1_BULLET3": data["job1_bullets"][2],
        "JOB1_BULLET4": data["job1_bullets"][3],

        "PROJ1_NAME": data["proj1_name"],
        "PROJ1_STACK": data["proj1_stack"],
        "PROJ1_GITHUB_URL": data["proj1_github_url"],
        "PROJ1_BULLET1": data["proj1_bullets"][0],
        "PROJ1_BULLET2": data["proj1_bullets"][1],
        "PROJ1_BULLET3": data["proj1_bullets"][2],
        "PROJ1_BULLET4": data["proj1_bullets"][3],

        "PROJ2_NAME": data["proj2_name"],
        "PROJ2_STACK": data["proj2_stack"],
        "PROJ2_GITHUB_URL": data["proj2_github_url"],
        "PROJ2_BULLET1": data["proj2_bullets"][0],
        "PROJ2_BULLET2": data["proj2_bullets"][1],
        "PROJ2_BULLET3": data["proj2_bullets"][2],
        "PROJ2_BULLET4": data["proj2_bullets"][3],

        "SKILLS_LANGUAGES": skills["languages"],
        "SKILLS_FRONTEND": skills["frontend"],
        "SKILLS_BACKEND": skills["backend"],
        "SKILLS_DATABASE": skills["database"],
        "SKILLS_TOOLS": skills["tools"],
        "SKILLS_SOFTWARE_ENGINEERING": skills["software_engineering"],
        "SKILLS_CORE_CS": skills["core_cs"],

        "DSA_BULLET1": data["dsa_bullets"][0],
        "DSA_BULLET2": data["dsa_bullets"][1],

        "AWARD_BULLET1": data["award_bullets"][0],
        "AWARD_BULLET2": data["award_bullets"][1],
        "AWARD_BULLET3": data["award_bullets"][2],
        "AWARD_BULLET4": data["award_bullets"][3],
    }


def render_tex(data: dict) -> str:
    '''
    Fills `resume_template.tex` placeholders with `data` values (LaTeX-escaped). Template markup itself is never touched.
    '''
    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    for key, value in _placeholders_from_data(data).items():
        template = template.replace(f"%%{key}%%", _escape_latex(str(value)))
    leftover = re.findall(r"%%[A-Z0-9_]+%%", template)
    if leftover:
        raise ValueError(f"Unfilled placeholders remain in resume template: {leftover}")
    return template


def compile_tex_to_pdf(tex_source: str, output_name: str) -> Path:
    '''
    Writes `tex_source` to `all resumes/tailored/<output_name>.tex` and compiles it to PDF using Tectonic.
    * Returns the `Path` to the compiled PDF.
    * Raises `RuntimeError` if compilation fails.
    '''
    TAILORED_DIR.mkdir(parents=True, exist_ok=True)
    tex_path = TAILORED_DIR / f"{output_name}.tex"
    pdf_path = TAILORED_DIR / f"{output_name}.pdf"
    tex_path.write_text(tex_source, encoding="utf-8")

    result = subprocess.run(
        ["tectonic", str(tex_path), "--outdir", str(TAILORED_DIR)],
        capture_output=True, text=True, timeout=120,
    )
    if result.returncode != 0 or not pdf_path.exists():
        raise RuntimeError(f"Tectonic failed to compile resume:\n{result.stdout}\n{result.stderr}")
    return pdf_path


_BULLET_KEYS = ["job1_bullets", "proj1_bullets", "proj2_bullets", "dsa_bullets", "award_bullets"]
_SKILL_KEYS = ["languages", "frontend", "backend", "database", "tools", "software_engineering", "core_cs"]
_FACT_KEYS = [
    "name", "location", "phone", "email", "linkedin_url", "linkedin_label", "github_url", "github_label",
    "school", "school_dates", "degree", "school_location",
    "job1_title", "job1_company", "job1_dates", "job1_location",
    "proj1_name", "proj1_stack", "proj1_github_url",
    "proj2_name", "proj2_stack", "proj2_github_url",
]
_LENGTH_SLACK = 1.05  # allow at most 5% growth to absorb minor tokenization differences, not new clauses


def enforce_template_lock(original: dict, tailored: dict) -> dict:
    '''
    Guards against the AI drifting outside "keyword tailoring only": for every field, falls back to the
    ORIGINAL value if the AI changed a fixed fact, or grew a bullet/skills line beyond a small slack margin.
    This is what actually keeps the resume's template and content locked, not just the prompt wording.
    '''
    safe = dict(original)

    for key in _FACT_KEYS:
        if tailored.get(key) != original.get(key):
            print_lg(f"Resume tailoring altered fixed fact '{key}', reverting to original.")
            safe[key] = original[key]

    for key in _BULLET_KEYS:
        orig_list = original[key]
        new_list = tailored.get(key)
        if not isinstance(new_list, list) or len(new_list) != len(orig_list):
            safe[key] = orig_list
            continue
        safe[key] = [
            new if isinstance(new, str) and len(new) <= len(orig) * _LENGTH_SLACK else orig
            for orig, new in zip(orig_list, new_list)
        ]

    orig_skills = original["skills"]
    new_skills = tailored.get("skills") if isinstance(tailored.get("skills"), dict) else {}
    safe_skills = dict(orig_skills)
    for key in _SKILL_KEYS:
        new_val = new_skills.get(key)
        if isinstance(new_val, str) and len(new_val) <= len(orig_skills[key]) * _LENGTH_SLACK:
            safe_skills[key] = new_val
    safe["skills"] = safe_skills

    return safe


def generate_tailored_resume(job_description: str, job_id: str, ai_client=None) -> str:
    '''
    Produces a keyword-tailored resume PDF for a specific job, keeping the template and all resume facts fixed.
    * Takes in `job_description` of type `str`.
    * Takes in `job_id` of type `str`, used to name the output file uniquely.
    * Takes in `ai_client`, an already-created OpenAI-compatible client. If `None`, skips AI tailoring and just
      renders the original resume content through the fixed template (still produces a valid PDF).
    * Returns path (as `str`) to the tailored resume PDF. Falls back to the static default resume path on any failure.
    '''
    from config.questions import default_resume_path

    try:
        data = load_resume_data()

        if ai_client is not None:
            from modules.ai.openaiConnections import ai_tailor_resume_keywords
            tailored = ai_tailor_resume_keywords(ai_client, job_description, data)
            data = enforce_template_lock(data, tailored)

        tex_source = render_tex(data)
        safe_job_id = re.sub(r"[^A-Za-z0-9_-]", "_", str(job_id))
        pdf_path = compile_tex_to_pdf(tex_source, f"resume_{safe_job_id}")
        print_lg(f"Generated tailored resume: {pdf_path}")
        return str(pdf_path)
    except Exception as e:
        critical_error_log("Failed to generate tailored resume, falling back to default resume.", e)
        return default_resume_path
