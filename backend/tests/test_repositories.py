"""Unit tests for repository pattern implementation."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime

# Test the base repository classes
from repositories.base import (
    BaseRepository,
    ConflictError,
    NotFoundError,
    PaginatedResult,
    PaginationParams,
    SortParams,
)


class TestPaginationParams:
    """Tests for PaginationParams."""

    def test_default_values(self):
        """Test default pagination values."""
        params = PaginationParams()
        assert params.skip == 0
        assert params.limit == 100
        assert params.offset == 0

    def test_custom_values(self):
        """Test custom pagination values."""
        params = PaginationParams(skip=10, limit=50)
        assert params.skip == 10
        assert params.limit == 50
        assert params.offset == 10

    def test_negative_skip_becomes_zero(self):
        """Test negative skip is clamped to 0."""
        params = PaginationParams(skip=-5, limit=50)
        assert params.skip == 0

    def test_limit_capped_at_1000(self):
        """Test limit is capped at 1000."""
        params = PaginationParams(skip=0, limit=2000)
        assert params.limit == 1000

    def test_limit_minimum_is_one(self):
        """Test limit minimum is 1."""
        params = PaginationParams(skip=0, limit=0)
        assert params.limit == 1


class TestSortParams:
    """Tests for SortParams."""

    def test_default_values(self):
        """Test default sort values."""
        params = SortParams()
        assert params.sort_by == "created_at"
        assert params.sort_order == "desc"

    def test_custom_values(self):
        """Test custom sort values."""
        params = SortParams(sort_by="name", sort_order="asc")
        assert params.sort_by == "name"
        assert params.sort_order == "asc"

    def test_sort_order_lowercase(self):
        """Test sort order is lowercased."""
        params = SortParams(sort_by="name", sort_order="ASC")
        assert params.sort_order == "asc"


class TestPaginatedResult:
    """Tests for PaginatedResult."""

    def test_paginated_result_with_more(self):
        """Test paginated result when there are more items."""
        result = PaginatedResult(
            items=["a", "b", "c"],
            total=10,
            skip=0,
            limit=3,
        )
        assert len(result.items) == 3
        assert result.total == 10
        assert result.skip == 0
        assert result.limit == 3
        assert result.has_more is True

    def test_paginated_result_no_more(self):
        """Test paginated result when there are no more items."""
        result = PaginatedResult(
            items=["a", "b", "c"],
            total=3,
            skip=0,
            limit=10,
        )
        assert result.has_more is False

    def test_paginated_result_partial_last_page(self):
        """Test paginated result on partial last page."""
        result = PaginatedResult(
            items=["a", "b"],
            total=12,
            skip=10,
            limit=5,
        )
        assert result.has_more is False


class TestNotFoundError:
    """Tests for NotFoundError."""

    def test_error_message(self):
        """Test error message format."""
        error = NotFoundError("User", "123")
        assert str(error) == "User with id '123' not found"
        assert error.model_name == "User"
        assert error.entity_id == "123"


class TestConflictError:
    """Tests for ConflictError."""

    def test_error_message(self):
        """Test conflict error message."""
        error = ConflictError("Email already exists")
        assert str(error) == "Email already exists"


class TestBaseRepository:
    """Tests for BaseRepository base class functionality."""

    @pytest.fixture
    def mock_session(self):
        """Create a mock async session."""
        session = AsyncMock()
        session.execute = AsyncMock()
        session.flush = AsyncMock()
        session.refresh = AsyncMock()
        session.delete = AsyncMock()
        session.add = MagicMock()
        session.rollback = AsyncMock()
        return session

    @pytest.fixture
    def mock_model(self):
        """Create a mock model class."""
        class MockModel:
            __tablename__ = "mock_table"
            id = MagicMock()
            name = MagicMock()
            created_at = MagicMock()
            
            def __init__(self, **kwargs):
                for key, value in kwargs.items():
                    setattr(self, key, value)
        
        # Set up the __table__.columns for inspection
        MockModel.__table__ = MagicMock()
        MockModel.__table__.columns = []
        
        return MockModel

    def test_repository_initialization(self, mock_session):
        """Test repository can be initialized with session."""
        class TestRepo(BaseRepository):
            model = MagicMock()
        
        repo = TestRepo(mock_session)
        assert repo.session == mock_session


# Test model and repository imports
class TestRepositoryImports:
    """Test that all repositories can be imported."""

    def test_import_base_repository(self):
        """Test BaseRepository import."""
        from repositories.base import BaseRepository
        assert BaseRepository is not None

    def test_import_user_repository(self):
        """Test UserRepository import."""
        from repositories.user import UserRepository
        assert UserRepository is not None

    def test_import_project_repository(self):
        """Test ProjectRepository import."""
        from repositories.project import ProjectRepository
        assert ProjectRepository is not None

    def test_import_service_repository(self):
        """Test ServiceRepository import."""
        from repositories.service import ServiceRepository
        assert ServiceRepository is not None

    def test_import_build_repository(self):
        """Test BuildRepository import."""
        from repositories.build import BuildRepository
        assert BuildRepository is not None

    def test_import_team_repository(self):
        """Test TeamRepository import."""
        from repositories.team import TeamRepository
        assert TeamRepository is not None

    def test_import_team_member_repository(self):
        """Test TeamMemberRepository import."""
        from repositories.team_member import TeamMemberRepository
        assert TeamMemberRepository is not None

    def test_import_tenant_repository(self):
        """Test TenantRepository import."""
        from repositories.tenant import TenantRepository
        assert TenantRepository is not None

    def test_import_environment_variable_repository(self):
        """Test EnvironmentVariableRepository import."""
        from repositories.environment_variable import EnvironmentVariableRepository
        assert EnvironmentVariableRepository is not None

    def test_import_webhook_repository(self):
        """Test WebhookRepository import."""
        from repositories.webhook import WebhookRepository
        assert WebhookRepository is not None


class TestModelImports:
    """Test that all models can be imported."""

    def test_import_models(self):
        """Test all models can be imported from models package."""
        from models import (
            Build,
            BuildStatus,
            EnvironmentVariable,
            Project,
            Service,
            ServiceStatus,
            Team,
            TeamMember,
            TeamMemberRole,
            Tenant,
            User,
            UserRole,
            Webhook,
            WebhookProvider,
        )
        
        # Verify models are classes
        assert Build is not None
        assert EnvironmentVariable is not None
        assert Project is not None
        assert Service is not None
        assert Team is not None
        assert TeamMember is not None
        assert Tenant is not None
        assert User is not None
        assert Webhook is not None
        
        # Verify enums
        assert BuildStatus.PENDING == "pending"
        assert ServiceStatus.RUNNING == "running"
        assert UserRole.ADMIN == "admin"
        assert TeamMemberRole.OWNER == "owner"
        assert WebhookProvider.GITHUB == "github"


class TestEnumValues:
    """Test enum values are correct."""

    def test_build_status_values(self):
        """Test BuildStatus enum values."""
        from models.base import BuildStatus
        
        assert BuildStatus.PENDING.value == "pending"
        assert BuildStatus.BUILDING.value == "building"
        assert BuildStatus.SUCCESS.value == "success"
        assert BuildStatus.FAILED.value == "failed"

    def test_service_status_values(self):
        """Test ServiceStatus enum values."""
        from models.base import ServiceStatus
        
        assert ServiceStatus.PENDING.value == "pending"
        assert ServiceStatus.BUILDING.value == "building"
        assert ServiceStatus.RUNNING.value == "running"
        assert ServiceStatus.FAILED.value == "failed"
        assert ServiceStatus.STOPPED.value == "stopped"

    def test_user_role_values(self):
        """Test UserRole enum values."""
        from models.base import UserRole
        
        assert UserRole.OWNER.value == "owner"
        assert UserRole.ADMIN.value == "admin"
        assert UserRole.MEMBER.value == "member"

    def test_team_member_role_values(self):
        """Test TeamMemberRole enum values."""
        from models.base import TeamMemberRole
        
        assert TeamMemberRole.OWNER.value == "owner"
        assert TeamMemberRole.ADMIN.value == "admin"
        assert TeamMemberRole.MEMBER.value == "member"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
