"""
Dependency injection container.
Provides instances of services and repositories.
"""

from src.domain.user.repositories import UserRepository
from src.domain.user.services import UserDomainService
from src.domain.authentication.services import AuthenticationDomainService
from src.infrastructure.persistence.user_repository import DjangoUserRepository
from src.infrastructure.events.publisher import InMemoryEventPublisher
from src.domain.shared.events import DomainEventPublisher
from src.application.user.use_cases import CreateUserUseCase, UpdateUserUseCase, GetUserUseCase, ChangePasswordUseCase
from src.application.authentication.use_cases import AuthenticateUserUseCase, AuthenticateUserJWTUseCase

# Add these imports
from src.infrastructure.events.handlers import (
    handle_user_created,
    handle_user_updated,
    handle_password_changed,
)
from src.domain.user.events import UserCreatedEvent, UserUpdatedEvent, PasswordChangedEvent


class ServiceContainer:
    """
    Simple dependency injection container.
    In production, consider using a proper DI framework.
    """

    def __init__(self):
        # Infrastructure layer
        self._user_repository: UserRepository = DjangoUserRepository()
        self._event_publisher: DomainEventPublisher = InMemoryEventPublisher()

        # Subscribe to events with specific event types
        self._event_publisher.subscribe(handle_user_created, event_type=UserCreatedEvent)
        self._event_publisher.subscribe(handle_user_updated, event_type=UserUpdatedEvent)
        self._event_publisher.subscribe(handle_password_changed, event_type=PasswordChangedEvent)

        # Domain services
        self._user_domain_service = UserDomainService(self._user_repository)
        self._auth_domain_service = AuthenticationDomainService(self._user_repository)

        # Application use cases
        self._create_user_use_case = CreateUserUseCase(
            user_repository=self._user_repository,
            user_domain_service=self._user_domain_service,
            event_publisher=self._event_publisher,
        )
        self._update_user_use_case = UpdateUserUseCase(
            user_repository=self._user_repository,
            user_domain_service=self._user_domain_service,
            event_publisher=self._event_publisher,
        )
        self._get_user_use_case = GetUserUseCase(user_repository=self._user_repository)
        self._change_password_use_case = ChangePasswordUseCase(
            user_repository=self._user_repository, event_publisher=self._event_publisher
        )
        self._authenticate_user_use_case = AuthenticateUserUseCase(
            user_repository=self._user_repository, auth_domain_service=self._auth_domain_service
        )
        self._authenticate_user_jwt_use_case = AuthenticateUserJWTUseCase(
            user_repository=self._user_repository, auth_domain_service=self._auth_domain_service
        )

    @property
    def create_user_use_case(self) -> CreateUserUseCase:
        return self._create_user_use_case

    @property
    def update_user_use_case(self) -> UpdateUserUseCase:
        return self._update_user_use_case

    @property
    def get_user_use_case(self) -> GetUserUseCase:
        return self._get_user_use_case

    @property
    def change_password_use_case(self) -> ChangePasswordUseCase:
        return self._change_password_use_case

    @property
    def authenticate_user_use_case(self) -> AuthenticateUserUseCase:
        return self._authenticate_user_use_case

    @property
    def authenticate_user_jwt_use_case(self) -> AuthenticateUserJWTUseCase:
        return self._authenticate_user_jwt_use_case


# Global container instance
_container: ServiceContainer = None


def get_container() -> ServiceContainer:
    """Get the global service container instance."""
    global _container
    if _container is None:
        _container = ServiceContainer()
    return _container
