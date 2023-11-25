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

def calc_trip_length(state):
    
    timediff = state.end_date - state.start_date
    return timediff.days

def check_trip_length(state):
    
    trip_durr = calc_trip_length(state.start_date, state.end_date)
    
    if trip_durr < 0 or trip_durr > 30:
        return f"Please make sure that the trips End Date is not before the End Date!!\nAlso Please Restrict the trip timeline to a month."
    
    elif trip_durr >=7:
        return f"Please split up the trip by weeks in order to make sure that a more accurate answer if given"
   



def build_message(test_info: str):
    return f"Your trip is {test_info} days long!"

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
    
    state.scenario.test_info.write(get_days(state))

    state.scenario.submit(wait=True)

    state.message = scenario.message.read()


def gptPromptCreation(state):
  verify_num_adults(state.num_adults)
  verify_num_kids(state.num_kids)
  check_trip_length(state.start_date, state.end_date)
  

  
  return f"Create an itinerary for a trip to {state.Destination} for {calc_trip_length(state.start_date, state.end_date)} days.\
          There are {state.num_adults} adults and {state.num_kids} children going. Along with places to eat, and good photo taking opportunities."

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
