import re
from collections.abc import Iterable

from ai_resume_analyzer.extractors.schemas import ResumeData
from ai_resume_analyzer.job_matching.base import BaseJobMatcher
from ai_resume_analyzer.job_matching.schemas import (
    JobDescription,
    JobMatchResult,
)

KEYWORD_PATTERN = re.compile(r"[a-z0-9][a-z0-9+#.\-]*")
SKILL_RELATIONSHIPS = {
    "web development": {
        "backend",
        "back end",
        "css",
        "express",
        "frontend",
        "front end",
        "full stack",
        "html",
        "javascript",
        "mern",
        "node",
        "node.js",
        "react",
        "tailwind",
        "web development",
    },
    "data science": {
        "analytics",
        "artificial intelligence",
        "data science",
        "machine learning",
        "numpy",
        "pandas",
        "python",
        "scikit learn",
        "scikit-learn",
        "sql",
    },
}
TECHNICAL_SKILLS = {
    "api",
    "aws",
    "azure",
    "css",
    "docker",
    "express",
    "fastapi",
    "frontend",
    "git",
    "html",
    "javascript",
    "machine learning",
    "node",
    "node.js",
    "numpy",
    "pandas",
    "python",
    "react",
    "scikit learn",
    "scikit-learn",
    "sql",
    "tailwind",
    "typescript",
}
RELATED_MATCH_THRESHOLD = 0.25
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
        required_skills = self._extract_skill_requirements(job_description.text)
        resume_keywords = self._extract_resume_keywords(resume_data)
        resume_skill_terms = self._extract_resume_skill_terms(resume_data)
        skill_scores = {
            skill: self._skill_match_score(skill, resume_skill_terms)
            for skill in required_skills
        }

        matched_skills = [
            skill
            for skill, score in skill_scores.items()
            if score >= RELATED_MATCH_THRESHOLD
        ]
        missing_skills = [
            skill
            for skill, score in skill_scores.items()
            if score < RELATED_MATCH_THRESHOLD
        ]
        matched_keywords = [
            keyword for keyword in job_keywords if keyword in resume_keywords
        ]
        missing_keywords = [
            keyword for keyword in job_keywords if keyword not in resume_keywords
        ]

        return JobMatchResult(
            overall_match=self._calculate_overall_match(
                skill_scores=list(skill_scores.values()),
                matched_keywords=matched_keywords,
                required_keywords=job_keywords,
            ),
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            matched_keywords=matched_keywords,
            missing_keywords=missing_keywords,
        )

    def _extract_keywords(self, text: str) -> list[str]:
        keywords: list[str] = []
        seen_keywords: set[str] = set()
        normalized_text = self._normalize_text(text)

        for skill in self._known_skill_terms():
            if " " not in skill:
                continue
            if not self._contains_term(normalized_text, skill):
                continue
            seen_keywords.add(skill)
            keywords.append(skill)

        for keyword in KEYWORD_PATTERN.findall(normalized_text):
            normalized_keyword = self._normalize_term(keyword)
            if not self._is_keyword(normalized_keyword):
                continue
            if normalized_keyword in seen_keywords:
                continue

            seen_keywords.add(normalized_keyword)
            keywords.append(normalized_keyword)

        return keywords

    def _extract_skill_requirements(self, text: str) -> list[str]:
        required_skills: list[str] = []
        seen_skills: set[str] = set()
        normalized_text = self._normalize_text(text)

        for skill in self._known_skill_terms():
            if not self._contains_term(normalized_text, skill):
                continue
            if skill in seen_skills:
                continue

            seen_skills.add(skill)
            required_skills.append(skill)

        return required_skills

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

    def _extract_resume_skill_terms(self, resume_data: ResumeData) -> set[str]:
        skill_terms: set[str] = set()
        normalized_skill_text = self._normalize_text(" ".join(resume_data.skills))

        for skill in self._known_skill_terms():
            if self._contains_term(normalized_skill_text, skill):
                skill_terms.add(skill)

        for skill in resume_data.skills:
            skill_terms.add(self._normalize_term(skill))
            skill_terms.update(self._extract_keywords(skill))

        return {skill for skill in skill_terms if skill}

    def _is_keyword(self, keyword: str) -> bool:
        return len(keyword) > 1 and keyword not in STOP_WORDS

    def _present(self, values: Iterable[str | None]) -> list[str]:
        return [value for value in values if value]

    def _skill_match_score(self, required_skill: str, resume_skills: set[str]) -> float:
        if required_skill in resume_skills:
            return 1.0

        related_skills = SKILL_RELATIONSHIPS.get(required_skill)
        if related_skills is not None:
            normalized_related_skills = {
                self._normalize_term(skill)
                for skill in related_skills
                if self._normalize_term(skill) != required_skill
            }
            related_matches = normalized_related_skills.intersection(resume_skills)
            if related_matches:
                return min(1.0, len(related_matches) / 4)

        for parent_skill, related_skills in SKILL_RELATIONSHIPS.items():
            normalized_related_skills = {
                self._normalize_term(skill) for skill in related_skills
            }
            if (
                required_skill in normalized_related_skills
                and parent_skill in resume_skills
            ):
                return 0.75

        return 0.0

    def _calculate_overall_match(
        self,
        *,
        skill_scores: list[float],
        matched_keywords: list[str],
        required_keywords: list[str],
    ) -> float:
        if skill_scores:
            score = (sum(skill_scores) / len(skill_scores)) * 100
            return max(0.0, min(100.0, round(score, 2)))

        if not required_keywords:
            return 0.0

        score = (len(matched_keywords) / len(required_keywords)) * 100
        return max(0.0, min(100.0, round(score, 2)))

    def _known_skill_terms(self) -> list[str]:
        skill_terms = set(TECHNICAL_SKILLS)
        for parent_skill, related_skills in SKILL_RELATIONSHIPS.items():
            skill_terms.add(parent_skill)
            skill_terms.update(related_skills)

        return sorted(
            {self._normalize_term(skill) for skill in skill_terms},
            key=lambda skill: (-len(skill), skill),
        )

    def _contains_term(self, normalized_text: str, term: str) -> bool:
        return f" {term} " in f" {normalized_text} "

    def _normalize_text(self, text: str) -> str:
        normalized = re.sub(r"[^a-z0-9+#]+", " ", text.lower())
        return f" {' '.join(normalized.split())} "

    def _normalize_term(self, value: str) -> str:
        normalized = re.sub(r"[^a-z0-9+#]+", " ", value.lower())
        return " ".join(normalized.split())
