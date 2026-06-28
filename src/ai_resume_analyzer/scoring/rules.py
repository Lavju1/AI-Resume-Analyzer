from collections.abc import Callable
from dataclasses import dataclass

from ai_resume_analyzer.extractors.schemas import ResumeData

RULE_POINTS = 20
MAX_ATS_SCORE = 100


@dataclass(frozen=True)
class ATSRule:
    section: str
    is_satisfied: Callable[[ResumeData], bool]
    strength: str
    weakness: str


def has_contact(data: ResumeData) -> bool:
    return bool(data.email or data.phone)


def has_skills(data: ResumeData) -> bool:
    return bool(data.skills)


def has_education(data: ResumeData) -> bool:
    return bool(data.education)


def has_experience(data: ResumeData) -> bool:
    return bool(data.experience)


def has_projects(data: ResumeData) -> bool:
    return bool(data.projects)


ATS_RULES = (
    ATSRule(
        section="contact",
        is_satisfied=has_contact,
        strength="Contact information is present.",
        weakness="Missing contact information.",
    ),
    ATSRule(
        section="skills",
        is_satisfied=has_skills,
        strength="Skills section is present.",
        weakness="Missing skills section.",
    ),
    ATSRule(
        section="education",
        is_satisfied=has_education,
        strength="Education section is present.",
        weakness="Missing education section.",
    ),
    ATSRule(
        section="experience",
        is_satisfied=has_experience,
        strength="Experience section is present.",
        weakness="Missing experience section.",
    ),
    ATSRule(
        section="projects",
        is_satisfied=has_projects,
        strength="Projects section is present.",
        weakness="Missing projects section.",
    ),
)
