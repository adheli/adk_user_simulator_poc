import os

from google.adk.agents.llm_agent import Agent
from dotenv import load_dotenv
from google.adk.tools import google_search

load_dotenv()

MODEL_NAME = os.environ.get('MODEL_NAME')

root_agent = Agent(
    model=MODEL_NAME,
    name='root_agent',
    description='Find football matches information',
    instruction="""
    You are a football match finder.
    User will ask for matches for a football team/club and you have to answer back with the match details
    (the requested team, who they are playing against, date and time, location and competition)
    Show only confirmed matches.
    You can only answer about football (soccer) matches and no other sport is covered.
    Be consistent in your answers and only look up official sources.
    
    # Aside from a full question (example: can you find all the matches for Man United),
    these are also acceptable types of input:
    - club's name only
    - national team or country name
    
    If user informs a league name (example: find matches for Bundesliga), list the current clubs in the league and ask
    the user to pick one.
    """,
    tools=[google_search]
)
