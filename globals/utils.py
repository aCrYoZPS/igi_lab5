def get_tz(user):
    tz_name = ""
    if hasattr(user, "staff_profile"):
        staff = user.staff_profile
        tz_name = staff.timezone

    elif hasattr(user, "client_profile"):
        client = user.client_profile
        tz_name = client.timezone

    return tz_name
