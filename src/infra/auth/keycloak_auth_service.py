import logging
from typing import Optional

from keycloak import KeycloakAdmin
from pydantic_settings import BaseSettings

from src.infra.auth.auth_service import AuthService


class KeycloakError(Exception):
    pass


class KeycloakSettings(BaseSettings):
    server_url: str = "http://keycloak:8080/"
    realm_name: str = "subscription-service"
    admin_username: str = "admin"
    admin_password: str = "admin"

    model_config = {
        "env_prefix": "KEYCLOAK_",
        "extra": "ignore"
    }


class KeycloakAuthService(AuthService):
    def __init__(self, settings: Optional[KeycloakSettings] = None):
        self.settings = settings or KeycloakSettings()
        self.logger = logging.getLogger(__name__)

        try:
            self.keycloak_admin = KeycloakAdmin(
                server_url=self.settings.server_url,
                username=self.settings.admin_username,
                password=self.settings.admin_password,
                realm_name=self.settings.realm_name,
                user_realm_name="master",
                verify=True,
            )

        except Exception as e:
            self.logger.error(f"Failed to initialize Keycloak client: {e}")
            raise

    def find_by_email(self, email: str) -> Optional[str]:
        try:
            users = self.keycloak_admin.get_users({"email": email})
        except Exception as e:
            self.logger.error(f"Error finding user by email: {e}")
            raise KeycloakError(f"Failed to find user in Keycloak")
        else:
            if users and len(users) > 0:
                return users[0]["id"]

    def create_user(self, email: str, password: str) -> str:
        """Create a new user in Keycloak"""
        try:
            # Create user with email
            user_id = self.keycloak_admin.create_user(
                {
                    "email": email,
                    "username": email,  # Using email as username
                    "enabled": True,
                    "emailVerified": False,
                    "credentials": [
                        {"type": "password", "value": password, "temporary": False}
                    ],
                }
            )

            return user_id
        except Exception as e:
            self.logger.error(f"Error creating user in Keycloak: {e}")
            raise KeycloakError(f"Failed to create user in Keycloak")
