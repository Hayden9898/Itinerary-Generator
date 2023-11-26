import taipy as tp
from taipy import Gui, Config, Core
from datetime import datetime
from openai import OpenAI
import os
from dotenv import load_dotenv, dotenv_values
import magic as img

load_dotenv()
stylekit = {
  "color_primary": "#d4cdcd",
  "color_secondary": "#b3465f",
  "color_background_dark": "#525151",
  "color_background_light": "#b3465f",
  "color_paper_dark": "#b3465f"

}


# Gui.run(stylekit=stylekit)
#ChatGpt initialization

# Our_key =os.getenv('OPENAI_API_KEY')

# client = OpenAI(api_key=Our_key,
#                 organization="org-XFRiKEA3bXXTSifH2T4XNFwX")


# def prompt(message: str, model: str):

#     completion = client.chat.completions.create(
#     model=model,
#     messages=[
#         {"role": "system", "content": "You are an AI Itinerary planner assistant. You will plan itineraries based on input given to you, and you scan the latest events/attractions for the itinerary."},
#         {"role": "user", "content": message}
#     ]
#     )
#     print(completion.choices[0].message.content)

    

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
    return f"Your trip is {test_info} days long!"

input_test_info_data_node_cfg = Config.configure_data_node(id="test_info")
message_data_node_cfg = Config.configure_data_node(id="message")
build_msg_task_cfg = Config.configure_task("build_msg", build_message, input_test_info_data_node_cfg, message_data_node_cfg)
scenario_cfg = Config.configure_scenario("scenario", task_configs=[build_msg_task_cfg])

def get_days(state):
    return state.calc_trip_length(state.start_date, state.end_date)

def gptPromptCreation():

    return f"Create an itinerary for a trip to {Destination} for 2 days.\
          There are {num_adults} adults and {num_kids} children going. Along with places to eat, and good photo taking opportunities. \
          Please include times of day in the itinerary. Please include the links to any relevant info (like restaurants) in the response. "


def submit_scenario(state):
    
    state.scenario.test_info.write(get_days(state))

    state.scenario.submit(wait=True)

    state.message = scenario.message.read()

#Markdown representation of the UI


section_1 = """ 
<br/>
<center> <|{"wizebannerwhitepng.png"}|image|> </center>


"""

section_2 = """

<center>Let's find some fun activities for your trip!!</center>
<br/>
<h4><center>Where do you plan on going?</center></h4> 
<br/>

<center><|{Destination}|input|></center>


<|layout|columns=5 5|
<|



<br/>
<h4><center>Number of Travellers over 18:</center></h4>
<center><|{num_adults}|number|></center>

<br/>
<h4><center>Trip start date:</center></h4>
<center><|{start_date}|date|></center>
|>

<|

<br/>
<h4><center>Travellers under 18:</center></h4>
<center><|{num_kids}|number|></center>
<br/>
<h3><center>Trip end date:</center></h3> 
<center><|{end_date}|date|></center>

|>
|>
"""

section_3 = """

<h4><center>Do you have any extra interests/requests?</center></h4>
<br/>
<center><|{interests}|input|></center>
<br/>


<center><|Generate Itinerary|button|on_action=submit_scenario|></center>

<br/>
<center><|{message}|text|></center>

<center> <|{data}|table|> </center>

"""
###Test Information, can be changed


Destination = "italy"
message = None
start_date = datetime.now()
end_date = datetime.now()
num_adults=2
num_kids=2
bool_pets=None

# prompt(message=gptPromptCreation(),model="gpt-4-1106-preview" )


# if __name__ == "__main__":
#     tp.Core().run()
#     scenario = tp.create_scenario(scenario_cfg)
#     tp.Gui(page).run(dark_mode=True)

if __name__ == "__main__":
    gui = Gui(page = section_1+section_2+section_3+section_4)
    scenario = tp.create_scenario(scenario_cfg)
    gui.run(stylekit=stylekit)
