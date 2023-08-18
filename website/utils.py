from datetime import datetime, timedelta, time


def user_group_is_client(user):
    # Function that checks if the user is in the 'Client' group
    return user.groups.filter(name='Client').exists()


def user_group_is_professional(user):
    # Function to checks if the user is in the 'Client' group
    return user.groups.filter(name='Professional').exists()


def get_next_time(current_time, time_slot):
    # calculating the slots by adding 15 min to the opening time of the mikvah and then 15 min to the ending
    # time of the last slot.
    opening_time = time(current_time.hour, current_time.minute, current_time.second)
    opening_datetime = datetime.combine(datetime.today(), opening_time)
    next_opening_time = (opening_datetime + timedelta(minutes=time_slot)).time()
    return next_opening_time


def get_time_format(time_str):
    # Function to translate str objects to time format jj/mm/yyyy
    if time_str.lower() == 'noon':
        time_apm = time(hour=12, minute=0).strftime("%I:%M %p")
        time_obj = datetime.strptime(time_apm, "%I:%M %p").time()
    elif len(time_str) == 6:
        time_apm = time(hour=int(time_str[0]), minute=0).strftime("%I:%M %p")
        time_obj = datetime.strptime(time_apm, "%I:%M %p").time()
    else:
        time_str_re = time_str.replace(".", "")
        time_obj = datetime.strptime(time_str_re, "%I:%M %p").time()
    return time_obj

