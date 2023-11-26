import taipy as tp
from taipy import Gui, Config, Core
from datetime import datetime
from openai import OpenAI
import os
from dotenv import load_dotenv
from taipy.gui import State, invoke_long_callback, notify, Markdown, Html

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


def get_formatted_itinerary(itinerary):
    formatted_str = ""

    # Split the itinerary into days
    days = itinerary.split('**')

    # Iterate through each day and add content to the formatted string
    
    for day in days:
        if day.strip():  # Check if the day is not empty
            # Split the day into activities
            activities = day.split('-')

            # Add the day as a heading to the formatted string
            formatted_str += activities[0].strip() + '\n'

            # Add each activity to the formatted string
            for activity in activities[1:]:
                formatted_str += f"  - {activity.strip()}\n"

    return formatted_str

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
          Please include times of day in the itinerary. Do it in less than 150 words. If the destination indicated is not a real place on earth, only output: 'Error'. After every completed day add 2 new lines (enters)."

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
    notify(state, "info", "Error: Please Enter Values")
    invoke_long_callback(state, submit_scenario(state), [state])





#Markdown representation of the UI

stylekit = {
  "color_primary": "#d48002",
  "color_secondary": "#d48002",
  "color_background": "#690f85",
  "color_paper_dark": "#690f85"
  
}


section_1 = """ 
<br/>
<center> <|{"wizebanner_big.png"}|image|> </center>

"""

section_2 = """

<center>Planning made easy™ </center>
<br/>
<br/>
<center>Where do you plan on going?</center> 
<br/>

<center><|{Destination}|input|></center>


<|layout|columns=5 5|
<|



<br/>
<center>Number of Travellers over 18:</center>
<center><|{num_adults}|number|></center>

<br/>
<center>Trip start date:</center> 
<center><|{start_date}|date|></center>
|>

<|

<br/>
<center>Travellers under 18:</center>
<center><|{num_kids}|number|></center>
<br/>
<center>Trip end date:</center> 
<center><|{end_date}|date|></center>

|>
|>
"""

section_3 = """

<center>Do you have any extra interests/requests?</center> 
<br/>
<center><|{interests}|input|></center>
<br/>


<center><|Generate Itinerary|button|on_action=submit_scenario|></center>

<br/>
<center><|{message}|text|> </center>
{: .output }

<br/>
<br/>



"""

section_4 = """

<|layout|columns=5  5|
<|

<center> <|{"wizecabin_color.png"}|image|> </center>
|>


<|
<center> <|{"campfirecolor.png"}|image|> </center>
|>

|>


<|card|
<center>WiseWay</center>

"""
###Test Information, can be changed

Destination = None
message = None
start_date = None
end_date = None
num_adults=None
num_kids=None
bool_pets=None
interests = None



if __name__ == "__main__":
    tp.Core().run()
    scenario = tp.create_scenario(scenario_cfg)
    Gui(page = section_1+section_2+section_3+section_4, css_file="./main.css").run(stylekit=stylekit)

#behrad's
