class ResumeParserError(Exception):
    """Base exception for resume parser failures."""


class ResumeParsingError(ResumeParserError):
    """Raised when a supported resume file cannot be parsed."""


class UnsupportedResumeFormatError(ResumeParserError):
    """Raised when a resume file extension cannot be parsed."""
