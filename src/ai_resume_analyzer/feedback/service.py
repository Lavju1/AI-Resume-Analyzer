from ai_resume_analyzer.extractors.schemas import ResumeData
from ai_resume_analyzer.feedback.schemas import FeedbackItem, ResumeFeedback
from ai_resume_analyzer.scoring.schemas import ATSScore

HIGH_ATS_SCORE_THRESHOLD = 80


class ResumeFeedbackService:
    def generate_feedback(
        self,
        extracted_data: ResumeData,
        ats_score: ATSScore,
    ) -> ResumeFeedback:
        feedback: list[FeedbackItem] = []

        if extracted_data.email is None:
            feedback.append(
                FeedbackItem(
                    category="contact",
                    severity="warning",
                    title="Add an email address.",
                    message=(
                        "Include a professional email address so recruiters can "
                        "contact you."
                    ),
                )
            )

        if not extracted_data.projects:
            feedback.append(
                FeedbackItem(
                    category="projects",
                    severity="warning",
                    title="Include 1-2 personal or academic projects.",
                    message=(
                        "Projects help demonstrate applied skills when experience "
                        "is limited."
                    ),
                )
            )

        if len(extracted_data.skills) > 10:
            feedback.append(
                FeedbackItem(
                    category="skills",
                    severity="success",
                    title="Good technical breadth.",
                    message="Your resume lists a broad set of skills for ATS matching.",
                )
            )

        if not extracted_data.experience:
            feedback.append(
                FeedbackItem(
                    category="experience",
                    severity="warning",
                    title="Add internships, freelance work, or academic experience.",
                    message=(
                        "Experience entries help show how you have used your skills "
                        "in practice."
                    ),
                )
            )

        if ats_score.overall_score >= HIGH_ATS_SCORE_THRESHOLD:
            feedback.append(
                FeedbackItem(
                    category="ats",
                    severity="success",
                    title="Your resume contains most important ATS sections.",
                    message=(
                        "Keep section headings clear and preserve this structure "
                        "when tailoring it."
                    ),
                )
            )

        if not feedback:
            feedback.append(
                FeedbackItem(
                    category="ats",
                    severity="info",
                    title="Tailor your resume for each role.",
                    message=(
                        "Mirror the most relevant keywords from the job description "
                        "where accurate."
                    ),
                )
            )

        return ResumeFeedback(
            overall_summary=self._build_overall_summary(ats_score),
            feedback=feedback,
        )

    def _build_overall_summary(self, ats_score: ATSScore) -> str:
        if ats_score.overall_score >= HIGH_ATS_SCORE_THRESHOLD:
            return "Strong ATS readiness with most core resume sections present."
        if ats_score.overall_score >= 60:
            return "Solid ATS foundation with a few sections to improve."
        return "Resume needs key section improvements before it is ATS ready."
