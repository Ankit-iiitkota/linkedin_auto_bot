##> Common Response Formats
array_of_strings = {"type": "array", "items": {"type": "string"}}
"""
Response schema to represent array of strings `["string1", "string2"]`
"""
#<


##> Extract Skills

# Structure of messages = `[{"role": "user", "content": extract_skills_prompt}]`

extract_skills_prompt = """
You are a job requirements extractor and classifier. Your task is to extract all skills mentioned in a job description and classify them into five categories:
1. "tech_stack": Identify all skills related to programming languages, frameworks, libraries, databases, and other technologies used in software development. Examples include Python, React.js, Node.js, Elasticsearch, Algolia, MongoDB, Spring Boot, .NET, etc.
2. "technical_skills": Capture skills related to technical expertise beyond specific tools, such as architectural design or specialized fields within engineering. Examples include System Architecture, Data Engineering, System Design, Microservices, Distributed Systems, etc.
3. "other_skills": Include non-technical skills like interpersonal, leadership, and teamwork abilities. Examples include Communication skills, Managerial roles, Cross-team collaboration, etc.
4. "required_skills": All skills specifically listed as required or expected from an ideal candidate. Include both technical and non-technical skills.
5. "nice_to_have": Any skills or qualifications listed as preferred or beneficial for the role but not mandatory.
Return the output in the following JSON format with no additional commentary:
{{
    "tech_stack": [],
    "technical_skills": [],
    "other_skills": [],
    "required_skills": [],
    "nice_to_have": []
}}

JOB DESCRIPTION:
{}
"""
"""
Use `extract_skills_prompt.format(job_description)` to insert `job_description`.
"""

# DeepSeek-specific optimized prompt, emphasis on returning only JSON without using json_schema
deepseek_extract_skills_prompt = """
You are a job requirements extractor and classifier. Your task is to extract all skills mentioned in a job description and classify them into five categories:
1. "tech_stack": Identify all skills related to programming languages, frameworks, libraries, databases, and other technologies used in software development. Examples include Python, React.js, Node.js, Elasticsearch, Algolia, MongoDB, Spring Boot, .NET, etc.
2. "technical_skills": Capture skills related to technical expertise beyond specific tools, such as architectural design or specialized fields within engineering. Examples include System Architecture, Data Engineering, System Design, Microservices, Distributed Systems, etc.
3. "other_skills": Include non-technical skills like interpersonal, leadership, and teamwork abilities. Examples include Communication skills, Managerial roles, Cross-team collaboration, etc.
4. "required_skills": All skills specifically listed as required or expected from an ideal candidate. Include both technical and non-technical skills.
5. "nice_to_have": Any skills or qualifications listed as preferred or beneficial for the role but not mandatory.

IMPORTANT: You must ONLY return valid JSON object in the exact format shown below - no additional text, explanations, or commentary.
Each category should contain an array of strings, even if empty.

{{
    "tech_stack": ["Example Skill 1", "Example Skill 2"],
    "technical_skills": ["Example Skill 1", "Example Skill 2"],
    "other_skills": ["Example Skill 1", "Example Skill 2"],
    "required_skills": ["Example Skill 1", "Example Skill 2"],
    "nice_to_have": ["Example Skill 1", "Example Skill 2"]
}}

JOB DESCRIPTION:
{}
"""
"""
DeepSeek optimized version, use `deepseek_extract_skills_prompt.format(job_description)` to insert `job_description`.
"""


extract_skills_response_format = {
    "type": "json_schema",
    "json_schema": {
        "name": "Skills_Extraction_Response",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "tech_stack": array_of_strings,
                "technical_skills": array_of_strings,
                "other_skills": array_of_strings,
                "required_skills": array_of_strings,
                "nice_to_have": array_of_strings,
            },
            "required": [
                "tech_stack",
                "technical_skills",
                "other_skills",
                "required_skills",
                "nice_to_have",
            ],
            "additionalProperties": False
        },
    },
}
"""
Response schema for `extract_skills` function
"""
#<

##> ------ Dheeraj Deshwal : dheeraj9811 Email:dheeraj20194@iiitd.ac.in/dheerajdeshwal9811@gmail.com - Feature ------
##> Answer Questions
# Structure of messages = `[{"role": "user", "content": answer_questions_prompt}]`

ai_answer_prompt = """
You are an intelligent AI assistant filling out a form and answer like human,. 
Respond concisely based on the type of question:

1. If the question asks for **years of experience, duration, or numeric value**, return **only a number** (e.g., "2", "5", "10").
2. If the question is **a Yes/No question**, return **only "Yes" or "No"**.
3. If the question requires a **short description**, give a **single-sentence response**.
4. If the question requires a **detailed response**, provide a **well-structured and human-like answer and keep no of character <350 for answering**.
5. Do **not** repeat the question in your answer.
6. here is user information to answer the questions if needed:
**User Information:** 
{}

**QUESTION Strat from here:**
{}
"""
#<


##> Tailor Resume Keywords (ATS optimization only, template/content locked)
# Structure of messages = `[{"role": "user", "content": tailor_resume_keywords_prompt}]`

tailor_resume_keywords_prompt = """
You are an ATS (Applicant Tracking System) keyword optimizer. You will be given:
1. A job description.
2. My resume content as a JSON object.

Your ONLY task is to slightly rephrase wording to naturally include keywords/skills from the job description that I genuinely already have evidence of in my resume, so the resume scores higher on ATS keyword matching for this specific job.

STRICT RULES - you must follow these exactly:
1. Do NOT invent, add, or claim any skill, tool, technology, employer, project, title, date, award, or achievement that is not already present in my resume content below. Never fabricate experience.
2. Do NOT change the structure of the JSON - keep every key exactly as given, do not add or remove keys.
3. Do NOT change facts: names, companies, dates, degree, school, project names, award names, or numbers (like "400+", "1587", "3-Star").
4. You MAY only:
   a. Reword bullet point sentences (in job1_bullets, proj1_bullets, proj2_bullets, dsa_bullets, award_bullets) to naturally weave in exact keyword phrases from the job description IF the underlying skill/action is already implied by the original bullet. Each rewritten bullet's character count MUST be LESS THAN OR EQUAL TO the original bullet's character count - never longer. Prefer replacing a generic phrase with a specific JD keyword of similar length over appending new clauses. Do not append trailing phrases like ", with a focus on X" or ", ensuring Y" - these make bullets longer and are NOT allowed.
   b. Reorder or lightly rephrase the comma-separated skill strings inside "skills" (languages, frontend, backend, database, tools, software_engineering, core_cs) to prioritize/emphasize the ones matching the job description first, but you may NOT add a skill/tool that isn't already listed somewhere in the original resume content, and the total character count of each skills line must not increase.
5. Every value you output must remain factually a subset of what's implied by the ORIGINAL content given to you. When unsure, leave the original wording unchanged.
6. Return ONLY the complete JSON object with the same schema as the input, with your edits applied. No commentary, no markdown fences.

JOB DESCRIPTION:
{}

MY RESUME CONTENT (JSON):
{}
"""
"""
Use `tailor_resume_keywords_prompt.format(job_description, resume_data_json_string)` to insert values.
"""
#<