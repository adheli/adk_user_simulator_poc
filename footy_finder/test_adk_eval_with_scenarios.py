import json
import logging
import os
from pathlib import Path

import pytest
from google.adk.evaluation.agent_evaluator import AgentEvaluator
from google.adk.evaluation.eval_config import EvalConfig
from google.adk.evaluation.eval_set import EvalSet


logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
AGENT_DIR = PROJECT_ROOT / "footy_finder"
EVAL_CONFIG_PATH = AGENT_DIR / "eval_config.json"
EVALSET_PATH = AGENT_DIR / "eval_set_with_scenarios.evalset.json"


def test_eval_files_reference_footy_finder_agent() -> None:
    eval_config = json.loads(EVAL_CONFIG_PATH.read_text())
    eval_set = json.loads(EVALSET_PATH.read_text())

    assert "criteria" in eval_config
    assert "user_simulator_config" in eval_config
    assert "safety_v1" not in eval_config["criteria"]
    assert "rubric_based_final_response_quality_v1" in eval_config["criteria"]

    assert eval_set["eval_set_id"] == "eval_set_with_scenarios"
    assert eval_set["name"] == "eval_set_with_scenarios"
    assert eval_set["eval_cases"], "Expected at least one eval case"

    for case in eval_set["eval_cases"]:
        assert case["session_input"]["app_name"] == "footy_finder"


@pytest.mark.asyncio
async def test_adk_eval_scenarios_against_agent() -> None:
    required_env = [
        "MODEL_NAME",
        "GOOGLE_GENAI_USE_VERTEXAI",
        "GOOGLE_CLOUD_PROJECT",
        "GOOGLE_CLOUD_LOCATION",
    ]
    missing = [key for key in required_env if not os.environ.get(key)]
    if missing:
        reason = "Missing required env vars for live ADK eval: " + ", ".join(missing)
        logger.warning("Skipping ADK eval test: %s", reason)
        pytest.skip(reason)

    eval_set = EvalSet.model_validate_json(EVALSET_PATH.read_text())
    eval_config = EvalConfig.model_validate_json(EVAL_CONFIG_PATH.read_text())

    await AgentEvaluator.evaluate_eval_set(
        agent_module="footy_finder",
        eval_set=eval_set,
        eval_config=eval_config,
        num_runs=1,
        print_detailed_results=True,
    )
