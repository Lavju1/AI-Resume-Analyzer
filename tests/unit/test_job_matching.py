from ai_resume_analyzer.extractors.schemas import ResumeData
from ai_resume_analyzer.job_matching.matcher import RuleBasedJobMatcher
from ai_resume_analyzer.job_matching.schemas import JobDescription


def test_web_development_requirement_matches_related_resume_skill() -> None:
    matcher = RuleBasedJobMatcher()
    resume_data = ResumeData(
        skills=["React"],
    )

    result = matcher.match(
        resume_data=resume_data,
        job_description=JobDescription(
            text="We need Web Development experience for a frontend role.",
        ),
    )

    assert result.overall_match > 0
    assert "web development" in result.matched_skills
    assert "web development" not in result.missing_skills


def test_data_science_requirement_matches_related_resume_skill() -> None:
    matcher = RuleBasedJobMatcher()
    resume_data = ResumeData(
        skills=["Python"],
    )

    result = matcher.match(
        resume_data=resume_data,
        job_description=JobDescription(
            text="Looking for Data Science experience and analytics ability.",
        ),
    )

    assert result.overall_match > 0
    assert "data science" in result.matched_skills
    assert "data science" not in result.missing_skills
