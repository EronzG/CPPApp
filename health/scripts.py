from datetime import date


def calculateAge(birthDate):
    days_in_year = 365.2425
    age = int((date.today() - birthDate).days / days_in_year)
    return age


# Driver code
# print(calculateAge(date(1999, 2, 3)), "years")
