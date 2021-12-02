

# Base

class ApplicationError(Exception):
    """Application's base error class."""


# Providers

class ProviderError(ApplicationError):
    """Providers' base error class."""


class TenantError(ProviderError):
    """Tenancy base error class."""


class TenantLocationError(TenantError):
    """The tenant location type was not found."""


class AuthError(ProviderError):
    """Auth error"""


class AuthenticationError(AuthError):
    """Authentication error"""


class AuthorizationError(ProviderError):
    """Authorization error"""


# Repository

class RepositoryError(ApplicationError):
    """Repositories' base error class."""


class EntityNotFoundError(RepositoryError):
    """The entity was not found in the repository."""


# Services

class ServiceError(ApplicationError):
    """Services' base error class."""


class NotificationError(ServiceError):
    """Notification generation error class."""

# Coordinators

class UserCreationError(ApplicationError):
    """The user couldn't be created."""


class TenantAlreadyExistsError(ApplicationError):
    """Raised when attempting to create an already existing tenant"""

class EmailExistsError(ApplicationError):
    """Email Exists Error"""
