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
        },
        {
            "id": "q4",
            "text": "Have you had any recent infections or illnesses?",
            "type": "boolean",
            "follow_ups": [
                {
                    "id": "q4a",
                    "text": "Please list them: ",
                    "type": "long_answer",
                    "conditional_on": True
                }
            ]
        },
          {
            "id": "q5",
            "text": "Do you have a history of substance abuse or addiction?",
            "type": "boolean",
            "follow_ups": []
        },
        {
            "id": "q6",
            "text": "Do you consume alcohol or recreational drugs?",
            "type": "boolean",
            "follow_ups": [
                {
                    "id": "q6a",
                    "text": "How often: ",
                    "type": "long_answer",
                    "conditional_on": True
                }
            ]
        },
        {
            "id": "q7",
            "text": "Do you smoke or use tobacco products?",
            "type": "boolean",
            "follow_ups": [
                {
                    "id": "q7a",
                    "text": "How often: ",
                    "type": "long_answer",
                    "conditional_on": True
                }
            ]
        },
        {
            "id": "q8",
            "text": "Have you had a cough or cold in the last 3 weeks? ",
            "type": "boolean",
            "follow_ups": []
    
        },
         {
            "id": "q9",
            "text": "Have you had an operation before?",
            "type": "boolean",
            "follow_ups": [
                {
                    "id": "q9a",
                    "text": "Last time: ",
                    "type": "long_answer",
                    "conditional_on": True
                }
            ]
        },
         {
            "id": "q10",
            "text": "Do you have recent heartburn or acid reflux? ",
            "type": "boolean",
            "follow_ups": [
                {
                    "id": "q10a",
                    "text": "Last time: ",
                    "type": "long_answer",
                    "conditional_on": True
                }
            ]
        },
         {
            "id": "q11",
            "text": "Do you wake up at night short of breath? ",
            "type": "boolean",
            "follow_ups": []
         },   
         {
            "id": "q12",
            "text": "Are you on dialysis?  ",
            "type": "boolean",
            "follow_ups": []
         },   
         {
            "id": "q13",
            "text": "Do you have epilepsy (fits)?",
            "type": "boolean",
            "follow_ups": [
                {
                    "id": "q13a",
                    "text": "Last time: ",
                    "type": "long_answer",
                    "conditional_on": True
                }
            ]
        },
        {
            "id": "q14",
            "text": "Additional Notes:",
            "type": "long_answer",
            "follow_ups": []
        }  
        
        # Add more default questions as required
    ]
    return default_questions