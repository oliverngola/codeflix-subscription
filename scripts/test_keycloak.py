import logging
import sys

from src.infra.auth.keycloak_auth_service import KeycloakAuthService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    try:
        # Initialize Keycloak service
        logger.info("Initializing Keycloak service...")
        auth_service = KeycloakAuthService()

        # Test find_by_email
        test_email = "test@example.com"
        logger.info(f"Looking for user with email: {test_email}")
        user_id = auth_service.find_by_email(test_email)

        if user_id:
            logger.info(f"Found user: {user_id}")
        else:
            logger.info(f"User not found. Creating new user...")
            new_user_id = auth_service.create_user(test_email, "password123")
            logger.info(f"Created user with ID: {new_user_id}")

        logger.info("Keycloak test completed successfully!")

    except Exception as e:
        logger.error(f"Error testing Keycloak: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
