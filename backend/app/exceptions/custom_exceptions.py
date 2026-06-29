class JobNotFoundException(Exception):
    """
    Raised when a requested job does not exist.
    """

    def __init__(self, job_id: int):
        self.message = f"Job with id {job_id} not found."
        super().__init__(self.message)


class DuplicateEmailException(Exception):
    """
    Raised when email already exists.
    """

    def __init__(self, email: str):
        self.message = f"Email '{email}' is already registered."
        super().__init__(self.message)


class DuplicateUsernameException(Exception):
    """
    Raised when username already exists.
    """

    def __init__(self, username: str):
        self.message = f"Username '{username}' already exists."
        super().__init__(self.message)


class UserNotFoundException(Exception):
    """
    Raised when user is not found.
    """

    def __init__(self, user_id: int):
        self.message = f"User with id {user_id} not found."
        super().__init__(self.message)


class InvalidCredentialsException(Exception):
    """
    Raised when login credentials are invalid.
    """

    def __init__(self):
        self.message = "Invalid email or password."
        super().__init__(self.message)


class InactiveUserException(Exception):
    """
    Raised when user account is inactive.
    """

    def __init__(self):
        self.message = "User account is inactive."
        super().__init__(self.message)


class UnauthorizedException(Exception):
    """
    Raised when authentication token is invalid.
    """

    def __init__(self):
        self.message = "Unauthorized."
        super().__init__(self.message)