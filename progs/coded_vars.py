def convert_gender(gender):
    "Converts a volunteer or refugee's gender (coded as an integer from 1-3 in csv files) into a string to be displayed to the user."
    if gender == 1:
        gender_str = "Male"
    elif gender == 2:
        gender_str = "Female"
    else:
        gender_str = "Non-binary"
    return gender_str


def convert_medical_condition(medical_cond):
    "Converts a refugee's medical condition (coded as an integer from 1-7 in refugees.csv) into a string to be displayed to the user."
    if medical_cond == 1:
        medical_str = "Healthy"
    elif medical_cond == 2:
        medical_str = "Minor illness with no injuries"
    elif medical_cond == 3:
        medical_str = "Major illness with no injuries"
    elif medical_cond == 4:
        medical_str = "Minor injury with no illness"
    elif medical_cond == 5:
        medical_str = "Major injury with no illness"
    elif medical_cond == 6:
        medical_str = "Illness and injury (non-critical)"
    else:
        medical_str = "Critical condition (illness and/or injury)"
    return medical_str
