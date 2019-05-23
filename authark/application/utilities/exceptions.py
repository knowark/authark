
# Base


class ApplicationError(Exception):
    """Application's base error class."""


# Repository

class RepositoryError(ApplicationError):
    """Repositories' base error class."""


class EntityNotFoundError(RepositoryError):
    """The entity was not found in the repository."""


# Coordinators

class UserCreationError(ApplicationError):
    """The user couldn't be created."""
