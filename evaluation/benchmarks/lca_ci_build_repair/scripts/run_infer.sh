#!/usr/bin/env bash
set -eo pipefail

source "evaluation/utils/version_control.sh"

MODEL_CONFIG=$1

get_wsai_code_version

echo "WSAI_CODE_VERSION: $WSAI_CODE_VERSION"
echo "MODEL_CONFIG: $MODEL_CONFIG"

EVAL_NOTE="$WSAI_CODE_VERSION"
if [ -n "$EXP_NAME" ]; then
  EVAL_NOTE="$EVAL_NOTE-$EXP_NAME"
fi

function run_eval() {
  COMMAND="poetry run python ./evaluation/benchmarks/lca_ci_build_repair/run_infer.py \
    --llm-config $MODEL_CONFIG "

  # Run the command
  eval $COMMAND
}

#unset SANDBOX_ENV_GITHUB_TOKEN # prevent the agent from using the github token to push
run_eval
