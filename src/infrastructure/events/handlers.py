"""
Event handlers - subscribe to domain events and perform side effects.
"""

from src.domain.user.events import UserCreatedEvent, UserUpdatedEvent, PasswordChangedEvent


def handle_user_created(event: UserCreatedEvent):
    """Handle UserCreatedEvent - runs when user is created."""

    print(f"User {event.username} created! Sending welcome email...")
    # Trigger background task
    # send_welcome_email_task.delay(event.aggregate_id)


def handle_user_updated(event: UserUpdatedEvent):
    """Handle UserUpdatedEvent - runs when user is updated."""

    print(f"User {event.user_id} updated fields: {event.updated_fields}")


def handle_password_changed(event: PasswordChangedEvent):
    """Handle PasswordChangedEvent - runs when password is changed."""

    print(f"User {event.user_id} changed password")
    # send_password_changed_notification_task.delay(event.user_id)
