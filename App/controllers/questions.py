def get_default_questionnaire():
    default_questions = [
        {
            "id": "q1",
            "text": "Please describe your current health condition.",
            "type": "long_answer",
            "conditional_on": True
        },
        {
            "id": "q2",
            "text": "Do you have Diabetes (Sugar)?",
            "type": "boolean",
            "follow_ups": [
                {
                    "id": "q2a",
                    "text": "For how long?",
                    "type": "long_answer",
                    "conditional_on": True
                }
            ]
        },
        {
            "id": "q3",
            "text": "Do you have hypertension (high blood pressure)?",
            "type": "boolean",
            "follow_ups": [
                {
                "id": "q3a",
                "text": "Is your condition managed (treated) [controlled] by Diet / Tablets ",
                "type": "long_answer",
                "conditional_on": True
                }
            ]
        },
        {
            "id": "q4",
            "text": "Do you have high cholesterol?",
            "type": "boolean",
            "follow_ups": [
                {
                    "id": "q4a",
                    "text": "Are you on medication?",
                    "type": "boolean",
                    "conditional_on": True
                }
            ]
        },
        {
            "id": "q5",
            "text": "Have you ever had a myocardial infarction (heart attack)?",
            "type": "boolean",
            "follow_ups": [
                {
                    "id": "q5a",
                    "text": "How long ago?",
                    "type": "long_answer",
                    "conditional_on": True
                }
            ]
        },
        {
            "id": "q6",
            "text": "Do you have ischaemic heart disease (angina)?",
            "type": "boolean",
            "follow_ups": [
                {
                    "id": "q6a",
                    "text": "For how long?",
                    "type": "long_answer",
                    "conditional_on": True
                }
            ]
    
        },
         {
            "id": "q7",
            "text": "Did you ever have a stroke or TIA?",
            "type": "boolean",
            "follow_ups": [
                {
                "id": "q7a",
                "text": "How long?",
                "type": "long_answer",
                "conditional_on": True
                }

            ]
        },
         {
            "id": "q8",
            "text": "Do you have heart failure? ",
            "type": "boolean",
            "follow_ups": [
                {
                    "id": "q8a",
                    "text": "How long? ",
                    "type": "long_answer",
                    "conditional_on": True
                }
            ]
        } 
        
    ]
    return default_questions