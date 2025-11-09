"""
User repository implementation (adapter).
Adapts Django ORM models to domain entities.
"""

from typing import Optional, List
from src.domain.user.entities import User
from src.domain.user.repositories import UserRepository
from src.users.models import User as DjangoUser


class DjangoUserRepository(UserRepository):
    """
    Django ORM implementation of UserRepository.
    Adapts Django User model to domain User entity.
    """

    def _to_domain(self, django_user: DjangoUser) -> User:
        """Convert Django User model to domain User entity."""
        return User(
            id=django_user.id,
            username=django_user.username,
            email=django_user.email,
            first_name=getattr(django_user, "first_name", None),
            last_name=getattr(django_user, "last_name", None),
            is_active=django_user.is_active,
            is_staff=django_user.is_staff,
            is_admin=django_user.is_admin,
            is_superuser=django_user.is_superuser,
            created_at=(
                django_user.date_joined if hasattr(django_user, "date_joined") and django_user.date_joined else None
            ),
        )

    def _to_django(self, domain_user: User) -> DjangoUser:
        """Convert domain User entity to Django User model."""
        if domain_user.id:
            # Update existing user
            django_user = DjangoUser.objects.get(id=domain_user.id)
            django_user.username = domain_user.username
            django_user.email = domain_user.email
            django_user.first_name = domain_user.first_name or ""
            django_user.last_name = domain_user.last_name or ""
            if hasattr(django_user, "phone_number"):
                django_user.phone_number = domain_user.phone_number
            django_user.is_active = domain_user.is_active
            django_user.is_staff = domain_user.is_staff
            django_user.is_admin = domain_user.is_admin
            django_user.is_superuser = domain_user.is_superuser

        else:
            # Create new user
            django_user = DjangoUser(
                username=domain_user.username,
                email=domain_user.email,
                first_name=domain_user.first_name or "",
                last_name=domain_user.last_name or "",
                is_active=domain_user.is_active,
                is_staff=domain_user.is_staff,
                is_admin=domain_user.is_admin,
                is_superuser=domain_user.is_superuser,
            )
            if hasattr(django_user, "phone_number"):
                django_user.phone_number = domain_user.phone_number

        return django_user

    def get_by_id(self, entity_id: any) -> Optional[User]:
        """Retrieve a user by ID."""
        try:
            django_user = DjangoUser.objects.get(id=entity_id)
            return self._to_domain(django_user)
        except DjangoUser.DoesNotExist:
            return None

    def get_all(self) -> List[User]:
        """Retrieve all users."""
        django_users = DjangoUser.objects.all()
        return [self._to_domain(user) for user in django_users]

    def save(self, entity: User) -> User:
        """Save or update a user."""
        django_user = self._to_django(entity)
        if hasattr(entity, "password"):
            django_user.set_password(entity.password)

        django_user.full_clean()
        django_user.save()
        return self._to_domain(django_user)

    def delete(self, entity: User) -> None:
        """Delete a user."""
        if entity.id:
            DjangoUser.objects.filter(id=entity.id).delete()

    def get_by_username(self, username: str) -> Optional[User]:
        """Retrieve a user by username."""
        try:
            django_user = DjangoUser.objects.get(username=username)
            return self._to_domain(django_user)
        except DjangoUser.DoesNotExist:
            return None

    def get_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by email."""
        try:
            django_user = DjangoUser.objects.get(email=email.lower())
            return self._to_domain(django_user)
        except DjangoUser.DoesNotExist:
            return None

    def exists_by_username(self, username: str) -> bool:
        """Check if a user exists with the given username."""
        return DjangoUser.objects.filter(username=username).exists()

    def exists_by_email(self, email: str) -> bool:
        """Check if a user exists with the given email."""
        return DjangoUser.objects.filter(email=email.lower()).exists()

    def get_active_users(self) -> List[User]:
        """Retrieve all active users."""
        django_users = DjangoUser.objects.filter(is_active=True)
        return [self._to_domain(user) for user in django_users]
