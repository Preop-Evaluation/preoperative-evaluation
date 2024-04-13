from flask import Blueprint, jsonify, request
from App.database import db
from App.models import Notification
from datetime import datetime

def create_notification(message, patient_id, title):
    try:
        new_notification = Notification(message, patient_id, title)
        db.session.add(new_notification)
        db.session.commit()
        return new_notification
    except Exception as e:
        print(e)
        db.session.rollback()
        return None    
    

def get_notifications_json():
    notifications = Notification.query.all()
    notifications_list = [notification.toDict() for notification in notifications]
    return jsonify({'notifications': notifications_list})

def get_notifications():
    notifications = Notification.query.all()
    return notifications

def get_notification(notification_id):
    notification = Notification.query.get_or_404(notification_id)
    return jsonify(notification.toDict())
     
def delete_notification(notification_id):
    notification = Notification.query.get(notification_id)
    db.session.delete(notification)
    db.session.commit()
    return jsonify({'message': 'Notification deleted successfully'})


def get_patient_notifications(patient_id):
    notifications = Notification.query.filter_by(patient_id=patient_id, seen=False).all()

    patient_notifications = sorted(notifications, key=lambda x: x.timestamp, reverse=True)
    notification_info = []

    for notification in patient_notifications:
        info = {
            'id': notification.id,
            'message': notification.message,  
            'title': notification.title,          
            'timestamp': notification.timestamp.strftime("%m/%d/%Y, %H:%M:%S")
        }

        time_ago = (datetime.now() - notification.timestamp).total_seconds()
        if time_ago < 60:
            info['time_ago'] = f"{int(time_ago)}s"
        elif time_ago < 3600:
            info['time_ago'] = f"{int(time_ago // 60)}m"
        elif time_ago < 86400:
            info['time_ago'] = f"{int(time_ago // 3600)}h"
        elif time_ago < 604800:
            info['time_ago'] = f"{int(time_ago // 86400)}d"
        elif time_ago < 2629800:
            info['time_ago'] = f"{int(time_ago // 604800)}w"
        elif time_ago < 31557600:
            info['time_ago'] = f"{int(time_ago // 2629800)}mo"
        else:
            info['time_ago'] = f"{int(time_ago // 31557600)}y"
            
        notification_info.append(info)
    return notification_info
      

def seen_notification(notification_id):
    notification = Notification.query.get(notification_id)
    notification.seen = True
    db.session.commit()
    return True