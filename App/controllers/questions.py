def get_default_questionnaire():
    default_questions = [
        {
            "id": "Q1",
            "text": "Q1. Please describe your current health condition.",
            "type": "long_answer",
            "conditional_on": True
        },
        {
            "id": "Q2",
            "text": "Q2. Do you have Diabetes (Sugar)?",
            "type": "boolean",
            "follow_ups": [
                {
                    "id": "Q2a",
                    "text": "For how long?",
                    "type": "long_answer",
                    "conditional_on": True
                }
            ]
        },
        {
            "id": "Q3",
            "text": "Q3. Do you have hypertension (high blood pressure)?",
            "type": "boolean",
            "follow_ups": [
                {
                "id": "Q3a",
                "text": "Is your condition managed (treated) [controlled] by Diet / Tablets ",
                "type": "long_answer",
                "conditional_on": True
                }
            ]
        },
        {
            "id": "Q4",
            "text": "Q4. Do you have high cholesterol?",
            "type": "boolean",
            "follow_ups": [
                {
                    "id": "Q4a",
                    "text": "Are you on medication?",
                    "type": "boolean",
                    "conditional_on": True
                }
            ]
        },
        {
            "id": "Q5",
            "text": "Q5. Have you ever had a myocardial infarction (heart attack)?",
            "type": "boolean",
            "follow_ups": [
                {
                    "id": "Q5a",
                    "text": "How long ago?",
                    "type": "long_answer",
                    "conditional_on": True
                }
            ]
        },
        {
            "id": "Q6",
            "text": "Q6. Do you have ischaemic heart disease (angina)?",
            "type": "boolean",
            "follow_ups": [
                {
                    "id": "Q6a",
                    "text": "For how long?",
                    "type": "long_answer",
                    "conditional_on": True
                }
            ]
    
        },
         {
            "id": "Q7",
            "text": "Q7. Did you ever have a stroke or TIA?",
            "type": "boolean",
            "follow_ups": [
                {
                "id": "Q7a",
                "text": "How long?",
                "type": "long_answer",
                "conditional_on": True
                }

            ]
        },
         {
            "id": "Q8",
            "text": "Q8. Do you have heart failure? ",
            "type": "boolean",
            "follow_ups": [
                {
                    "id": "Q8a",
                    "text": "How long? ",
                    "type": "long_answer",
                    "conditional_on": True
                }
            ]
        } 
        
    ]
    return default_questions