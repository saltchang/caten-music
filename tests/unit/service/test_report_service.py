from unittest.mock import AsyncMock

import pytest
from app.core.entities.song_report import SongReport
from app.core.exceptions import InvalidInputError
from app.service.report_service import ReportService


@pytest.fixture
def report_repo():
    return AsyncMock()


@pytest.fixture
def service(report_repo):
    return ReportService(report_repo=report_repo)


class TestCreateReport:
    async def test_create_report(self, service, report_repo):
        """
        GIVEN valid report data with a sufficient description
        WHEN create_report is called
        THEN the report is persisted and returned
        """
        # Arrange
        report_repo.create.return_value = SongReport(
            id=1,
            description='Wrong lyrics in verse 2',
            song_sid='1001001',
            user_id=1,
        )

        # Act
        result = await service.create_report(
            description='Wrong lyrics in verse 2',
            song_sid='1001001',
            user_id=1,
        )

        # Assert
        assert result.description == 'Wrong lyrics in verse 2'
        report_repo.create.assert_called_once()


class TestListReports:
    async def test_list_reports(self, service, report_repo):
        """
        GIVEN two reports exist
        WHEN list_reports is called
        THEN all reports are returned
        """
        # Arrange
        report_repo.list_all.return_value = [
            SongReport(id=1, description='Wrong lyrics', song_sid='1011054', user_id=1),
            SongReport(id=2, description='Broken audio', song_sid='1010066', user_id=2),
        ]

        # Act
        result = await service.list_reports()

        # Assert
        assert len(result) == 2
        report_repo.list_all.assert_called_once()


class TestCreateReportValidation:
    async def test_create_report_too_short(self, service):
        """
        GIVEN a description that is too short
        WHEN create_report is called
        THEN InvalidInputError is raised
        """
        # Act & Assert
        with pytest.raises(InvalidInputError):
            await service.create_report(
                description='Hi',
                song_sid='1001001',
                user_id=1,
            )
