from ai_resume_analyzer.extractors.schemas import ResumeData
from ai_resume_analyzer.scoring.rules import (
    ACTION_VERBS,
    ATS_KEYWORDS,
    CATEGORY_WEIGHTS,
    KEYWORD_PATTERN,
    MAX_ATS_SCORE,
    QUANTIFIED_ACHIEVEMENT_PATTERN,
    SECTION_HEADINGS,
    SUMMARY_HEADINGS,
)
from ai_resume_analyzer.scoring.schemas import (
    ATSCategoryScore,
    ATSScore,
    ATSSectionScores,
)


class ResumeScoringService:
    def score_resume(self, data: ResumeData, parsed_text: str = "") -> ATSScore:
        category_scores = {
            "contact_information": self._score_contact_information(data),
            "professional_summary": self._score_professional_summary(parsed_text),
            "skills": self._score_skills(data),
            "education": self._score_education(data),
            "experience": self._score_experience(data),
            "projects": self._score_projects(data),
            "keywords": self._score_keywords(data, parsed_text),
            "action_verbs": self._score_action_verbs(data, parsed_text),
            "quantified_achievements": self._score_quantified_achievements(
                data,
                parsed_text,
            ),
            "formatting": self._score_formatting(parsed_text),
        }

        total_score = sum(score.score for score in category_scores.values())
        total_possible = sum(score.max_score for score in category_scores.values())
        overall_score = round((total_score / total_possible) * MAX_ATS_SCORE)
        overall_score = max(0, min(MAX_ATS_SCORE, overall_score))

        missing_sections = [
            category for category, score in category_scores.items() if score.score == 0
        ]
        strengths = [
            score.feedback
            for score in category_scores.values()
            if score.score == score.max_score
        ]
        weaknesses = [
            score.feedback
            for score in category_scores.values()
            if score.score < score.max_score
        ]

        return ATSScore(
            overall_score=overall_score,
            section_scores=ATSSectionScores(**category_scores),
            missing_sections=missing_sections,
            strengths=strengths,
            weaknesses=weaknesses,
        )

    def _score_contact_information(self, data: ResumeData) -> ATSCategoryScore:
        max_score = CATEGORY_WEIGHTS["contact_information"]
        score = 0
        missing_items: list[str] = []

        if data.email:
            score += 4
        else:
            missing_items.append("email address")

        if data.phone:
            score += 4
        else:
            missing_items.append("phone number")

        if data.name:
            score += 2
        else:
            missing_items.append("name")

        if not missing_items:
            feedback = "Contact information is complete."
        else:
            feedback = "Lost points because the resume is missing: "
            feedback += ", ".join(missing_items) + "."

        return self._category(score, max_score, feedback)

    def _score_professional_summary(self, parsed_text: str) -> ATSCategoryScore:
        max_score = CATEGORY_WEIGHTS["professional_summary"]
        if self._has_heading(parsed_text, SUMMARY_HEADINGS):
            return self._category(
                max_score,
                max_score,
                "Professional summary section is present.",
            )

        if self._word_count(parsed_text) >= 80:
            return self._category(
                5,
                max_score,
                "Lost points because no clear professional summary heading was found.",
            )

        return self._category(
            0,
            max_score,
            "Lost points because no professional summary was detected.",
        )

    def _score_skills(self, data: ResumeData) -> ATSCategoryScore:
        max_score = CATEGORY_WEIGHTS["skills"]
        skill_count = len(self._unique_values(data.skills))

        if skill_count >= 10:
            score = max_score
            feedback = "Skills section has strong breadth."
        elif skill_count >= 6:
            score = 12
            feedback = "Lost points because fewer than 10 skills were detected."
        elif skill_count >= 3:
            score = 8
            feedback = "Lost points because the skills section is limited."
        elif skill_count > 0:
            score = 4
            feedback = "Lost points because very few skills were detected."
        else:
            score = 0
            feedback = "Lost points because no skills were detected."

        return self._category(score, max_score, feedback)

    def _score_education(self, data: ResumeData) -> ATSCategoryScore:
        max_score = CATEGORY_WEIGHTS["education"]
        if data.education:
            return self._category(max_score, max_score, "Education section is present.")
        return self._category(
            0,
            max_score,
            "Lost points because no education section was detected.",
        )

    def _score_experience(self, data: ResumeData) -> ATSCategoryScore:
        max_score = CATEGORY_WEIGHTS["experience"]
        experience_count = len(data.experience)

        if experience_count >= 3:
            score = max_score
            feedback = "Experience section has multiple entries."
        elif experience_count == 2:
            score = 16
            feedback = "Lost points because only two experience entries were detected."
        elif experience_count == 1:
            score = 10
            feedback = "Lost points because only one experience entry was detected."
        else:
            score = 0
            feedback = "Lost points because no experience section was detected."

        return self._category(score, max_score, feedback)

    def _score_projects(self, data: ResumeData) -> ATSCategoryScore:
        max_score = CATEGORY_WEIGHTS["projects"]
        project_count = len(data.projects)

        if project_count >= 2:
            score = max_score
            feedback = "Projects section has enough supporting examples."
        elif project_count == 1:
            score = 10
            feedback = "Lost points because only one project was detected."
        else:
            score = 0
            feedback = "Lost points because no projects were detected."

        return self._category(score, max_score, feedback)

    def _score_keywords(
        self,
        data: ResumeData,
        parsed_text: str,
    ) -> ATSCategoryScore:
        max_score = CATEGORY_WEIGHTS["keywords"]
        keywords = self._extract_ats_keywords(self._combined_text(data, parsed_text))
        keyword_count = len(keywords)

        if keyword_count >= 10:
            score = max_score
            feedback = "Resume contains strong ATS keyword coverage."
        elif keyword_count >= 6:
            score = 8
            feedback = "Lost points because ATS keyword coverage could be broader."
        elif keyword_count >= 3:
            score = 5
            feedback = "Lost points because only a few ATS keywords were detected."
        elif keyword_count > 0:
            score = 2
            feedback = "Lost points because ATS keyword coverage is minimal."
        else:
            score = 0
            feedback = "Lost points because no recognizable ATS keywords were found."

        return self._category(score, max_score, feedback)

    def _score_action_verbs(
        self,
        data: ResumeData,
        parsed_text: str,
    ) -> ATSCategoryScore:
        max_score = CATEGORY_WEIGHTS["action_verbs"]
        action_verbs = self._extract_action_verbs(self._combined_text(data, parsed_text))
        verb_count = len(action_verbs)

        if verb_count >= 5:
            score = max_score
            feedback = "Resume uses strong action verbs."
        elif verb_count >= 3:
            score = 4
            feedback = "Lost points because more action verbs would strengthen impact."
        elif verb_count > 0:
            score = 2
            feedback = "Lost points because few action verbs were detected."
        else:
            score = 0
            feedback = "Lost points because no action verbs were detected."

        return self._category(score, max_score, feedback)

    def _score_quantified_achievements(
        self,
        data: ResumeData,
        parsed_text: str,
    ) -> ATSCategoryScore:
        max_score = CATEGORY_WEIGHTS["quantified_achievements"]
        quantified_count = len(
            QUANTIFIED_ACHIEVEMENT_PATTERN.findall(
                self._achievement_text(data, parsed_text)
            )
        )

        if quantified_count >= 3:
            score = max_score
            feedback = "Resume includes multiple quantified achievements."
        elif quantified_count > 0:
            score = 3
            feedback = "Lost points because more quantified achievements are needed."
        else:
            score = 0
            feedback = "Lost points because no quantified achievements were detected."

        return self._category(score, max_score, feedback)

    def _score_formatting(self, parsed_text: str) -> ATSCategoryScore:
        max_score = CATEGORY_WEIGHTS["formatting"]
        if not parsed_text.strip():
            return self._category(
                0,
                max_score,
                "Lost points because resume text could not be evaluated.",
            )

        score = 0
        feedback_items: list[str] = []
        lines = [line.strip() for line in parsed_text.splitlines() if line.strip()]
        heading_count = sum(
            1 for line in lines if self._normalize_heading(line) in SECTION_HEADINGS
        )
        bullet_count = sum(1 for line in lines if line.startswith(("-", "*", "•")))
        long_line_count = sum(1 for line in lines if len(line) > 140)

        if len(lines) >= 5:
            score += 2
        else:
            feedback_items.append("too few readable lines")

        if heading_count >= 4:
            score += 4
        elif heading_count >= 2:
            score += 2
            feedback_items.append("some standard section headings are missing")
        else:
            feedback_items.append("standard section headings are missing")

        if bullet_count >= 3:
            score += 2
        else:
            feedback_items.append("few bullet-style entries were detected")

        if long_line_count == 0:
            score += 2
        else:
            feedback_items.append("some lines are too long for ATS-friendly parsing")

        if not feedback_items:
            feedback = "Formatting appears ATS-friendly."
        else:
            feedback = "Lost points because " + ", ".join(feedback_items) + "."

        return self._category(score, max_score, feedback)

    def _category(
        self,
        score: int,
        max_score: int,
        feedback: str,
    ) -> ATSCategoryScore:
        return ATSCategoryScore(
            score=max(0, min(max_score, score)),
            max_score=max_score,
            feedback=feedback,
        )

    def _combined_text(self, data: ResumeData, parsed_text: str) -> str:
        values = [
            parsed_text,
            data.name or "",
            data.email or "",
            data.phone or "",
            *data.skills,
            *data.education,
            *data.experience,
            *data.projects,
        ]
        return " ".join(value for value in values if value)

    def _achievement_text(self, data: ResumeData, parsed_text: str) -> str:
        achievement_values = [*data.experience, *data.projects]
        if achievement_values:
            return " ".join(achievement_values)
        return parsed_text

    def _extract_ats_keywords(self, text: str) -> set[str]:
        tokens = {token.strip(".-").lower() for token in KEYWORD_PATTERN.findall(text)}
        return {token for token in tokens if token in ATS_KEYWORDS}

    def _extract_action_verbs(self, text: str) -> set[str]:
        tokens = {token.strip(".-").lower() for token in KEYWORD_PATTERN.findall(text)}
        return {token for token in tokens if token in ACTION_VERBS}

    def _has_heading(self, text: str, headings: set[str]) -> bool:
        return any(
            self._normalize_heading(line) in headings for line in text.splitlines()
        )

    def _normalize_heading(self, line: str) -> str:
        normalized = line.strip().strip(":").lower()
        normalized = normalized.strip("-*• ")
        return " ".join(normalized.split())

    def _unique_values(self, values: list[str]) -> set[str]:
        return {value.casefold() for value in values if value.strip()}

    def _word_count(self, text: str) -> int:
        return len(KEYWORD_PATTERN.findall(text))
