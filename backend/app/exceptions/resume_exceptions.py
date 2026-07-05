"""
Resume module custom exceptions.
"""


class ResumeNotFoundException(Exception):
    """
    Raised when a resume is not found.
    """

    def __init__(self, resume_id: int):
        self.message = f"Resume with id {resume_id} not found."
        super().__init__(self.message)


class InvalidResumeFileException(Exception):
    """
    Raised when uploaded resume is invalid.
    """

    def __init__(self):
        self.message = "Invalid resume file."
        super().__init__(self.message)


class UnsupportedResumeTypeException(Exception):
    """
    Raised when resume type is unsupported.
    """

    def __init__(self):
        self.message = "Unsupported resume file type."
        super().__init__(self.message)


class ResumeTooLargeException(Exception):
    """
    Raised when resume exceeds maximum allowed size.
    """

    def __init__(self):
        self.message = "Resume file exceeds maximum allowed size."
        super().__init__(self.message)
