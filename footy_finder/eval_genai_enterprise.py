import json
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai.types import HttpOptions

# logger = logging.getLogger(__name__)

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from footy_finder.agent import footy_finder
else:
    from .agent import footy_finder

EXPERIMENT_NAME = 'footy-vertex-ai-eval'
AGENT_ID = 'footy_finder'

# not really working - seems to validate more the model than agent
def main():
    load_dotenv()

    project_id = os.environ.get('GOOGLE_CLOUD_PROJECT')
    location = os.environ.get('GOOGLE_CLOUD_LOCATION')

    print("Starting Gemini Enterprise AI evaluation client")
    client = genai.Client(project=project_id, location=location, http_options=HttpOptions(api_version="v1"))

    print("Loading evaluation dataset")
    eval_generated_dataset = json.loads(open('eval_set_with_scenarios.evalset.json').read())
    print("Loaded evaluation dataset:")
    print(eval_generated_dataset)


if __name__ == "__main__":
    main()
