# backend/app/services/suggestions.py

def get_suggestions(user_input, place_data):
    suggestions = []
    for place in place_data:
        if user_input.lower() in place.name.lower():
            suggestions.append(place)
    return suggestions
