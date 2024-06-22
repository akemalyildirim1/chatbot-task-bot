"""Backend integration module."""

from pydantic import BaseModel, validate_call

from src.core import configuration

from .utils import HttpResponse, send_http_request


class BackendAPI(BaseModel):
    """Backend API class.

    Attributes:
        url: The backend API URL.

    Methods:
        create_new_user: Create a new user.
        query: Search the query in the indexed documents.
    """

    url: str = configuration.BACKEND_API_URL

    @validate_call
    async def create_new_user(self, teams_id: str, name: str) -> None:
        """Create a new user.

        Arguments:
            teams_id: The teams ID of the user.
            name: The name of the user.

        Returns:
            None.
        """
        await send_http_request(
            url=f"{self.url}/user/",
            method="POST",
            body={
                "teams_id": teams_id,
                "name": name,
            },
        )

    @validate_call
    async def query(self, teams_id: str, query: str) -> str:
        """Search the query in the indexed documents.

        Arguments:
            teams_id: The teams ID of the user.
            query: The query to search.

        Returns:
            The search result.
        """
        response: HttpResponse = await send_http_request(
            url=f"{self.url}/query/?teams_id={teams_id}&query={query}",
            method="GET",
        )
        return response.data
