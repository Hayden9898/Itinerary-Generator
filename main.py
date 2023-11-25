import taipy as tp
from taipy import Gui, Config, Core
from datetime import datetime
from openai import OpenAI

#ChatGpt initialization





def stream(message: str, model: str):
  stream = client.chat.completions.create(
    model=model,
    messages = [
      {"role": "system", "content": "You are an AI assistant. You will answer questions, and you are an expert writer."},
      {"role": "user", "content": message},
    ],
    stream=True,
  )
  for part in stream:
    print(part.choices[0].delta.content or "", end="")


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

def submit_scenario(state):
    
    state.scenario.test_info.write(get_days(state))

    state.scenario.submit(wait=True)

    state.message = scenario.message.read()


def gptPromptCreation():

    return f"Create an itinerary for a trip to {Destination} for {calc_trip_length(start_date, end_date)} days.\
          There are {num_adults} adults and {num_kids} children going. Along with places to eat, and good photo taking opportunities."

#Markdown representation of the UI


page = """

Where are you going?  <|{Destination}|input|>

Planning on bringing pets: <|{bool_pets}|toggle|lov=Item 1;Item 2;Item 3|>

Travellers over 18: <|{num_adults}|number|>

Travellers under 18: <|{num_kids}|number|>

Trip start date: <|{start_date}|date|>

Trip end date: <|{end_date}|date|>

<|submit|button|on_action=submit_scenario|>

Message: <|{message}|text|>


"""
Destination = "ajit is sexy"
message = None
start_date = datetime.now()
end_date = datetime.now()
num_adults = 0
num_kids = 0 


stream(message="", model="gpt-4-1106-preview")

if __name__ == "__main__":
    tp.Core().run()
    scenario = tp.create_scenario(scenario_cfg)
    tp.Gui(page).run(dark_mode=True)
