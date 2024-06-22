"""Project configurations."""

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class TeamsConfiguration(BaseModel):
    """Teams configurations class.

    Attributes:
    """

    APP_ID: str
    APP_PASSWORD: str


class Configuration(BaseSettings):
    """Project settings class."""

    model_config = SettingsConfigDict(env_nested_delimiter="__")

    TEAMS: TeamsConfiguration
    BACKEND_API_URL: str


configuration: Configuration = Configuration()


class AdapterConfiguration:
    """Adapter Configuration"""

    PORT = 3000
    APP_ID = configuration.TEAMS.APP_ID
    APP_PASSWORD = configuration.TEAMS.APP_PASSWORD
    APP_TYPE = "MultiTenant"


adapter_configuration: AdapterConfiguration = AdapterConfiguration()
