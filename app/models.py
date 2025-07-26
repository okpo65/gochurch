"""
Centralized models registry to avoid circular imports
"""

# Import all models here to register them with SQLAlchemy Base
from app.user.models import User, Profile
from app.church.models import Church
from app.verification.models import IdentityVerification
from app.community.models import Board, Post, PostTag, Comment
from app.action.models import ActionLog

# Export all models for easy importing
__all__ = [
    'User',
    'Profile', 
    'Church',
    'IdentityVerification',
    'Board',
    'Post',
    'PostTag',
    'Comment',
    'ActionLog'
]

# Models dictionary for dynamic access
MODELS = {
    'User': User,
    'Profile': Profile,
    'Church': Church,
    'IdentityVerification': IdentityVerification,
    'Board': Board,
    'Post': Post,
    'PostTag': PostTag,
    'Comment': Comment,
    'ActionLog': ActionLog
}

def get_model(model_name: str):
    """Get model class by name"""
    return MODELS.get(model_name)

def get_all_models():
    """Get all model classes"""
    return MODELS
