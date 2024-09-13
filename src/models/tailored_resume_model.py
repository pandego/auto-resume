from typing import List, Optional, Dict

from pydantic import BaseModel, Field  # , EmailStr  # , HttpUrl, constr


# ---------------------------- #
# --- Tailored Resume Data --- #
# ---------------------------- #


# --- Contact Information --- #
class ContactInfo(BaseModel):
    name: str = Field(..., description="Full name of the individual")
    phone: str = Field(..., description="Contact phone number")
    city_country: str = Field(..., description="City and country of residence")
    email: str = Field(..., description="Email address")
    linkedin: str = Field(..., description="LinkedIn profile URL")
    github: str = Field(..., description="GitHub profile URL")
    medium: str = Field(..., description="Medium profile URL")
    twitter: Optional[str] = Field(None, description="Twitter profile URL")
    homepage: Optional[str] = Field(None, description="Personal website URL")
    role: str = Field(..., description="Current job title or professional role")


# --- Skills & Languages --- #
class Skills(BaseModel):
    programming_languages: List[str] = Field(..., description="List of programming languages")
    technical_stack: List[str] = Field(..., description="List of technical tools, frameworks, etc.")
    soft_skills: List[str] = Field(..., description="List of soft skills (e.g., leadership, communication)")


# --- Experience --- #
class ExperienceItem(BaseModel):
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Employer or company name")
    period: str = Field(..., description="Time period of employment (e.g., 'Jan 2015 - Dec 2020')")
    # missions: List[str] = Field(default_factory=list, description="List of responsibilities or tasks in this role")
    # results: List[str] = Field(default_factory=list, description="List of key achievements and outcomes")
    summary: List[str] = Field(..., description="A summary list, combining key tasks, responsibilities, achievements, and impact into concise points tailored to the job description, limiting the summary to 2-3 bullet points.")

# --- Education --- #
class EducationItem(BaseModel):
    degree: str = Field(..., description="Degree title (e.g., 'Master's degree in AI')")
    institution: str = Field(..., description="Name of school or university")
    period: str = Field(..., description="Time period of study (e.g., '2015 - 2020')")
    grade: Optional[str] = Field(None, description="Grade or Honors, if applicable")
    # description: Optional[str] = Field(None, description="Description of the program or coursework")


# --- Certifications --- #
class CertificationItem(BaseModel):
    title: str = Field(..., description="Certification title (e.g., 'AWS Certified')")
    institution: str = Field(..., description="Provider or issuing institution (e.g., 'Amazon')")
    year: int = Field(..., description="Year the certification was obtained")


# --- Tailored Resume Data --- #
class TailoredResumeData(BaseModel):
    # contact_info: ContactInfo = Field(..., description="Contact details")
    contact_info: Dict[str, str] = Field(..., description="Contact details")
    introduction: str = Field(..., description="Professional summary or career objective")
    skills: Skills = Field(..., description="Skills section")
    languages: List[Dict[str, int]] = Field(..., description="List of spoken languages with proficiency levels")
    experiences: List[ExperienceItem] = Field(..., description="List of work experiences")
    education: List[EducationItem] = Field(..., description="List of education entries")
    certifications: List[CertificationItem] = Field(..., description="Optional list of certifications")
    interests: List[str] = Field(...,
                                 description="List of interests or hobbies (e.g., 'Weightlifting, Photography, VR gaming')")
    company_applying: str = Field(..., description="Company name for which the resume is tailored")

class TailoredResume(BaseModel):
    # --- Introduction --- #
    introduction: Optional[str] = Field(None, description="Optional brief professional summary or career objective")

    # --- Skills --- #
    programming_languages: List[str] = Field(..., description="List of programming languages")
    technical_stack: List[str] = Field(..., description="List of technical tools, frameworks, etc.")
    soft_skills: List[str] = Field(..., description="List of soft skills (e.g., leadership, communication)")

    # --- Experience --- #
    job_title: str = Field(..., description="Job title")
    company: str = Field(..., description="Employer or company name")
    period: str = Field(..., description="Time period of employment (e.g., 'Jan 2015 - Dec 2020')")
    missions: List[str] = Field(..., description="List of responsibilities or tasks in this role")
    results: List[str] = Field(..., description="List of key achievements and outcomes")

    # --- Certifications --- #
    certification_title: str = Field(..., description="Certification title (e.g., 'AWS Certified')")
    where: str = Field(..., description="Provider or issuing institution (e.g., 'Amazon')")
    year: int = Field(..., description="Year the certification was obtained")

    # --- Interests --- #
    interests: Optional[List[str]] = Field(
        None,
        description="Optional list of interests or hobbies (e.g., 'Weightlifting, Photography, VR gaming')",
    )
