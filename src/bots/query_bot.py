"""Query bot module."""

from logging import getLogger

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount

from src.core import RequestFailedError
from src.integration.backend import BackendAPI


class QueryBot(ActivityHandler):
    """Query bot class."""

    logger = getLogger(__name__)

    backend: BackendAPI = BackendAPI()

    async def on_members_added_activity(
        self, members_added: list[ChannelAccount], turn_context: TurnContext
    ):
        """Handle members added activity."""
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                try:
                    self.logger.info(f"Creating new user: {member.id}")
                    await self.backend.create_new_user(
                        teams_id=member.id,
                        name=member.name if member.name else "Undefined",
                    )
                    await turn_context.send_activity("Hello and welcome!")
                except RequestFailedError as error:
                    if error.status == 409:
                        await turn_context.send_activity("Welcome again!")
                    else:
                        await turn_context.send_activity("Failed to create user!")

    async def on_message_activity(self, turn_context: TurnContext):
        """Handle message activity."""
        query: str = turn_context.activity.text

        try:
            self.logger.info(f"Querying: {query}")
            result = await self.backend.query(
                teams_id=turn_context.activity.from_property.id,
                query=query,
            )
            await turn_context.send_activity(MessageFactory.text(result))
        except RequestFailedError:
            await turn_context.send_activity("Failed to query!")
