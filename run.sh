#!/bin/bash

# Change cwd to script location.
cd "$(dirname "$(realpath "$0")")";

# Handle different build commands.
case "$1" in
  "test")
    python3 -m pytest --cov-report=xml --cov=src
    ;;

  "interactive")
    python3 -c "from IPython import embed; embed()"
    ;;

  *)
    echo "Invalid argument specified: $1"
    exit 1
    ;;
esac
