
# Base


class ApplicationError(Exception):
    """Application's base error class."""


# Repository

class RepositoryError(ApplicationError):
    """Repositories' base error class."""


class EntityNotFoundError(RepositoryError):
    """The entity was not found in the repository."""

# Services


class ServiceError(ApplicationError):
    """Services' base error class."""


class TenantError(ServiceError):
    """Tenancy base error class."""


class TenantLocationError(TenantError):
    """The tenant location type was not found."""

# Coordinators


class UserCreationError(ApplicationError):
    """The user couldn't be created."""