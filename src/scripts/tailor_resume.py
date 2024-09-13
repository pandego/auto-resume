import argparse
import json
import os
import sys

from loguru import logger
from rich import print as rprint

from src.models.tailored_resume_model import *
from src.models.utils import extract_contact_info, extract_education
from src.prompts.tailor_resume_prompts import *
from src.scripts.utils import load_data_from_json, save_to_json
from src.service.client import get_client

# ------------------------- #
# --- Initialize Client --- #
# ------------------------- #

use_structured_output: bool = False  # only for OpenAI for now
client_type: str = "openai"
# client_type = "groq"
# client_type = "openrouter"    # not implemented yet
# client_type = "ollama"        # not implemented yet

client = get_client(
    client_type=client_type,
)

if client_type == "openai":
    model: str = os.environ.get("OPENAI_MODEL_NAME")
elif client_type == "groq":
    model: str = os.environ.get("GROQ_MODEL_NAME")
elif client_type == "openrouter":
    model: str = os.environ.get("OPENROUTER_MODEL_NAME")
elif client_type == "ollama":
    model: str = os.environ.get("OLLAMA_MODEL_NAME")

# ------------------------ #
# --- Define Functions --- #
# ------------------------ #

if client_type == "openai" and use_structured_output:

    def tailor_resume(resume: str, job_description: str) -> Dict:
        prompt = tailor_resume_prompt_template.format(
            resume=resume, job_description=job_description
        )
        completion = client.beta.chat.completions.parse(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that tailors resumes to job descriptions.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            response_format=TailoredResume,
        )
        return completion.choices[0].message.parsed.model_dump()

else:

    # --- Introduction --- #
    def generate_introduction(resume: Dict, job_description: Dict) -> str:
        """
        Generate an introduction based on the resume and job description.
        """
        prompt = introduction_prompt_template.format(resume=resume,
                                                     job_description=job_description)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=512,
            temperature=0.2,  # 0.2 is a good temperature for generating text
            seed=42,
        )

        introduction = response.choices[0].message.content.strip()

        return introduction


    # --- Skills --- #
    def generate_skills(resume: Dict, job_description: Dict) -> Skills:
        """
        Generate a list of skills based on the skills section of the resume and job description.
        """
        prompt = skills_prompt_template.format(skills_section=resume.get("skills"),
                                               job_description=job_description)

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=512,
                temperature=0.0,
                seed=42,
            )

            skills = json.loads(response.choices[0].message.content.strip())


        except Exception as e:
            logger.error(f"Error generating skills:\n   {e}")
            logger.warning("Returning empty skills.")
            return Skills(
                programming_languages=[],
                technical_stack=[],
                soft_skills=[])

        return Skills(
            programming_languages=skills.get("programming_languages"),
            technical_stack=skills.get("technical_stack"),
            soft_skills=skills.get("soft_skills"))


    # --- Experience --- #
    def generate_experience(resume: Dict, job_description: Dict) -> List[ExperienceItem]:
        prompt = experience_prompt_template.format(experience_section=resume.get("experience"),
                                                   job_description=job_description)

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1024,
                temperature=0.0,
                seed=42,
            )

            experience_list = json.loads(response.choices[0].message.content.strip())

        except Exception as e:
            logger.error(f"Error generating experiences:\n   {e}")
            logger.warning("Returning empty experience.")
            return [ExperienceItem(
                title="",
                company="",
                period="",
                summary=[],
            )]

        return [ExperienceItem(**item) for item in experience_list]


    # --- Certifications --- #
    def generate_certifications(resume: Dict, job_description: Dict) -> List[CertificationItem]:
        prompt = certifications_prompt_template.format(certificate_section=resume.get("certificates"),
                                                       job_description=job_description)

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=512,
                temperature=0.0,
                seed=42,
            )

            certification_list = json.loads(response.choices[0].message.content.strip())

        except Exception as e:
            logger.error(f"Error generating certifications:\n   {e}")
            logger.warning("Returning empty certifications.")
            return [CertificationItem(
                title="",
                institution="",
                year=0,
            )]

        return [CertificationItem(**item) for item in certification_list]


    # --- Interests --- #
    def generate_interests(resume: Dict, job_description: Dict) -> List[str]:
        prompt = interests_prompt_template.format(interest_section=resume.get("interests"),
                                                  job_description=job_description)

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=512,
                temperature=0.0,
                seed=42,
            )

            interests_list = (
                response.choices[0].message.content.strip().split(", "))  # since we want a 'list' of keywords

        except Exception as e:
            logger.error(f"Error generating interests:\n   {e}")
            logger.warning("Returning empty interests.")
            return []

        return interests_list


    def tailor_resume(resume: dict, job_description: dict) -> Dict:
        # Extract information directly from the resume or job description
        contact_info = extract_contact_info(resume)
        # contact_info = resume.get("contact_info", {})
        # languages = extract_languages(resume)
        languages = resume.get("languages", [])
        education = extract_education(resume)
        company_applying = job_description.get("Company", "Unknown")

        # Generate tailored sections
        introduction = generate_introduction(resume, job_description)
        skills = generate_skills(resume, job_description)
        experiences = generate_experience(resume, job_description)
        certifications = generate_certifications(resume, job_description)
        interests = generate_interests(resume, job_description)

        tailored_resume = TailoredResumeData(
            # Extracted information
            company_applying=company_applying,
            contact_info=contact_info,
            languages=languages,
            education=education,
            # Generated sections
            introduction=introduction,
            skills=skills,
            experiences=experiences,
            certifications=certifications,
            interests=interests,
        )

        return tailored_resume.model_dump()  # Return structured data


# ------------------- #
# --- Script Args --- #
# ------------------- #


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate a tailored resume based on job description"
    )
    parser.add_argument(
        "--resume_path",
        default="data/resume_data/structured/resume_data_v2.json",
        help="Path to the resume file",
    )
    parser.add_argument(
        "--job_description_path",
        default="data/job_descriptions/structured/Chief_Barkology_Officer_(CBO)_DoggoTech_Solutions.json",
        help="Path to the job description file",
    )
    parser.add_argument(
        "--output_path",
        default="outputs/resumes",
        help="Path to the output folder",
    )

    return parser.parse_args()


# ------------ #
# --- Main --- #
# ------------ #

def main(
        input_resume_path: str = "data/resume_data/structured/resume_data_v2.json",
        input_job_description_path: str = "data/job_descriptions/structured/Chief_Barkology_Officer_(CBO)_DoggoTech_Solutions.json",
        output_folder: str = "outputs/resumes",
) -> None:
    try:
        # Load Structured Resume & Job Description from JSON files
        resume_data = load_data_from_json(input_resume_path)
        job_description = load_data_from_json(input_job_description_path)

        # Generate Tailored Resume
        tailored_resume = tailor_resume(resume_data, job_description)
        rprint(tailored_resume)

        # Save the tailored resume to JSON
        save_to_json(tailored_resume, output_folder, file_type="Tailored Resume")

    except FileNotFoundError as e:
        logger.error(f"Oups:\n   {e}")
        sys.exit(1)


if __name__ == "__main__":
    args = parse_args()

    main(
        input_resume_path=args.resume_path,
        input_job_description_path=args.job_description_path,
        output_folder=args.output_path,
    )
