from flask import request, jsonify 
from datetime import datetime, timedelta
from model.userModel import User
from model.subscriptionModel import Subscription
from mongoengine.errors import DoesNotExist

def setup_subscription(user):
    trial_duration = timedelta(days=1)
    trial_subscription = Subscription(price=9.99)
    trial_subscription.start_date = datetime.utcnow()
    user.subscription = trial_subscription
    user.trial_end = trial_subscription.start_date + trial_duration
       
def cancel_subscription(user_id):
    try:
        user = User.objects.get(id=user_id)
    except DoesNotExist:
        raise ValueError("User does not exist")

    if not user.subscription:
        raise ValueError("User has no active subscription")

    user.subscription.end_date = datetime.utcnow()
    user.save()

def amend_subscription_plan(user_id, new_plan):
    if new_plan not in ["Monthly", "Annually"]:
        raise ValueError("Invalid subscription plan")

    try:
        user = User.objects.get(id=user_id)
    except DoesNotExist:
        raise ValueError("User does not exist")

    if not user.subscription or user.subscription.end_date is not None:
        raise ValueError("User has no active subscription or the subscription has an end date")
    
        
    if new_plan == "Monthly":
        user.subscription.plan = "Monthly"
        user.subscription.price = 9.99 
    elif new_plan == "Annually":
        user.subscription.plan = "Annually"
        user.subscription.price = 99.99 

    user.save()
    
def reinstate_subscription(user_id):
    try:
        user = User.objects.get(id=user_id)
    except DoesNotExist:
        raise ValueError("User does not exist")
    
    if not user.subscription:
        raise ValueError("User does not have an active subscription")
    
    if user.subscription.end_date is None:
        raise ValueError("User's subscription has not expired yet")
    
    user.subscription.end_date = None
    user.subscription.reinstate_date = datetime.utcnow()
    user.save()

def get_subscription_details(user_id):
    try:
        user = User.objects.get(id=user_id)
    except DoesNotExist:
        raise ValueError("User does not exist")
    
    if not user.subscription:
        raise ValueError("User doe not have an active subscription")
    
    subscription_details = user.subscription.to_mongo().to_dict()
    subscription_details["trial_end"] = user.trial_end
    return subscription_details
    


    
        
                     