from ai_resume_analyzer.extractors.schemas import ResumeData
from ai_resume_analyzer.scoring.rules import ATS_RULES, MAX_ATS_SCORE, RULE_POINTS
from ai_resume_analyzer.scoring.schemas import ATSScore, ATSSectionScores


class ResumeScoringService:
    def score_resume(self, data: ResumeData) -> ATSScore:
        section_scores: dict[str, int] = {}
        missing_sections: list[str] = []
        strengths: list[str] = []
        weaknesses: list[str] = []

        for rule in ATS_RULES:
            if rule.is_satisfied(data):
                section_scores[rule.section] = RULE_POINTS
                strengths.append(rule.strength)
                continue

            section_scores[rule.section] = 0
            missing_sections.append(rule.section)
            weaknesses.append(rule.weakness)

        overall_score = min(sum(section_scores.values()), MAX_ATS_SCORE)

        return ATSScore(
            overall_score=overall_score,
            section_scores=ATSSectionScores(**section_scores),
            missing_sections=missing_sections,
            strengths=strengths,
            weaknesses=weaknesses,
        )
