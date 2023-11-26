import taipy as tp
from taipy import Gui, Config, Core
from datetime import datetime
from taipy.gui import State, invoke_long_callback, notify
import magic as img

###################
    #Definitions#
###################

template = ("Trip Length:\nLocation:\nDay 1:\n(Activity Name)" + 
    "\n(Activity Location and Time)\n(Activity Description)\n\n" +
"(Activity Name)\n(Activity Location and Time)\n(Activity Description)\n\n" +
".\n.\n.\n.\n\n" + "Day x:\n(Activity Name)\n(Activity Location)\n(Activity Description)")

def calc_trip_length(start_date, end_date):
    
    timediff = end_date - start_date
    return timediff.days

def check_trip_length(state):
    
    trip_durr = calc_trip_length(state.start_date, state.end_date)
    
    if trip_durr < 0 or trip_durr > 30:
        return f"Please make sure that the trips End Date is not before the End Date!!\nAlso Please Restrict the trip timeline to a month."
    
    elif trip_durr >=7:
        return f"Please split up the trip by weeks in order to make sure that a more accurate answer if given"

    else:
      return


def build_message(test_info: str):
    return test_info

input_test_info_data_node_cfg = Config.configure_data_node(id="test_info")
message_data_node_cfg = Config.configure_data_node(id="message")
build_msg_task_cfg = Config.configure_task("build_msg", build_message, input_test_info_data_node_cfg, message_data_node_cfg)
scenario_cfg = Config.configure_scenario("scenario", task_configs=[build_msg_task_cfg])


def submit_scenario(state):
    
    state.scenario.test_info.write(state.check_trip_length(state))

    state.scenario.submit(wait=True)

    state.message = scenario.message.read()

def on_action(state, id):
    notify(state, "info", "Your trip will be planned shortly...")
    invoke_long_callback(state, submit_scenario(state), [state])

#Markdown representation of the UI


page = """

<|{"wizebanner.png"}|image|>

Where are you going?  <|{Destination}|input|>

Planning on bringing pets: <|{bool_pets}|toggle|lov=Item 1;Item 2;Item 3|>

Travellers over 18: <|{num_adults}|number|>

Travellers under 18: <|{num_adults}|number|>

Trip start date: <|{start_date}|date|>

Trip end date: <|{end_date}|date|>

Do you have any special interests? <|{interests}|input|>

<|submit|button|on_action=submit_scenario|>

Message: <|{message}|text|>


"""


Destination = None
message = None
start_date = None
end_date = None


if __name__ == "__main__":
    
    tp.Core().run()
    scenario = tp.create_scenario(scenario_cfg)
    tp.Gui(page).run(dark_mode=True)
