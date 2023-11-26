import taipy as tp
from taipy import Gui, Config, Core
from datetime import datetime
from openai import OpenAI
import os
from dotenv import load_dotenv, dotenv_values
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
    return state.calc_trip_length(state.start_date, state.end_date)

def gptPromptCreation(state):
    return f"Create an itinerary for a trip to {state.Destination} for {calc_trip_length(state.start_date, state.end_date)} days.There are {state.num_adults} adults and {state.num_kids} children going. Please include times of day in the itinerary. Please include the hyperlinks to any relevant info (like restaurants) in the response. Also please restate my inputs. "


def submit_scenario(state):
    
    print(gptPromptCreation(state))

    state.scenario.test_info.write(prompt(message=gptPromptCreation(state),model="gpt-4-1106-preview"))

    state.scenario.submit(wait=True)

    state.message = scenario.message.read()

def on_action(state, id):
    notify(state, "info", "Your trip will be planned shortly...")
    invoke_long_callback(state, submit_scenario(state), [state])


stylekit = {
  "color_primary": "#b3465f",
  "color_secondary": "#b3465f",
  "color_background_dark": "#525151",
  "color_background_light": "#d4cdcd", 
  "color_paper_dark": "#b3465f"
  
}


section_1 = """ 
###<center>WIZEWAY</center>
"""

section_2 = """

<center>Let's start find some fun activities for your trip!!</center>
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

<center><|Generate Itinerary|button|on_action=submit_scenario|></center>

<center>Here Is Your Itinerary!!:</center> 
<br/>
<center><|{message}|text|></center>

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
  Gui(page = section_1+section_2+section_3).run(dark_mode=True)
