# backend/app/utils/validators.py

from datetime import datetime

def validate_date(date_text, date_format="%Y-%m-%d"):
    """
    Validates that a string is a valid date in the given format.
    Returns a datetime.date object if valid, else raises ValueError.
    """
    try:
        return datetime.strptime(date_text, date_format).date()
    except ValueError as e:
        raise ValueError(f"Invalid date format: {date_text}. Expected format: {date_format}") from e

def validate_non_empty_string(value, field_name="Field"):
    """
    Validates that a given value is a non-empty string.
    """
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")

def validate_positive_integer(value, field_name="Field"):
    """
    Validates that a given value is a positive integer.
    """
    if not isinstance(value, int) or value <= 0:
        raise ValueError(f"{field_name} must be a positive integer.")

def validate_coordinates(latitude, longitude):
    """
    Validates that latitude and longitude are within valid ranges.
    """
    if not (-90 <= latitude <= 90):
        raise ValueError("Latitude must be between -90 and 90 degrees.")
    if not (-180 <= longitude <= 180):
        raise ValueError("Longitude must be between -180 and 180 degrees.")
