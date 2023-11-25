import taipy as tp
from taipy import Gui, Config, Core
from datetime import datetime
from openai import OpenAI
import os
from dotenv import load_dotenv, dotenv_values

load_dotenv()

#ChatGpt initialization

Our_key =os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=Our_key,
                organization="org-XFRiKEA3bXXTSifH2T4XNFwX")


def prompt(message: str, model: str):

    completion = client.chat.completions.create(
    model=model,
    messages=[
        {"role": "system", "content": "You are an AI Itinerary planner assistant. You will plan itineraries based on input given to you, and you scan the latest events/attractions for the itinerary."},
        {"role": "user", "content": message}
    ]
    )
    return (completion.choices[0].message.content)



###################
    #Definitions#
###################

def calc_trip_length(start_date, end_date):
    
    timediff = end_date - start_date
    return timediff.days

def check_trip_length(trip_dur):
    if trip_dur < 0 or trip_dur > 30:
        return -1
    
    elif trip_dur >=7:
        return 1
    
    else:
        return 2


def build_message(test_info: str):
    return f"{test_info}"

input_test_info_data_node_cfg = Config.configure_data_node(id="test_info")
message_data_node_cfg = Config.configure_data_node(id="message")
build_msg_task_cfg = Config.configure_task("build_msg", build_message, input_test_info_data_node_cfg, message_data_node_cfg)
scenario_cfg = Config.configure_scenario("scenario", task_configs=[build_msg_task_cfg])

def get_days(state):
    return state.calc_trip_length(state.start_date, state.end_date)

def get_num_Adults(state):
    return state.num_adults

def get_num_Kids(state):
    return state.num_kids

def verify_num_adults(num_adults):
    # Initialize the verification flag to False
    verification = False

    # Continue the loop until verification is True
    while not verification:
        try:
            # Attempt to convert the input to a float
            num_adults = float(num_adults)

            # Check if the input is a non-negative number
            if num_adults >= 0:
                # If valid, set verification to True and return the number of adults
                verification = True
                return num_adults
            else:
                # If not valid, return an error message
                return "Please enter a non-negative number"
        except ValueError:
            # If the conversion to float fails, return an error message
            return "Please enter a number"

def verify_num_kids(num_kids):
    # Initialize the verification flag to False
    verification = False

    # Continue the loop until verification is True
    while not verification:
        try:
            # Attempt to convert the input to a float
            num_kids = float(num_kids)

            # Check if the input is a non-negative number
            if num_kids >= 0:
                # If valid, set verification to True and return the number of kids
                verification = True
                return num_kids
            else:
                # If not valid, return an error message
                return "Please enter a non-negative number"
        except ValueError:
            # If the conversion to float fails, return an error message
            return "Please enter a number"
 
def get_days(state):
    return state.calc_trip_length(state.start_date, state.end_date)

def gptPromptCreation():

    return f"Create an itinerary for a trip to {Destination} for 1 days.\
          There are {num_adults} adults and {num_kids} children going. Along with places to eat, and good photo taking opportunities. \
          Please include times of day in the itinerary. Please include the hyperlinks to any relevant info (like restaurants) in the response. Do this in 100 words. "


def submit_scenario(state):
    
    state.scenario.test_info.write(prompt(message=gptPromptCreation(),model="gpt-4-1106-preview"))

    state.scenario.submit(wait=True)

    state.message = scenario.message.read()

#Markdown representation of the UI

page = """

Where are you going?  <|{Destination}|input|>

Planning on bringing pets: <|{bool_pets}|toggle|lov=Yes;No|>

Travellers over 18: <|{num_adults}|number|>

Travellers under 18: <|{num_kids}|number|>

Trip start date: <|{start_date}|date|>

Trip end date: <|{end_date}|date|>

<|Generate Itinerary|button|on_action=submit_scenario|>

Message: <|{message}|text|>


"""
###Test Information, can be changed

Destination = None
message = None
start_date = datetime.now()
end_date = datetime.now()
num_adults=2
num_kids=2
bool_pets=None


if __name__ == "__main__":
    tp.Core().run()
    scenario = tp.create_scenario(scenario_cfg)
    tp.Gui(page).run(dark_mode=True)