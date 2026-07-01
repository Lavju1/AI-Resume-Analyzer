from ai_resume_analyzer.extractors.schemas import ResumeData
from ai_resume_analyzer.scoring.service import ResumeScoringService


def test_weighted_score_penalizes_missing_quantified_achievements() -> None:
    service = ResumeScoringService()
    resume_data = ResumeData(
        name="Ada Lovelace",
        email="ada@example.com",
        phone="555-123-4567",
        skills=[
            "Python",
            "FastAPI",
            "SQL",
            "PostgreSQL",
            "Docker",
            "React",
            "TypeScript",
            "AWS",
            "REST",
            "Git",
        ],
        education=["BS Computer Science"],
        experience=[
            "Built backend APIs",
            "Designed database models",
            "Collaborated with frontend teams",
        ],
        projects=[
            "Created resume analyzer using FastAPI and React",
            "Implemented Docker deployment pipeline",
        ],
    )
    parsed_text = """
    Professional Summary
    Backend engineer focused on API design and database-backed applications.

    Skills
    Python, FastAPI, SQL, PostgreSQL, Docker, React, TypeScript, AWS, REST, Git

    Education
    BS Computer Science

    Experience
    - Built backend APIs
    - Designed database models
    - Collaborated with frontend teams

    Projects
    - Created resume analyzer using FastAPI and React
    - Implemented Docker deployment pipeline
    """

    score = service.score_resume(resume_data, parsed_text=parsed_text)

    assert score.overall_score < 100
    assert score.section_scores.quantified_achievements.score == 0
    assert (
        "quantified achievements"
        in score.section_scores.quantified_achievements.feedback
    )
    assert "quantified_achievements" in score.missing_sections


def test_weighted_score_returns_detailed_partial_feedback() -> None:
    service = ResumeScoringService()
    resume_data = ResumeData(
        email="candidate@example.com",
        skills=["Python", "SQL"],
        education=[],
        experience=["Worked on backend tasks"],
        projects=[],
    )

    score = service.score_resume(resume_data, parsed_text="Skills\nPython, SQL")

    assert score.overall_score < 50
    assert score.section_scores.contact_information.score == 4
    assert score.section_scores.skills.score == 4
    assert score.section_scores.experience.score == 10
    assert score.section_scores.projects.score == 0
    assert score.section_scores.education.score == 0
    assert score.weaknesses
