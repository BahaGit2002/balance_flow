# from unittest.mock import MagicMock, AsyncMock, patch
# from fastapi import Request
#
# import pytest
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from app.api.deps import get_current_user
# from app.models import User
#
#
# @pytest.mark.asyncio
# async def test_get_current_user_success():
#     pass
#     # request = MagicMock(spec=Request)
#     # request.state.user = {"user_id": 1}
#     #
#     # db = AsyncMock(spec=AsyncSession)
#     #
#     # with patch("app.repositories.users.UserRepository") as MockUserRepository:
#     #     mock_user_repo = MockUserRepository.return_value
#     #     mock_user_repo.get_by_id = AsyncMock(
#     #         return_value=User(
#     #             id=1, full_name="Test User", email="test@example.com",
#     #             is_admin=True, password="testpass"
#     #         )
#     #     )
#     #
#     #     user = await get_current_user(request, db)
#
#         # Assertions
#         # assert user.id == 1
#         # assert user.is_admin is True
#         # mock_user_repo.get_by_id.assert_called_once_with(1)
#
#
# # @pytest.mark.asyncio
# # async def test_get_current_user_no_payload():
# #     pass
# #
# #
# # @pytest.mark.asyncio
# # async def test_get_current_user_no_payload():
# #     pass
# #
# #
# # @pytest.mark.asyncio
# # async def test_get_current_user_invalid_payload():
# #     pass
# #
# #
# # @pytest.mark.asyncio
# # async def test_get_current_user_user_not_found():
# #     pass
# #
# #
# # @pytest.mark.asyncio
# # async def test_admin_required_success():
# #     pass
# #
# #
# # @pytest.mark.asyncio
# # async def test_admin_required_not_admin():
# #     pass
