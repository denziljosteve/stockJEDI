#!/bin/bash
set -e

# Database migration script
# Usage: ./migrate.sh [upgrade|downgrade|revision|history|current]

ALEMBIC_CMD=${1:-upgrade}
ALEMBIC_REVISION=${2:-head}

case "$ALEMBIC_CMD" in
    upgrade)
        echo "Running database upgrades..."
        alembic upgrade "$ALEMBIC_REVISION"
        ;;
    downgrade)
        echo "Running database downgrade..."
        alembic downgrade "$ALEMBIC_REVISION"
        ;;
    revision)
        echo "Creating new migration..."
        alembic revision --autogenerate -m "$ALEMBIC_REVISION"
        ;;
    history)
        echo "Migration history:"
        alembic history
        ;;
    current)
        echo "Current revision:"
        alembic current
        ;;
    *)
        echo "Usage: $0 {upgrade|downgrade|revision|history|current} [revision]"
        exit 1
        ;;
esac
