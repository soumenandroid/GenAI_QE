from crewai import Task
from textwrap import dedent
from datetime import date

class TripTasks:

    def customer_interest_search_tasks(self, agent, city, customer_interest_topic):
        return Task(
            description=dedent(f"""
                Get the top 3 places searching the internet.
                Search query: "Best places to fulfill {customer_interest_topic} in {city}"
                
            """),
            agent=agent,
            expected_output=f"The top 3 places to fulfill customer interest topic in the city"
        )

    def trip_info(self, agent, city, date_range):
        return Task(
            description=dedent(f"""
                Identify to 5 tourist attractions of the destination city 
                on that trip date range.
                
                Trip Date: {date_range}
                destination city: {city}
            """),
            agent=agent,
            expected_output="Comprehensive city guide of the city"
        )

    def plan_task(self, agent, origin, city, date_range):
        return Task(
            description=dedent(f"""
                Expand this guide into a full 7-day travel itinerary, packing suggestions, 
                and a budget breakdown.
                                
                Trip Date: {date_range}
                Traveling from: {origin}
                destination city: {city}
            """),
            agent=agent,
            expected_output="Complete expanded travel plan with daily schedule and budget breakdown"
        )

    