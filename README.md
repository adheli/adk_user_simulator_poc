# ADK User Simulator PoC

Proof of concept for evaluating a Google ADK agent with recorded conversations and user-simulator scenarios.

The repository contains a single football match finder agent, `footy_finder`, plus evaluation assets that exercise both direct fixture lookup behavior and simulated multi-turn user interactions.

## Agent

`footy_finder` is an ADK `Agent` that helps users find confirmed football (soccer) matches.

The agent is configured in `footy_finder/agent.py` with:

- `google_search` as its only tool
- `MODEL_NAME` loaded from the environment
- instructions to answer only football match questions
- a requirement to use official sources and show only confirmed matches
- support for short inputs such as a club name, national team, or country name
- league-name handling that asks the user to pick a club from the league

Expected match responses include the requested team, opponent, date and time, location, and competition when available.

## Repository Layout

```text
.
├── footy_finder/
│   ├── agent.py                         # ADK root agent
│   ├── eval_config.json                 # ADK eval criteria and user simulator config
│   ├── eval_set_1.evalset.json          # Recorded conversation eval case
│   ├── eval_set_with_scenarios.evalset.json
│   │                                    # Scenario-based user simulator eval cases
│   ├── sample_conversations.json        # Source scenario definitions
│   └── session.json                     # Sample ADK session input
├── pyproject.toml                       # Python dependencies
├── uv.lock                              # Locked dependency graph
└── README.md
```

## Requirements

- Python 3.12 or newer
- `uv`
- Google ADK with eval support, installed from `pyproject.toml`
- Google Cloud / Vertex AI access if `GOOGLE_GENAI_USE_VERTEXAI=true`

Create `footy_finder/.env` with the required runtime settings:

```bash
GOOGLE_GENAI_USE_VERTEXAI=true
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=your-location
MODEL_NAME=your-agent-model
```

The local `.env` file is loaded by `python-dotenv` from `footy_finder/agent.py`.

## Install

```bash
uv sync
```

## Run Locally

Start the ADK web playground from the repository root:

```bash
uv run adk web .
```

Then select the `footy_finder` app in the ADK UI.

Example prompts:

```text
get me Brazil matches
bayern
premier league
```

## Evaluations

The repository includes two evalsets.

### Recorded Conversation Eval

`footy_finder/eval_set_1.evalset.json` contains one eval case, `get_me_matches`, with a recorded conversation covering:

- Brazil national team match lookup
- Bayern Munich match lookup from a short club-name input
- Premier League league-name handling, where the agent lists clubs and asks the user to choose one

### Scenario-Based User Simulator Eval

`footy_finder/eval_set_with_scenarios.evalset.json` contains three scenario-driven eval cases:

- `27ddaf7b`: novice user asks for Premier League matches for Manchester United
- `b7a30b86`: expert user asks for Liverpool matches, England matches, and then the current Premier League table
- `2be83af7`: rushed user asks for non-soccer schedules first, then asks for a soccer team

These scenarios are designed to test multi-turn behavior, clarification handling, refusal or boundary behavior for unsupported sports, and whether the agent stays within its football-match-finder scope.

### Eval Configuration

`footy_finder/eval_config.json` enables:

- `hallucinations_v1` with a `0.5` threshold and intermediate natural-language response evaluation
- `safety_v1` with a `0.8` threshold
- a user simulator powered by `gemini-2.5-flash`
- up to `20` simulator invocations per eval case

Run evals from the repository root:

```bash
uv run adk eval footy_finder footy_finder/eval_set_1.evalset.json --config_file_path footy_finder/eval_config.json
uv run adk eval footy_finder footy_finder/eval_set_with_scenarios.evalset.json --config_file_path footy_finder/eval_config.json
```

## Current Scope and Limitations

- The agent only covers football/soccer match information.
- It uses live Google Search, so answers may vary as fixtures and official pages change.
- It does not have a dedicated football data API; source quality depends on search results and the model following the official-source instruction.
- League table requests are outside the main instruction, which focuses on match details. The scenario eval intentionally probes this boundary.
- Non-soccer sports such as rugby and baseball should be treated as unsupported.

## Development Notes

The project dependencies are declared in `pyproject.toml`, including `google-adk[eval]`, `google-cloud-aiplatform[evaluation]`, `pytest`, `fastapi`, and `uvicorn`.

There are currently no unit tests in the repository. Behavioral validation is represented by the ADK evalsets under `footy_finder/`.
