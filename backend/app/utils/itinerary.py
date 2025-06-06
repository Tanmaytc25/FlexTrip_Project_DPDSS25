# backend/app/utils/itinerary.py

from datetime import timedelta

def distribute_pois_across_days(pois, days):
    """
    Distributes POIs across the given number of days as evenly as possible.
    """
    if days <= 0:
        raise ValueError("Number of days must be positive.")

    daily_plan = [[] for _ in range(days)]
    for idx, poi in enumerate(pois):
        day_index = idx % days
        daily_plan[day_index].append(poi)

    return daily_plan

def calculate_trip_duration(start_date, end_date):
    """
    Calculates the number of days between two dates, inclusive.
    """
    if start_date > end_date:
        raise ValueError("Start date must be before end date.")
    return (end_date - start_date).days + 1

def format_itinerary(itinerary):
    """
    Formats the itinerary into a printable format or structure.
    """
    formatted = ""
    for day, pois in enumerate(itinerary, start=1):
        formatted += f"Day {day}:\n"
        for poi in pois:
            formatted += f"  - {poi}\n"
        formatted += "\n"
    return formatted
