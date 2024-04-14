def get_default_questionnaire():
    default_questions = [
        {
            "id": "q0",
            "text": "Please describe your current health condition.",
            "type": "long_answer",
            "follow_ups": []
        },
        {
            "id": "q1",
            "text": "Do you have Diabetes (Sugar)?",
            "type": "boolean",
            "follow_ups": [
                {
                    "id": "q2a",
                    "text": "For how long?",
                    "type": "long_answer",
                    "conditional_on": "Other"
                }
            ]
        },
        {
            "id": "q2",
            "text": "Is your condition managed (treated) [controlled] by Diet / Tablets / Insulin",
            "type": "multiple_choice",
            "choices": ["Diet", "Tablets", "Insulin"],
        },
        {
            "id": "q3",
            "text": "What medication are you on?",
            "type": "long_answer",
        },
        {
            "id": "q4",
            "text": "Do you have hypertension (high blood pressure)?",
            "type": "boolean",
            "follow_ups": [
                {
                    "id": "q4a",
                    "text": "Is your condition managed (treated) [controlled] by Diet / Tablets ",
                    "type": "long_answer",
                    "conditional_on": True,
                }
            ]
        },
          {
            "id": "q5",
            "text": "What medication are you on for the hypertension?",
            "type": "long_answer",
            "conditional_on": True
        },
        {
            "id": "q6",
            "text": "Do you have high cholesterol?",
            "type": "boolean",
            "follow_ups": [
                {
                    "id": "q6a",
                    "text": "Are you on medication?",
                    "type": "boolean",
                }
            ]
        },
        {
            "id": "q7",
            "text": "Have you ever had a myocardial infarction (heart attack)?",
            "type": "boolean",
            "follow_ups": [
                {
                    "id": "q7a",
                    "text": "How long ago?",
                    "type": "long_answer",
                    "conditional_on": True
                }
            ]
        },
        {
            "id": "q8",
            "text": "Do you have ischaemic heart disease (angina)?",
            "type": "boolean",
            "follow_ups": [
                {
                    "id": "q8a",
                    "text": "For how long?",
                    "type": "long_answer",
                    "conditional_on": True
                }
            ]
    
        },
         {
            "id": "q9",
            "text": "Did you ever have a stroke or TIA?",
            "type": "boolean",
            "follow_ups": [
                {
                "id": "q9a",
                "text": "How long?",
                "type": "long_answer",
                "conditional_on": True
                }

            ]
        },
         {
            "id": "q10",
            "text": "Do you have heart failure? ",
            "type": "boolean",
            "follow_ups": [
                {
                    "id": "q10a",
                    "text": "How long? ",
                    "type": "long_answer",
                    "conditional_on": True
                }
            ]
        } 
        
        # Add more default questions as required
    ]
    return default_questions