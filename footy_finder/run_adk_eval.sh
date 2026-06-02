#!/usr/bin/env bash

SCRIPT_FOLDER=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
CONFIG_FILE=$SCRIPT_FOLDER"/eval_config.json"
EVAL_FILE=$SCRIPT_FOLDER"/eval_set_with_scenarios.evalset.json"

uv run adk eval footy_finder "$EVAL_FILE" --config_file_path "$CONFIG_FILE" --eval_storage_uri gs://onyx-eval-bucket \
  > eval_result.log
