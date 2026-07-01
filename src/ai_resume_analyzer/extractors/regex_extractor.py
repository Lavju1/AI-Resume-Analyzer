import re

from ai_resume_analyzer.extractors.base import BaseResumeExtractor
from ai_resume_analyzer.extractors.schemas import ResumeData

EMAIL_PATTERN = re.compile(
    r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
    re.IGNORECASE,
)
PHONE_PATTERN = re.compile(
    r"(?<!\w)(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{2,4}\)?[\s.-]?)?"
    r"\d{3,4}[\s.-]?\d{3,4}(?!\w)"
)
SECTION_ALIASES = {
    "skills": {
        "skills",
        "technical skills",
        "core skills",
        "key skills",
    },
    "education": {
        "education",
        "academic background",
        "educational background",
    },
    "experience": {
        "experience",
        "work experience",
        "professional experience",
        "employment experience",
    },
    "projects": {
        "projects",
        "project experience",
        "personal projects",
    },
}
SKILL_SEPARATORS = re.compile(r"[,;|]|(?:\s+[•]\s+)")
LEADING_BULLET_PATTERN = re.compile(r"^[\s\-*•]+")


MULTI_WORD_SKILLS = {
    "artificial intelligence": "Artificial Intelligence",
    "data science": "Data Science",
    "machine learning": "Machine Learning",
    "web development": "Web Development",
}
MULTI_WORD_SKILL_PATTERN = re.compile(
    r"\b("
    + "|".join(
        re.escape(skill)
        for skill in sorted(MULTI_WORD_SKILLS, key=len, reverse=True)
    )
    + r")\b",
    re.IGNORECASE,
)


class RegexResumeExtractor(BaseResumeExtractor):
    def extract(self, text: str) -> ResumeData:
        sections = self._extract_sections(text)

        return ResumeData(
            name=None,
            email=self._extract_email(text),
            phone=self._extract_phone(text),
            skills=sections["skills"],
            education=sections["education"],
            experience=sections["experience"],
            projects=sections["projects"],
        )

    def _extract_email(self, text: str) -> str | None:
        match = EMAIL_PATTERN.search(text)
        if match is None:
            return None
        return match.group(0)

    def _extract_phone(self, text: str) -> str | None:
        for match in PHONE_PATTERN.finditer(text):
            phone = match.group(0).strip()
            digit_count = sum(character.isdigit() for character in phone)
            if digit_count >= 7:
                return phone
        return None

    def _extract_sections(self, text: str) -> dict[str, list[str]]:
        sections: dict[str, list[str]] = {
            "skills": [],
            "education": [],
            "experience": [],
            "projects": [],
        }
        current_section: str | None = None

        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line:
                continue

            header, inline_value = self._parse_header_line(line)
            if header is not None:
                current_section = header
                if inline_value:
                    sections[header].extend(
                        self._split_section_values(inline_value, header)
                    )
                continue

            if current_section is not None:
                sections[current_section].extend(
                    self._split_section_values(line, current_section)
                )

        return {
            section: self._dedupe_values(values) for section, values in sections.items()
        }

    def _parse_header_line(self, line: str) -> tuple[str | None, str]:
        before_colon, separator, after_colon = line.partition(":")
        if separator:
            header = self._section_key(before_colon)
            if header is not None:
                return header, after_colon.strip()

        header = self._section_key(line)
        if header is not None:
            return header, ""

        return None, ""

    def _section_key(self, value: str) -> str | None:
        normalized = self._normalize_header(value)
        for section, aliases in SECTION_ALIASES.items():
            if normalized in aliases:
                return section
        return None

    def _normalize_header(self, value: str) -> str:
        normalized = LEADING_BULLET_PATTERN.sub("", value).strip().lower()
        normalized = re.sub(r"[^a-z0-9&/ ]+", "", normalized)
        return re.sub(r"\s+", " ", normalized).strip()

    def _split_section_values(self, value: str, section: str) -> list[str]:
        stripped_value = LEADING_BULLET_PATTERN.sub("", value).strip()
        if not stripped_value:
            return []

        if section == "skills":
            skills: list[str] = []
            for item in SKILL_SEPARATORS.split(stripped_value):
                skills.extend(self._split_skill_value(item))
            return skills

        return [stripped_value]

    def _split_skill_value(self, value: str) -> list[str]:
        stripped_value = value.strip()
        if not stripped_value:
            return []

        normalized_value = re.sub(r"\s+", " ", stripped_value.lower()).strip()
        if normalized_value in MULTI_WORD_SKILLS:
            return [MULTI_WORD_SKILLS[normalized_value]]

        matches = [
            MULTI_WORD_SKILLS[match.group(0).lower()]
            for match in MULTI_WORD_SKILL_PATTERN.finditer(stripped_value)
        ]
        if not matches:
            return [stripped_value]

        remaining_text = MULTI_WORD_SKILL_PATTERN.sub(" ", stripped_value)
        remaining_text = re.sub(
            r"\b(?:and|or)\b",
            " ",
            remaining_text,
            flags=re.IGNORECASE,
        )
        if not remaining_text.strip():
            return matches

        return [stripped_value]

    def _dedupe_values(self, values: list[str]) -> list[str]:
        deduped_values: list[str] = []
        seen_values: set[str] = set()

        for value in values:
            key = value.casefold()
            if key in seen_values:
                continue
            seen_values.add(key)
            deduped_values.append(value)

        return deduped_values
