from typing import Optional
from src.application.shared.dtos import UserDTO, UserCreateDTO, UserUpdateDTO
from src.application.shared.exceptions import ValidationError, NotFoundError, ConflictError
from src.domain.user.entities import User
from src.domain.user.repositories import UserRepository
from src.domain.user.services import UserDomainService
from src.domain.user.events import UserCreatedEvent, UserUpdatedEvent
from src.domain.shared.events import DomainEventPublisher
from src.domain.shared.exceptions import BusinessRuleViolationError
from rest_framework.exceptions import ValidationError as DRFValidationError
from django.utils.translation import gettext_lazy as _


class CreateUserUseCase:
    """
    Use case for creating a new user.
    """

    def __init__(
        self,
        user_repository: UserRepository,
        user_domain_service: UserDomainService,
        event_publisher: Optional[DomainEventPublisher] = None,
    ):
        self._user_repository = user_repository
        self._user_domain_service = user_domain_service
        self._event_publisher = event_publisher

    def execute(self, user_data: UserCreateDTO) -> UserDTO:
        """
        Create a new user.

        Raises:
            ValidationError: If validation fails (e.g., invalid username/email format)
            ConflictError: If username/email already exists
        """
        # Validate using domain service
        try:
            self._user_domain_service.validate_user_creation(username=user_data.username, email=user_data.email)
        except BusinessRuleViolationError as e:
            # Convert domain exception to application exception
            if "already taken" in e.message:
                raise ConflictError(e.message, extra={"field": "username" if "Username" in e.message else "email"})
            raise ValidationError(e.message, extra=e.details)

        # Create domain entity
        user = User(
            username=user_data.username,
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            is_active=True,
            password=user_data.password,
        )

        # Save user
        saved_user = self._user_repository.save(user)

        # Publish domain event
        if self._event_publisher:
            event = UserCreatedEvent(aggregate_id=saved_user.id, username=saved_user.username, email=saved_user.email)
            self._event_publisher.publish(event)

        return self._to_dto(saved_user)

    @staticmethod
    def _to_dto(user: User) -> UserDTO:
        """Convert User entity to UserDTO."""
        return UserDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            is_staff=user.is_staff,
            is_admin=user.is_admin,
            is_superuser=user.is_superuser,
        )


class UpdateUserUseCase:
    """
    Use case for updating an existing user.
    """

    def __init__(
        self,
        user_repository: UserRepository,
        user_domain_service: UserDomainService,
        event_publisher: Optional[DomainEventPublisher] = None,
    ):
        self._user_repository = user_repository
        self._user_domain_service = user_domain_service
        self._event_publisher = event_publisher

    def execute(self, user_id: int, user_data: UserUpdateDTO) -> UserDTO:
        """
        Update an existing user.

        Raises:
            NotFoundError: If user not found
            ConflictError: If email already exists
        """
        # Get user
        user = self._user_repository.get_by_id(user_id)
        if user is None:
            raise NotFoundError(message=f"User with ID {user_id} not found")

        # Validate email uniqueness if email is being updated
        if user_data.email and user_data.email != user.email:
            if not self._user_domain_service.is_email_unique(user_data.email, exclude_user_id=user_id):
                raise ConflictError(f"Email '{user_data.email}' is already taken", extra={"field": "email"})

        # Update fields
        updated_fields = []
        if user_data.first_name is not None:
            user.first_name = user_data.first_name
            updated_fields.append("first_name")
        if user_data.last_name is not None:
            user.last_name = user_data.last_name
            updated_fields.append("last_name")
        if user_data.email is not None:
            user.email = user_data.email.lower().strip()
            updated_fields.append("email")
        if user_data.phone_number is not None:
            user.phone_number = user_data.phone_number
            updated_fields.append("phone_number")

        # Save user
        saved_user = self._user_repository.save(user)

        # Publish domain event
        if self._event_publisher and updated_fields:
            event = UserUpdatedEvent(aggregate_id=saved_user.id, user_id=saved_user.id, updated_fields=updated_fields)
            self._event_publisher.publish(event)

        return self._to_dto(saved_user)

    @staticmethod
    def _to_dto(user: User) -> UserDTO:
        """Convert User entity to UserDTO."""
        return UserDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            is_staff=user.is_staff,
            is_admin=user.is_admin,
            is_superuser=user.is_superuser,
        )


class GetUserUseCase:
    """
    Use case for retrieving a user.
    """

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def execute(self, user_id: int) -> UserDTO:
        """
        Get a user by ID.

        Raises:
            NotFoundError: If user not found
        """
        user = self._user_repository.get_by_id(user_id)
        if user is None:
            raise NotFoundError(f"User with ID {user_id} not found")

        return self._to_dto(user)

    @staticmethod
    def _to_dto(user: User) -> UserDTO:
        """Convert User entity to UserDTO."""
        return UserDTO(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active,
            is_staff=user.is_staff,
            is_admin=user.is_admin,
            is_superuser=user.is_superuser,
        )


class ChangePasswordUseCase:
    """
    Use case for changing a user's password.
    """

    def __init__(self, user_repository: UserRepository, event_publisher: Optional[DomainEventPublisher] = None):
        self._user_repository = user_repository
        self._event_publisher = event_publisher

    def execute(self, user_id: int, old_password: str, new_password: str) -> None:
        """
        Change a user's password.

        Raises:
            NotFoundError: If user not found
            ValidationError: If old password is incorrect or new password is invalid
        """
        # Get user
        user = self._user_repository.get_by_id(user_id)
        if user is None:
            raise NotFoundError(f"User with ID {user_id} not found")

        # Verify old password using Django's check_password
        from django.contrib.auth import password_validation

        if not user.check_password(old_password):
            raise DRFValidationError(_("Your old password was entered incorrectly. Please enter it again."))

        # Validate new password (Django's password validation)
        # Get Django user for validation
        from src.users.models import User as DjangoUser

        django_user = DjangoUser.objects.get(id=user.id)
        password_validation.validate_password(new_password, django_user)

        # Save user
        self._user_repository.save(user)

        # Publish domain event
        if self._event_publisher:
            from src.domain.user.events import PasswordChangedEvent

            event = PasswordChangedEvent(aggregate_id=user.id, user_id=user.id)
            self._event_publisher.publish(event)
