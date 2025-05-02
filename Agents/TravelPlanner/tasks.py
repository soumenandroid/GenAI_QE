from crewai import Task
from textwrap import dedent
from datetime import date

class TripTasks:

    def weather_forecast(self, agent, city, range):
        return Task(
            description=dedent(f"""
                Check for weather forecast in destination city.
                destination city: {city}
                Trip Date: {range}
            """),
            agent=agent,
            expected_output="Detailed weather report on the chosen city "
        )

    def trip_info(self, agent, city, range):
        return Task(
            description=dedent(f"""
                Identify to 5 tourist attractions of the destination city 
                on that trip date range.
                
                Trip Date: {range}
                destination city: {city}
            """),
            agent=agent,
            expected_output="Comprehensive city guide of the city"
        )

    def plan_task(self, agent, origin, city, range):
        return Task(
            description=dedent(f"""
                Expand this guide into a full 7-day travel itinerary, packing suggestions, 
                and a budget breakdown.
                                
                Trip Date: {range}
                Traveling from: {origin}
                destination city: {city}
            """),
            agent=agent,
            expected_output="Complete expanded travel plan with daily schedule and budget breakdown"
        )

    