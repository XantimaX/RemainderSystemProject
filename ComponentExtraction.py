import re

components = ('quiz', 'midsem', 'compre')
number_suffixes = "stndrdth"
month_dict = {
    "january"       : '01',
    "february"      : '02',
    "march"         : '03',
    "april"         : '04',
    "may"           : '05',
    "june"          : '06',
    "july"          : '07',
    "august"        : '08',
    "september"     : '09',
    "october"       : '10',
    "november"      : '11',
    "december"      : '12'
}

def extract_details(component_name,component_date) :

    component_name_list = component_name.split(' ')
    for i,component_name in enumerate(component_name_list) :
        component_name_list[i] = component_name.lower().strip()

    modified_component_name = ("".join(component_name_list)).replace("-", "")

    if ("lab" in modified_component_name) :
        return

    for component in components :
        if component in modified_component_name :
            modified_component_name = component
            break
    else :
        return

    #Making the date into DD/MM/YYYY

    temp_date_list = re.split("[\. /\n-]", component_date)
    date_list = []
    for i in temp_date_list :
        if i != "" :
            date_list.append(i)

    if (len(date_list) == 0) :
        return [modified_component_name, "Surprize"]
    if (not(date_list[0].isnumeric())):
        # If the date mentioned is something like "TBA"
        return [modified_component_name, component_date]

    status = False

    required_month = None

    for month in month_dict.keys() :
        if date_list[1].lower() in month :
            required_month = month
            break

    if 1 <= int(date_list[0]) <= 9:
        date_list[0] = "0" + str(int(date_list[0]))

    if required_month :
        date_list[0] = date_list[0].strip(number_suffixes)
        date_list[1] = month_dict[required_month]

    date_list[2] = date_list[2].strip(",")
    modified_component_date = "/".join(date_list[:3])
    return [modified_component_name, modified_component_date]