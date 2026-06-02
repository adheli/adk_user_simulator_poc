import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from vertexai import Client, types

# logger = logging.getLogger(__name__)

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from footy_finder.agent import root_agent
else:
    from .agent import root_agent

EXPERIMENT_NAME = 'footy-vertex-ai-eval'
AGENT_ID = 'footy_finder'


def main():
    load_dotenv()

    project_id = os.environ.get('GOOGLE_CLOUD_PROJECT')
    location = os.environ.get('GOOGLE_CLOUD_LOCATION')

    print("Starting Vertex AI evaluation client")
    client = Client(project=project_id, location=location)

    print("Generating evaluation dataset")
    eval_generated_dataset = client.evals.generate_conversation_scenarios(
        agent_info={
            "name": AGENT_ID,
            "root_agent_id": root_agent.name,
            "agents": {
                root_agent.name: {
                    "agent_id": root_agent.name,
                    "agent_type": "LlmAgent",
                    "description": root_agent.description,
                    "instruction": root_agent.instruction,
                }
            },
        },
        config={
            "count": 5,
            "generation_instruction": "Generate scenarios where a user asks for football matches scheduled for the "
                                      "current season.",
        },
        allow_cross_region_model=True
    )

    print("Generated evaluation dataset:")
    print(eval_generated_dataset)

    print("Run evaluation")
    eval_result = client.evals.evaluate(
        dataset=eval_generated_dataset,
        metrics=[
            types.RubricMetric.FINAL_RESPONSE_QUALITY,
            types.RubricMetric.TOOL_USE_QUALITY,
            types.RubricMetric.HALLUCINATION,
            types.RubricMetric.SAFETY,
        ]
    )

    print("Show the results")
    eval_result.show() # it doesn't show anything when running as python script, only works in Colab or Jupiter

    # print("Identify the top failure patterns in the results")
    # loss_clusters = client.evals.generate_loss_clusters(eval_result=eval_result)
    # loss_clusters.show()

    print("Automatically refine the system prompt to fix identified issues")
    optimize_result = client.optimizer.optimize(
        targets=["system_prompt"],
        benchmark=eval_result,
        tests=eval_generated_dataset
    )

    return {
        "eval_generated_dataset": eval_generated_dataset,
        # "traces": traces,
        "eval_result": eval_result,
        # "loss_clusters": loss_clusters,
        "optimize_result": optimize_result,
    }


if __name__ == "__main__":
    main()
