import logging

from app.database.database_repository import delete_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info("Delete database init.")
    delete_db()
    logger.info("Delete database end.")


if __name__ == "__main__":
    main()
