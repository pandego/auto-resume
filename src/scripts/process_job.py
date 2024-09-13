import argparse
import json
import os
import sys
from typing import Dict, List

from loguru import logger
from rich import print as rprint

from src.models.job_model import JobDescription
from src.prompts.job_prompts import *
from src.scripts.utils import load_file_from_txt, save_to_json
from src.service.client import get_client

# ------------------------- #
# --- Initialize Client --- #
# ------------------------- #

use_structured_output: bool = True  # only for OpenAI for now
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

    def parse_job_description(job_description: str) -> Dict:
        prompt = process_job_prompt_template.format(text=job_description)
        completion = client.beta.chat.completions.parse(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that extracts information from job descriptions.",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            response_format=JobDescription,
        )
        return completion.choices[0].message.parsed.model_dump()

else:

    def get_summary(job_description: str) -> str:
        prompt = summary_generation_prompt_template.format(text=job_description)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            max_tokens=1024,
            temperature=0.0,
            seed=42,
        )
        return response.choices[0].message.content


    def get_title(job_description: str) -> str:
        prompt = title_extraction_prompt_template.format(text=job_description)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            max_tokens=1024,
            temperature=0.0,
            seed=42,
        )
        return response.choices[0].message.content.strip()


    def get_company(job_description: str) -> str:
        prompt = company_extraction_prompt_template.format(text=job_description)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            max_tokens=1024,
            temperature=0.0,
            seed=42,
        )
        return response.choices[0].message.content.strip()


    def get_location(job_description: str) -> str:
        prompt = location_extraction_prompt_template.format(text=job_description)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            max_tokens=1024,
            temperature=0.0,
            seed=42,
        )
        return response.choices[0].message.content.strip()


    def get_technical_skills(job_description: str) -> List[str]:
        prompt = technical_skills_extraction_prompt_template.format(
            text=job_description
        )
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            max_tokens=1024,
            temperature=0.0,
            seed=42,
        )
        return (
            response.choices[0].message.content.strip().split(", ")
        )  # since we want a 'list' of keywords


    def get_soft_skills(job_description: str) -> List[str]:
        prompt = soft_skills_extraction_prompt_template.format(text=job_description)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            max_tokens=1024,
            temperature=0.0,
            seed=42,
        )
        return (
            response.choices[0].message.content.strip().split(", ")
        )  # since we want a 'list' of keywords


    def get_qualifications(job_description: str) -> List[str]:
        prompt = qualifications_extraction_prompt_template.format(text=job_description)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            max_tokens=1024,
            temperature=0.0,
            seed=42,
        )
        return (
            response.choices[0].message.content.strip().split("\n")
        )  # since we want a 'list' of qualifications


    def get_responsibilities(job_description: str) -> List[str]:
        prompt = responsibilities_extraction_prompt_template.format(
            text=job_description
        )
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            max_tokens=1024,
            temperature=0.0,
            seed=42,
        )
        return (
            response.choices[0].message.content.strip().split("\n")
        )  # since we want a 'list' of responsibilities


    def get_missions(job_description: str) -> List[str]:
        prompt = missions_extraction_prompt_template.format(text=job_description)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            max_tokens=1024,
            temperature=0.0,
            seed=42,
        )
        return (
            response.choices[0].message.content.strip().split("\n")
        )  # since we want a 'list' of missions


    # def get_generated_title(job_description: str) -> str:
    #     prompt = title_generation_prompt_template.format(text=job_description)
    #     response = client.chat.completions.create(
    #         model=model,
    #         messages=[
    #             {
    #                 "role": "user",
    #                 "content": prompt,
    #             },
    #         ],
    #         max_tokens=1024,
    #         temperature=0.0,
    #         seed=42,
    #     )
    #     return response.choices[0].message.content.strip()

    # --------------------- #
    # --- Main Function --- #
    # --------------------- #

    def parse_job_description(job_description: str) -> Dict:
        summary = get_summary(job_description)
        title = get_title(job_description)
        company = get_company(job_description)
        location = get_location(job_description)
        technical_skills = get_technical_skills(job_description)
        soft_skills = get_soft_skills(job_description)
        qualifications = get_qualifications(job_description)
        responsibilities = get_responsibilities(job_description)
        missions = get_missions(job_description)
        # generated_title = get_generated_title(job_description)

        job_insights = JobDescription(
            Summary=summary,
            Title=title,
            Company=company,
            Location=location,
            Technical_Skills=technical_skills,
            Soft_Skills=soft_skills,
            Qualifications=qualifications,
            Responsibilities=responsibilities,
            Missions=missions,
            # Generated_Title=generated_title,
        )

        return job_insights.model_dump()


# ------------------- #
# --- Script Args --- #
# ------------------- #


def parse_args():
    parser = argparse.ArgumentParser(
        description="Extract job description insights using LLM."
    )
    parser.add_argument(
        "--job_description_path",
        type=str,
        default="data/job_descriptions/raw/test_DoggoTech_CTO.txt",  # for testing purposes
        help="Filename of the job description file located in the default folder 'data/job_description/raw'",
    )
    parser.add_argument(
        "--output_path",
        default="data/job_descriptions/structured",
        help="Path to the output folder",
    )

    return parser.parse_args()


# ------------ #
# --- Main --- #
# ------------ #


def main(
        input_file_path: str = "data/job_descriptions/raw/test_DoggoTech_CTO.txt",
        output_folder: str = "data/job_descriptions/structured",
) -> None:
    try:
        # Load Unstructured Job Description from TXT file
        job_description_unstructured = load_file_from_txt(input_file_path)

        # Generate Structured Job Description
        job_description_structured = parse_job_description(job_description_unstructured)
        rprint(json.dumps(job_description_structured, indent=2))

        # Save the job description
        save_to_json(job_description_structured, output_folder, file_type="Structured Job Description")

    except FileNotFoundError as e:
        logger.error(f"Oups:\n   {e}")
        sys.exit(1)


if __name__ == "__main__":
    args = parse_args()

    main(
        input_file_path=args.job_description_path,
        output_folder=args.output_path,
    )
