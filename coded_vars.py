import pandas as pd

def convert_gender(gender):
    if gender == 1:
        gender_str = "Male"
    elif gender == 2:
        gender_str = "Female"
    else:
        gender_str = "Non-binary"
    return gender_str


def convert_medical_condition(medical_cond):
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
