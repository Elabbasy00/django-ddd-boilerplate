"""
Common exceptions - kept for backward compatibility.
New code should use exceptions from application/shared/exceptions.py
"""

from src.application.shared.exceptions import ApplicationError

# Re-export for backward compatibility
__all__ = ["ApplicationError"]
