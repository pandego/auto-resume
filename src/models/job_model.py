from typing import List

from pydantic import BaseModel, Field


class JobDescription(BaseModel):
    Summary: str = Field(
        ...,
        description="A concise summary of the job description, focusing on the core responsibilities, mission, and requirements.",
    )
    Title: str = Field(
        ..., description="The title of the job exactly as provided on the description."
    )
    Company: str = Field(
        ...,
        description="The company name of the job exactly as provided on the description.",
    )
    Location: str = Field(
        ...,
        description="The location of the job exactly as provided on the description.",
    )
    Technical_Skills: List[str] = Field(
        ...,
        description="A list of key technical skills required for the job, extracted from the description.",
    )
    Soft_Skills: List[str] = Field(
        ...,
        description="A list of key soft skills required for the job, extracted from the description.",
    )
    Qualifications: List[str] = Field(
        ...,
        description="A list of key qualifications for the job, extracted from the description.",
    )
    Responsibilities: List[str] = Field(
        ...,
        description="A list of key responsibilities for the role, outlining the main tasks and duties expected from the job holder.",
    )
    Missions: List[str] = Field(
        ...,
        description="A list of key missions or objectives of the job, listing the main objectives of the role.",
    )
    # Generated_Title: str = Field(
    #     ...,
    #     description="A generated job title based on the job description, in case the provided title doesn't match the responsibilities or content.",
    # )
