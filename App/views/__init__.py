from .admin import admin_views
from .user import user_views
from .index import index_views
from .auth import auth_views
from .questionnaire import questionnaire_views
from .patient import patient_views
from .doctor import doctor_views
from .anesthesiologist import anesthesiologist_views


views = [user_views, index_views, auth_views, questionnaire_views, patient_views, doctor_views, anesthesiologist_views, admin_views] 

