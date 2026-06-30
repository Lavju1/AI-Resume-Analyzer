import re
from collections.abc import Iterable

from ai_resume_analyzer.extractors.schemas import ResumeData
from ai_resume_analyzer.job_matching.base import BaseJobMatcher
from ai_resume_analyzer.job_matching.schemas import (
    JobDescription,
    JobMatchResult,
)

KEYWORD_PATTERN = re.compile(r"[a-z0-9][a-z0-9+#.\-]*")
STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "our",
    "the",
    "to",
    "with",
    "you",
    "your",
    "ability",
    "about",
    "across",
    "all",
    "also",
    "build",
    "candidate",
    "collaborate",
    "communication",
    "company",
    "develop",
    "development",
    "excellent",
    "experience",
    "familiar",
    "help",
    "including",
    "join",
    "knowledge",
    "looking",
    "manage",
    "must",
    "preferred",
    "required",
    "requirements",
    "responsibilities",
    "role",
    "strong",
    "team",
    "using",
    "work",
    "years",
}


class RuleBasedJobMatcher(BaseJobMatcher):
    def match(
        self,
        *,
        resume_data: ResumeData,
        job_description: JobDescription,
    ) -> JobMatchResult:
        job_keywords = self._extract_keywords(job_description.text)
        resume_keywords = self._extract_resume_keywords(resume_data)
        resume_skill_keywords = self._extract_resume_skill_keywords(resume_data)

        matched_skills = [
            keyword for keyword in job_keywords if keyword in resume_skill_keywords
        ]
        missing_skills = [
            keyword for keyword in job_keywords if keyword not in resume_skill_keywords
        ]
        matched_keywords = [
            keyword for keyword in job_keywords if keyword in resume_keywords
        ]
        missing_keywords = [
            keyword for keyword in job_keywords if keyword not in resume_keywords
        ]

        return JobMatchResult(
            overall_match=self._calculate_overall_match(
                matched_skills=matched_skills,
                required_skills=job_keywords,
            ),
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            matched_keywords=matched_keywords,
            missing_keywords=missing_keywords,
        )

    def _extract_keywords(self, text: str) -> list[str]:
        keywords: list[str] = []
        seen_keywords: set[str] = set()

        for keyword in KEYWORD_PATTERN.findall(text.lower()):
            normalized_keyword = keyword.strip(".-")
            if not self._is_keyword(normalized_keyword):
                continue
            if normalized_keyword in seen_keywords:
                continue

            seen_keywords.add(normalized_keyword)
            keywords.append(normalized_keyword)

        return keywords

    def _extract_resume_keywords(self, resume_data: ResumeData) -> set[str]:
        resume_sections = [
            resume_data.name,
            resume_data.email,
            resume_data.phone,
            *resume_data.skills,
            *resume_data.education,
            *resume_data.experience,
            *resume_data.projects,
        ]
        return set(self._extract_keywords(" ".join(self._present(resume_sections))))

    def _extract_resume_skill_keywords(self, resume_data: ResumeData) -> set[str]:
        return set(self._extract_keywords(" ".join(resume_data.skills)))

    def _is_keyword(self, keyword: str) -> bool:
        return len(keyword) > 1 and keyword not in STOP_WORDS

    def _present(self, values: Iterable[str | None]) -> list[str]:
        return [value for value in values if value]

    def _calculate_overall_match(
        self,
        *,
        matched_skills: list[str],
        required_skills: list[str],
    ) -> float:
        if not required_skills:
            return 0.0

        score = (len(matched_skills) / len(required_skills)) * 100
        return max(0.0, min(100.0, round(score, 2)))
