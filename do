#!/usr/bin/env bash



## quality-gates: Quick and easy quality confirmations
function task_quality_gates {
  set -e
  task_format
  task_type_check
  task_lint
  task_test
}

## formatting: Applies formatting
function task_format {
  poetry run isort .
  poetry run black .
}

## type-check: Runs mypy static type analysis
function task_type_check {
  poetry run mypy
}

## lint: Runs flake8 linting
function task_lint {
  poetry run flake8 .
}

## test: Runs unit tests
function task_test {
  poetry run pytest .
}


#-------- All task definitions go above this line --------#

function task_usage {
    echo "Usage: $0"
    sed -n 's/^##//p' <"$0" | column -t -s ':' |  sed -E $'s/^/\t/'
}

cmd=${1:-}
shift || true
resolved_command=$(echo "task_${cmd}" | sed 's/-/_/g')
if [[ "$(LC_ALL=C type -t "${resolved_command}")" == "function" ]]; then
    pushd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null
    ${resolved_command} "$@"
else
    task_usage
    if [ -n "${cmd}" ]; then
      echo "'$cmd' could not be resolved - please use one of the above tasks"
      exit 1
    fi
fi
