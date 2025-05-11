import streamlit as st
from crewai import Crew
from textwrap import dedent

from Agents_def import TripAgents
from tasks import TripTasks
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TripCrew:
    def __init__(self, origin, city, customer_interest_topic, date_range):
        self.city = city
        self.origin = origin
        self.customer_interest_topic=customer_interest_topic
        self.date_range = date_range

    def run(self):
        agents = TripAgents()
        tasks = TripTasks()

        customer_interest_search_agent = agents.customer_interest_search_agent()
        local_expert_agent = agents.local_expert()
        travel_concierge_agent = agents.travel_concierge()

        customer_interest_search_task = tasks.customer_interest_search_tasks(
            customer_interest_search_agent,
            self.city,
            self.customer_interest_topic,
        )
        trip_info_task = tasks.trip_info(
            local_expert_agent,
            self.city,
            self.date_range,
        )
        plan_task = tasks.plan_task(
            travel_concierge_agent, 
            self.origin,
            self.city,
            self.date_range,
        )

        
        crew = Crew(
            agents=[customer_interest_search_agent, local_expert_agent, travel_concierge_agent],
            tasks=[customer_interest_search_task, trip_info_task, plan_task],
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
    customer_interest_topic = st.text_input("Do you have any specific interests or hobbies you'd like to pursue during your visit to the city?", placeholder="Best coffee shop or street food")
    date_range = st.text_input("What is the date range you are interested in traveling?", placeholder="Enter the date range (e.g., 2024-09-15 to 2024-09-25)")
    
    # Button to trigger the trip plan
    if st.button("Plan My Trip"):
        if location and city and date_range:
            # Initialize TripCrew
           
            trip_crew = TripCrew(location, city, customer_interest_topic, date_range)
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
