from typing import Dict, List

from models.tailored_resume_model import ContactInfo, EducationItem


# --------------------------------- #
# --- Deterministic Resume Data --- #
# --------------------------------- #


def extract_contact_info(resume_data: Dict) -> Dict:
    """
    Extracts contact information from the structured resume data.

    Parameters
    ----------
    resume_data : Dict
        A dictionary containing the resume data.

    Returns
    -------
    ContactInfo
        An instance of ContactInfo containing the extracted contact information.
    """
    contact_info = resume_data.get("contact_info", {})

    return dict(ContactInfo(
        name=contact_info.get("name", ""),
        phone=contact_info.get("phone", ""),
        city_country=contact_info.get("city_country", ""),
        email=contact_info.get("email", ""),
        linkedin=contact_info.get("linkedin", ""),
        github=contact_info.get("github", ""),
        medium=contact_info.get("medium", ""),
        twitter=contact_info.get("twitter", None),  # Optional field
        homepage=contact_info.get("homepage", None),  # Optional field
        role=contact_info.get("role", [""])[0]  # Take the first role if there are multiple
    ))


def extract_languages(resume_data: Dict) -> List[Dict[str, int]]:
    """
    Extracts language information from the structured resume data.

    Parameters
    ----------
    resume_data : Dict
        A dictionary containing the resume data.

    Returns
    -------
    List[Dict[str, int]]
        A list of languages extracted from the resume data.

    Notes
    -----
    This function assumes that the 'languages' key exists in the resume_data dictionary
    and contains a list of spoken languages with proficiency levels.

    """
    languages = resume_data.get("languages", [])

    return languages


def extract_education(resume_data: Dict) -> List[dict]:
    """
    Extracts education information from the structured resume data.

    Parameters
    ----------
    resume_data : Dict
        A dictionary containing the resume data.

    Returns
    -------
    List[EducationItem]
        A list of EducationItem instances containing the extracted education information.

    Notes
    -----
    This function assumes that the 'education' key exists in the resume_data dictionary
    and contains all the necessary fields for the EducationItem model.
    """
    education_data = resume_data.get("education", [])

    # Convert the period from array to formatted string (e.g., [2010, 2014] -> "2010 - 2014")
    education_items = []
    for edu in education_data:
        period_str = f"{edu['period'][0]} - {edu['period'][1]}" if "period" in edu else "Unknown"

        # Create an instance of EducationItem and append to the list
        education_items.append(dict(
            EducationItem(
                degree=edu.get("degree", "Unknown"),
                institution=edu.get("institution", "Unknown"),
                period=period_str,
                grade=edu.get("grade"),
                # description=edu.get("description")
            ))
        )

    return education_items
