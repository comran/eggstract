#!/bin/bash

# Change cwd to script location.
cd "$(dirname "$(realpath "$0")")";

check_for_init_py() {
  subdirs=$(find src -type d \( ! -iname __pycache__ \))
  failed=0

  for subdir in $subdirs
  do
    test -f "$subdir/__init__.py"

    if [ $? -eq 1 ]
    then
      echo "$subdir needs an __init__.py file"
      failed=1
    fi

  done

  if [ $failed -eq 1 ]
  then
    exit 1
  fi
}

# Handle different build commands.
case "$1" in
  "cli")
    shift
    python3 src/cli/cli.py $@
    ;;

  "test")
    shift
    echo "#########################################################################################"
    echo "Running check_for_init_py..."
    check_for_init_py
    echo "Done!"
    set -e
    echo ""
    echo "#########################################################################################"
    echo "Running pytest..."
    python3 -m pytest --cov-report=xml --cov=src --verbose --disable-pytest-warnings -n auto $@
    echo "Done!"
    echo ""
    echo "#########################################################################################"
    echo "Running mypy..."
    python3 -m mypy
    echo "Done!"
    echo ""
    echo "#########################################################################################"
    echo "Generating coverage report..."
    python3 -m coverage report -m #--fail-under=50
    echo "Done!"
    ;;

  "test_small")
    shift
    python3 -m pytest --cov-report=xml --cov=src --verbose --disable-pytest-warnings $@
    ;;

  "interactive")
    python3 -c "from IPython import embed; embed()"
    ;;

  "format")
    echo "Running black formatter..."
    python3 -m black -l 100 -t py36 src
    python3 -m black -l 100 -t py36 tst
    echo "Done!"
    echo ""
    echo "Running isort formatter..."
    python3 -m isort src/**/*.py
    python3 -m isort tst/**/*.py
    echo "Done!"
    echo "Running autoflake..."
    python3 -m autoflake --in-place -r src
    echo "Done!"
    ;;

  "lint")
    echo "Running pylint..."
    python3 -m pylint $(find [a-z]* -type d)
    echo "Done!"
    ;;

  *)
    echo "Invalid argument specified: $1"
    exit 1
    ;;
esac
