import taipy as tp
from taipy import Gui, Config, Core
from datetime import datetime
from openai import OpenAI
import os
from dotenv import load_dotenv
from taipy.gui import State, invoke_long_callback, notify

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
    return calc_trip_length(state.start_date, state.end_date)

def gptPromptCreation(state):
    return f"Create an itinerary for a trip to {state.Destination} for {get_days(state)+1} days.\
        There are {state.num_adults} adults and {state.num_kids} children going. Please keep in mind these notes: {state.interests}. \
          Please include times of day in the itinerary. Please include the hyperlinks to any relevant info (like restaurants) in the response. Do it in less than 150 words. If the destination indicated is not a real place on earth, only output: 'Error'"

def verify_num_adults(state):
    # Initialize the verification flag to False
    verification = False

    # Continue the loop until verification is True
    while not verification:
        try:
            # Attempt to convert the input to a float
            state.num_adults = float(state.num_adults)

            # Check if the input is a non-negative number
            if state.num_adults >= 0:
                # If valid, set verification to True and return the number of adults
                verification = True
                return state.num_adults
            else:
                # If not valid, return an error message
                return "Please enter a non-negative number"
        except ValueError:
            # If the conversion to float fails, return an error message
            return "Please enter a number"

def verify_num_kids(state):
    # Initialize the verification flag to False
    verification = False

    # Continue the loop until verification is True
    while not verification:
        try:
            # Attempt to convert the input to a float
            state.num_kids = float(state.num_kids)

            # Check if the input is a non-negative number
            if state.num_kids >= 0:
                # If valid, set verification to True and return the number of kids
                verification = True
                return state.num_kids
            else:
                # If not valid, return an error message
                return "Please enter a non-negative number"
        except ValueError:
            # If the conversion to float fails, return an error message
            return "Please enter a number"
 

def submit_scenario(state):
    
    gpt_output = prompt(message=gptPromptCreation(state),model="gpt-4-1106-preview")

    if(gpt_output=="Error"):
        gpt_output = "That is not a real destination, please re-enter. "

    state.scenario.test_info.write(gpt_output)

    state.scenario.submit(wait=True)

    state.message = scenario.message.read()

def on_action(state, id):
    notify(state, "info", "Your trip will be planned shortly...")
    invoke_long_callback(state, submit_scenario(state), [state])

#Markdown representation of the UI

page = """

Where are you going?  <|{Destination}|input|>

Planning on bringing pets: <|{bool_pets}|toggle|lov=Yes;No|>

Travellers over 18: <|{num_adults}|number|> 

Travellers under 18: <|{num_kids}|number|>

Trip start date: <|{start_date}|date|>

Trip end date: <|{end_date}|date|>

Any special interests or instructions (for example, do you have any pets?): <|{interests}|input|>

<|Generate Itinerary|button|on_action=submit_scenario|>

Itinerary: <|{message}|text|>


"""
###Test Information, can be changed

Destination = None
message = None
start_date = None
end_date = None
num_adults=None
num_kids=None
bool_pets=None

if __name__ == "__main__":
    tp.Core().run()
    scenario = tp.create_scenario(scenario_cfg)
    tp.Gui(page).run(dark_mode=True)