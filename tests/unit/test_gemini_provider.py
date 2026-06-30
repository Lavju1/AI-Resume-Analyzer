from ai_resume_analyzer.ai.gemini_provider import GeminiProvider


def test_parse_response_text_splits_markdown_sections() -> None:
    provider = GeminiProvider(api_key="test-key", model="test-model")

    analysis = provider._parse_response_text(
        """
        ### **Professional Summary**
        Experienced backend engineer with FastAPI experience.

        ---

        ### Top Strengths
        - **FastAPI and SQLAlchemy experience**
        - Clear project work

        ### Weaknesses
        * Missing quantified impact

        ### Resume Improvement Recommendations
        1. Add metrics to experience bullets
        2. Tailor keywords for each role
        """
    )

    assert analysis.summary == "Experienced backend engineer with FastAPI experience."
    assert analysis.strengths == [
        "FastAPI and SQLAlchemy experience",
        "Clear project work",
    ]
    assert analysis.weaknesses == ["Missing quantified impact"]
    assert analysis.recommendations == [
        "Add metrics to experience bullets",
        "Tailor keywords for each role",
    ]


def test_parse_response_text_supports_alternate_headings() -> None:
    provider = GeminiProvider(api_key="test-key", model="test-model")

    analysis = provider._parse_response_text(
        """
        **Summary**
        Strong technical foundation.

        **Strengths**
        - Python

        **Recommendations**
        - Add more project detail
        """
    )

    assert analysis.summary == "Strong technical foundation."
    assert analysis.strengths == ["Python"]
    assert analysis.weaknesses == []
    assert analysis.recommendations == ["Add more project detail"]


def test_parse_response_text_uses_empty_lists_for_missing_sections() -> None:
    provider = GeminiProvider(api_key="test-key", model="test-model")

    analysis = provider._parse_response_text(
        """
        Summary: Solid resume for an entry-level role.
        """
    )

    assert analysis.summary == "Solid resume for an entry-level role."
    assert analysis.strengths == []
    assert analysis.weaknesses == []
    assert analysis.recommendations == []
