# ------------------------- #
# --- Structured Output --- #
# ------------------------- #

# One prompt to rule them all 🤣
process_job_prompt_template: str = """
You will be provided with a detailed job description. Based on the description, please extract and generate the following information:

1. **Summary**: Write a concise summary that captures the core responsibilities, key qualifications, and overall mission of the job. The summary should be in a single block of plain text without formatting.
2. **Job Title**: Extract the exact job title. If no title is explicitly stated, generate one based on the description.
3. **Company Name**: Extract the exact company name. If no company name is found, output "No company name found".
4. **Location**: Extract the exact job location (City, Country) or state "Remote" if the job is fully remote. If no location or remote work is found, output "No location found".
5. **Technical Skills**: List the 5-7 key technical skills required, focusing on core programming languages, frameworks, and tools. Use "Proficient in" or "Familiar with" to indicate skill level, separating each skill with a comma (,).
6. **Soft Skills**: List 3-5 key soft skills relevant to the job, separating each skill with a comma (,).
7. **Qualifications**: Generate a list of the key qualifications based on the job description. Each qualification should be on a new line.
8. **Key Responsibilities**: Generate a list of key responsibilities based on the job description. Each responsibility should be on a new line.
9. **Missions**: Extract a list of key missions or purposes of the job, each on a new line.

Here is the job description:
"{text}"
"""


# --------------------------- #
# --- Unstructured Output --- #
# --------------------------- #

# 1. Summarize the Job Description
summary_generation_prompt_template: str = """
You will be provided with a detailed job description.
Write a concise summary that captures the core responsibilities, key qualifications, and overall mission of the job.
Do not include any formatting such as paragraphs, bold text, bullet points, or extra new lines.
Ensure the summary is written as a single block of plain text.
Here is the job description:
"{text}"
"""


# 2. Extract Job Title from Description
title_extraction_prompt_template: str = """
You will be provided with a job description.
Extract only the exact job title from the description without any additional text, headers, or formatting.
Do not generate or infer a title; only output the title explicitly stated in the text.
If no title is explicitly stated, output "No title found".
Here is the job description:
"{text}"
"""

# 3. Extract Company from the Description
company_extraction_prompt_template: str = """
You will be provided with a job description.
Extract only the exact company name from the description without any additional text, headers, or formatting.
Do not generate or infer a company name; only output the company name explicitly stated in the text.
If no company name is explicitly stated, output "No company name found".
Here is the job description:
"{text}"
"""

# 4. Extract Location from the Description
location_extraction_prompt_template: str = """
You will be provided with a job description.
Extract only the exact location (City, Country) from the description without any additional text, headers, or formatting.
If the job is described as fully remote, output "Remote" instead of a location.
Do not generate or infer a location; only output the location or 'Remote' if explicitly stated in the text.
If no location or remote work is explicitly stated, output "No location found".
Here is the job description:
"{text}"
"""


# 5. Extract Technical Skills from the Description
technical_skills_extraction_prompt_template: str = """
You will be provided with a job description.
Generate a concise list of relevant technical skills required for the job based on the description.
Focus on core programming languages, frameworks, and tools.
Avoid listing common libraries or packages.
Use "proficient in" or "familiar with" to indicate skill level.
Do not use numbering or bullet points.
Limit the list to 5-7 key technical skills.
Separate each skill with a comma (,).
Here is the job description:
"{text}"
"""

# 6. Extract Soft Skills from the Description
soft_skills_extraction_prompt_template: str = """
You will be provided with a job description.
Generate a brief list of relevant soft skills required for the job based on the description.
Focus on interpersonal and professional qualities.
Do not use numbering or bullet points.
Limit the list to 3-5 key soft skills.
Separate each skill with a comma (,).
Here is the job description:
"{text}"
"""

# 7. Extract Qualifications from the Description
qualifications_extraction_prompt_template: str = """
You will be provided with a job description.
Generate a list of key qualifications for this role based on the job description.
Ensure that only meaningful qualifications are included. 
Do not include any empty qualifications, additional formatting, or line breaks.
Separate each qualification by a new line.
Here is the job description:
"{text}"
"""


# 8. Extract Responsibilities from the Description
responsibilities_extraction_prompt_template: str = """
You will be provided with a job description.
Generate a list of key responsibilities for this role based on the job description.
Ensure each responsibility is meaningful and do not include empty lines or unnecessary formatting.
Do not use numbering or bullets.
Separate each responsibility by a new line.
Here is the job description:
"{text}"
"""


# 9. Extract Missions from the Description
missions_extraction_prompt_template: str = """
You will be provided with a job description.
Extract a list of key missions or purposes of the job.
Each mission should be meaningful and avoid any empty or irrelevant entries.
Do not include additional line breaks or formatting.
Separate each mission by a new line.
Here is the job description:
"{text}"
"""


# 10. Generate Job Title by Description
title_generation_prompt_template: str = """
You will be provided with a detailed job description.
Generate a new job title that best fits the description if the provided title does not match the responsibilities.
Ensure the job title is less than 5 words and is written in plain text without any additional characters, formatting, or newlines.
Here is the job description:
"{text}"
"""
