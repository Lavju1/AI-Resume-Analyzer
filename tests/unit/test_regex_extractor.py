from ai_resume_analyzer.extractors.regex_extractor import RegexResumeExtractor


def test_multi_word_skills_are_extracted_as_single_skills() -> None:
    extractor = RegexResumeExtractor()

    resume_data = extractor.extract("""
        Skills:
        Web Development Machine Learning Data Science Artificial Intelligence
        """)

    assert resume_data.skills == [
        "Web Development",
        "Machine Learning",
        "Data Science",
        "Artificial Intelligence",
    ]
