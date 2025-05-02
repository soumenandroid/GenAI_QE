import streamlit as st
from crewai import Crew
from textwrap import dedent
from Agents import TripAgents
from tasks import TripTasks
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TripCrew:
    def __init__(self, origin, city, date_range):
        self.city = city
        self.origin = origin
        self.date_range = date_range

    def run(self):
        agents = TripAgents()
        tasks = TripTasks()

        city_selector_agent = agents.city_selection_agent()
        local_expert_agent = agents.local_expert()
        travel_concierge_agent = agents.travel_concierge()

        weather_tasks = tasks.weather_forecast(
            city_selector_agent,
            self.city,
            self.date_range
        )
        trip_info_task = tasks.trip_info(
            local_expert_agent,
            self.city,
            self.date_range
        )
        plan_task = tasks.plan_task(
            travel_concierge_agent, 
            self.origin,
            self.city,
            self.date_range
        )

        
        crew = Crew(
            agents=[city_selector_agent, local_expert_agent, travel_concierge_agent],
            tasks=[weather_tasks, trip_info_task, plan_task],
            verbose=True
        )

        result = crew.kickoff()
        return result

# Streamlit app function
def trip_planner_app():
    st.title("Requirement Analysis Agent")
    
    # Input from the user
    location = st.text_input("From where will you be traveling from?", placeholder="Enter your origin location")
    city = st.text_input("Which place are you interested in visiting?", placeholder="Enter your destination city")
    date_range = st.text_input("What is the date range you are interested in traveling?", placeholder="Enter the date range (e.g., 2024-09-15 to 2024-09-25)")
    
    # Button to trigger the trip plan
    if st.button("Plan My Trip"):
        if location and city and date_range:
            # Initialize TripCrew
            trip_crew = TripCrew(location, city, date_range)
            st.write("Running the trip planner...")
            
            # Run the trip planning process and get the result
            result = trip_crew.run()
            
            # Display the result
            st.write("### Here is your Trip Plan")
            st.write(result)
        else:
            st.warning("Please fill in all fields to plan your trip.")

# Main function to run the app
if __name__ == "__main__":
    trip_planner_app()
