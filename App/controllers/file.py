def get_default_questionnaire():
    default_questions = [
        {
            "id": "q1",
            "text": "Please describe your current health condition.",
            "type": "long_answer",
            "follow_ups": []
        },
        {
            "id": "q2",
            "text": "Do you have any allergies?",
            "type": "multiple_choice",
            "choices": ["None", "Peanuts", "Shellfish", "Pollen", "Other"],
            "follow_ups": [
                {
                    "id": "q2a",
                    "text": "Please specify your other allergies.",
                    "type": "long_answer",
                    "conditional_on": "Other"
                }
            ]
        },
        {
            "id": "q3",
            "text": "Are you currently taking any medication?",
            "type": "boolean",
            "follow_ups": [
                {
                    "id": "q3a",
                    "text": "Please list the medications you are taking.",
                    "type": "long_answer",
                    "conditional_on": True
                }
            ]
        }
        # Add more default questions as required
    ]
    return default_questions