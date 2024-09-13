# ------------------------- #
# --- Structured Output --- #
# ------------------------- #

# One prompt to rule them all 🤣
tailor_resume_prompt_template: str = """
You will be provided with a candidate's resume and a detailed job description. Based on the information provided, extract or generate the following details:

1. **Contact Information**: Extract and format the contact information from the resume. Include name, phone, email, and optional fields like LinkedIn, GitHub, Medium, Twitter, or homepage if they are available. Do not fabricate any information. 
    Format:
    {{
        "name": "",
        "phone": "",
        "city_country": "",
        "email": "",
        "linkedin": "",
        "github": "",
        "medium": "",
        "twitter": "",
        "homepage": "",
        "role": ""
    }}

2. **Professional Summary**: Create a tailored professional summary or career objective based on both the resume and job description. Highlight key qualifications that match the job requirements, focusing on the candidate's most relevant skills and experiences.
    Format:
    "summary": ""

3. **Skills**: Categorize and extract the candidate's skills, emphasizing those most relevant to the job description. Organize the skills into categories such as programming languages, technical stack, soft skills, and spoken languages with proficiency levels.
    Format:
    {{
        "programming_languages": [],
        "technical_stack": [],
        "soft_skills": []
    }}

4. **Languages**: Extract and format the candidate's languages and their proficiency levels.
    Format:
    {{
        "languages": [
            {{"English": 4}},
            {{"French": 5}}
        ]
    }}

5. **Work Experience**: Tailor the work experience entries to highlight responsibilities and achievements most relevant to the job description. For each entry, provide the job title, company, period, key tasks/responsibilities, and achievements.
    Format:
    [
        {{
            "title": "",
            "company": "",
            "period": "",
            "missions": [],
            "results": []
        }}
    ]

6. **Education**: Extract and format the candidate's education details, including the degree, institution, period of study, and grade if available.
    Format:
    [
        {{
            "degree": "",
            "institution": "",
            "period": "",
            "grade": ""
        }}
    ]

7. **Certifications**: If available, extract certifications from the resume. Include the certification title, issuing institution, and year obtained. Focus on certifications relevant to the job.
    Format:
    [
        {{
            "title": "",
            "institution": "",
            "year": ""
        }}
    ]

8. **Interests**: If provided, extract interests or hobbies that may be relevant or interesting for the job application. Limit the list to 3-5 key interests.
    Format:
    "interests": []

Here is the candidate's resume:
"{resume}"

Here is the job description:
"{job_description}"
"""

# --------------------------- #
# --- Unstructured Output --- #
# --------------------------- #

# 1. Objective Prompt
# introduction_prompt_template: str = """
# Based on the resume data and job description, create a tailored professional summary or career objective.
# Highlight key qualifications that match the job requirements, focusing on the candidate's most relevant skills and experiences.
# Do not invent any information, but adjust the focus of the summary to better align with the job description.
# Here is the resume data:
# "{resume}"
# Here is the job description:
# "{job_description}"
# """
introduction_prompt_template: str = """
Generate a concise, tailored professional summary based **only** on the resume provided and aligned with the job description.
Highlight key qualifications and experiences relevant to the job, but do **not** create or invent any new information.
The summary should be derived entirely from the resume without adding external details. 

Ensure the output is no longer than 2-3 sentences, with no introductions or explanations.

Resume:
"{resume}"

Job Description:
"{job_description}"

Output only the professional summary.

"""

# 2. Skills Prompt
# skills_prompt_template: str = """
# Given the resume data extract and categorize skills from the resume, emphasizing those most relevant to the job description.
# Organize the skills into categories such as programming languages, technical stack, soft skills, and spoken languages with proficiency levels.
# Do not make up any information; use only the details provided in the resume.
# Here is the resume data:
# "{resume}"
# Here is the job description:
# "{job_description}"
# Format the output as follows, nothing else but the JSON and nothing else but the keys in the example output:
#
# Example Output:
# {{
#     "programming_languages": ["Python", "SQL", "R"]
#     "technical_stack": ["TensorFlow", "Keras", "Azure", "Docker", "Git", "Azure DevOps"]
#     "soft_skills": ["Leadership", "Communication", "Problem-solving"]
#     ]
# }}
# """
skills_prompt_template: str = """
Extract and categorize the most relevant skills from the resume, focusing specifically on those that align with the job description.
Organize the skills into the following categories: "programming_languages," "technical_stack," and "soft_skills." 

Only use skills explicitly mentioned in the resume, and do **not** invent or infer any information.
Ensure the output is in JSON format with **only** the required keys and values.

Here is the resume skills data:
"{skills_section}"

Here is the job description:
"{job_description}"

Format the output exactly as follows, with no additional text or explanations:

Example Output:
{{
    "programming_languages": ["Python", "SQL", "R"],
    "technical_stack": ["LangChain", "Keras", "Azure", "Docker", "Git", "Azure DevOps"],
    "soft_skills": ["Leadership", "Communication", "Problem-solving"]
}}

"""

# 4. Experience Prompt
# experience_prompt_template: str = """
# Tailor the work experience entries to highlight responsibilities and achievements most relevant to the job description.
# For each entry, provide the job title, company, period, missions (key tasks and responsibilities), and results (achievements and impact).
# Do not fabricate any information, but emphasize the most relevant experiences for the job.
# Here is the resume data:
# "{resume}"
# Here is the job description:
# "{job_description}"
# Format the output as follows, nothing else but the JSON and nothing else but the keys in the example output:
#
# Example Output:
# [
#     {{
#         "title": "Senior AI Engineer",
#         "company": "BarkTech",
#         "period": "Jan 2019 - Present",
#         "missions": [
#             "Developed AI models for pet activity recognition.",
#             "Led a team of dog-inspired data scientists."
#         ],
#         "results": [
#             "Increased customer retention by 15% through predictive activity models.",
#             "Developed a real-time barking translation feature."
#         ]
#     }},
#     {{
#         "title": "Machine Learning Engineer",
#         "company": "PetAI Solutions",
#         "period": "Jun 2016 - Dec 2018",
#         "missions": [
#             "Built machine learning pipelines for pet recognition software.",
#             "Collaborated with the dev team to create innovative pet tracking solutions."
#         ],
#         "results": [
#             "Reduced pet location tracking errors by 25%.",
#             "Implemented a novel fur pattern recognition algorithm."
#         ]
#     }}
# ]
# """
experience_prompt_template: str = """
Create a tailored summary of work experience entries by merging the most relevant responsibilities (missions) and achievements (results) into concise bullet points.
Focus only on the experiences most relevant to the job description.

For each job entry, provide:
- Job title
- Company
- Period of employment
- A summary list, combining key tasks, responsibilities, achievements, and impact into concise points tailored to the job description, limiting the summary to 2-3 bullet points.

Use only the information provided in the experience section of the resume. **Do not fabricate or invent any information.**

Here is the experience section of the resume:
"{experience_section}"

Here is the job description:
"{job_description}"

Format the output as follows, with no extra text or explanations, and nothing but the required JSON structure:

Example Output:
[
    {{
        "title": "Senior AI Engineer",
        "company": "BarkTech",
        "period": "Jan 2019 - Present",
        "summary": [
            "Increased customer retention by 15% through predictive activity models.",
            "Developed a real-time barking translation feature that improved user engagement by 20%."
        ]
    }},
    {{
        "title": "Machine Learning Engineer",
        "company": "PetAI Solutions",
        "period": "Jun 2016 - Dec 2018",
        "summary": [
            "Built machine learning pipelines for pet recognition software.",
            "Collaborated with the dev team to create innovative pet tracking solutions."
        ]
    }}
]

"""

# 5. Education Prompt
# education_prompt_template: str = """
# Extract and format the education information from the resume.
# Include the degree, institution, period of study, and grade (if available).
# Do not invent any information, and format the education details correctly.
# Here is the resume data:
# "{resume}"
# Format the output as follows, nothing else but the JSON and nothing else but the keys in the example output:
#
# Example Output:
# [
#     {{
#         "degree": "Master's degree in AI for Pets",
#         "institution": "Paw University",
#         "period": "2015 - 2017",
#         "grade": "Summa Cum Laude"
#     }},
#     {{
#         "degree": "Bachelor's degree in Data Science",
#         "institution": "Bark Institute of Technology",
#         "period": "2011 - 2015",
#         "grade": "Magna Cum Laude"
#     }}
# ]
# """

# 6. Certifications Prompt
# certifications_prompt_template: str = """
# If available, extract certification information from the resume.
# Include the certification title, issuing institution, and year obtained.
# Select only the most relevant certifications that are most relevant to the job description.
# Do not fabricate any details; only include certifications found in the resume.
# Here is the resume data:
# "{resume}"
# Here is the job description:
# "{job_description}"
# Format the output as follows, nothing else but the JSON and nothing else but the keys in the example output:
#
# Example Output:
# [
#         {{
#             "title": "Certified PetAI Specialist",
#             "institution": "PetAI Academy",
#             "year": 2020
#         }},
#         {{
#             "title": "Advanced Bark Recognition Expert",
#             "institution": "Canine Tech",
#             "year": 2018
#         }}
# ]
# """
certifications_prompt_template: str = """
Extract up to 4 of the most relevant certifications from the certificate section of the resume, focusing on those that align most closely with the job description.
For each certification, include the title, issuing institution, and year obtained.

Only use the certification information provided in the resume. **Do not fabricate or invent any details.**

Here is the certification section of the resume:
"{certificate_section}"

Here is the job description:
"{job_description}"

Format the output exactly as follows, with no extra text or explanations, and nothing but the required JSON structure:

Example Output:
[
    {{
        "title": "Certified PetAI Specialist",
        "institution": "PetAI Academy",
        "year": 2020
    }},
    {{
        "title": "Advanced Bark Recognition Expert",
        "institution": "Canine Tech",
        "year": 2018
    }}
]

"""

# 7. Interests Prompt
# interests_prompt_template: str = """
# If provided, extract interests or hobbies from the resume that might be relevant or interesting for the job application.
# Do not add any fictional information; only include what is found in the resume.
# Limit the list to 3-5 key interests.
# Separate each interest with a comma (,).
# Here is the resume data:
# "{resume}"
# Here is the job description:
# "{job_description}"
# """
interests_prompt_template: str = """
Extract up to 3-4 hobbies or interests from the resume that may be relevant or interesting for the job application. Focus on those that align with the job description, and do **not** invent or infer any information.

Only include hobbies found in the resume and ensure that the output is a list of strings.

Here is the hobbies/interests section of the resume:
"{interest_section}"

Here is the job description:
"{job_description}"

Format the output exactly as follows, with no extra text or explanations:

Example Output:
"Barking", "Howling at the moon", "Dog to Human translation"

"""
