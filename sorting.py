import re

def custom_sort(detail) :
    if re.match("\d\d/\d\d/\d\d\d?\d?",detail[2]) :
        date = detail[2].split("/")
        return (int(date[2][-2:]), int(date[1]), int(date[0]))
    return (1000000,1000000,1000000)

def sort_dates(details):
    sorted_details = sorted(details,key=custom_sort)
    return sorted_details