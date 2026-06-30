import re

CATEGORY_WEIGHTS = {
    "contact_information": 10,
    "professional_summary": 10,
    "skills": 15,
    "education": 10,
    "experience": 20,
    "projects": 15,
    "keywords": 10,
    "action_verbs": 5,
    "quantified_achievements": 5,
    "formatting": 10,
}
MAX_ATS_SCORE = 100

ACTION_VERBS = {
    "achieved",
    "analyzed",
    "architected",
    "automated",
    "built",
    "collaborated",
    "created",
    "delivered",
    "designed",
    "developed",
    "implemented",
    "improved",
    "increased",
    "launched",
    "led",
    "managed",
    "optimized",
    "reduced",
    "resolved",
    "shipped",
}

ATS_KEYWORDS = {
    "api",
    "aws",
    "azure",
    "ci",
    "cloud",
    "css",
    "database",
    "deployment",
    "docker",
    "fastapi",
    "git",
    "html",
    "java",
    "javascript",
    "kubernetes",
    "linux",
    "machine",
    "microservices",
    "node",
    "postgresql",
    "python",
    "react",
    "rest",
    "sql",
    "typescript",
}

SECTION_HEADINGS = {
    "education",
    "experience",
    "professional experience",
    "professional summary",
    "profile",
    "projects",
    "skills",
    "summary",
    "technical skills",
    "work experience",
}

SUMMARY_HEADINGS = {
    "career summary",
    "objective",
    "professional summary",
    "profile",
    "summary",
}

KEYWORD_PATTERN = re.compile(r"[a-z0-9][a-z0-9+#.\-]*")
QUANTIFIED_ACHIEVEMENT_PATTERN = re.compile(
    r"(?<!\w)(?:\$?\d+(?:[,.]\d+)*(?:\+|%|x|k|m)?)(?!\w)",
    re.IGNORECASE,
)
