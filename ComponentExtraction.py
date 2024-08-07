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
    "december"      : '12',
    "jan"           : '01',
    "feb"           : '02',
    "march"         : '03',
    "april"         : '04',
    "may"           : '05',
    "june"          : '06',
    "july"          : '07',
    "aug"           : '08',
    "sep"           : '09',
    "oct"           : '10',
    "nov"           : '11',
    "dec"           : '12'
}



def extract_details(component_name,component_date) :

    component_name_list = component_name.split(' ')
    for i,component_name in enumerate(component_name_list) :
        component_name_list[i] = component_name.lower().strip()

    modified_component_name = ("".join(component_name_list)).replace("-", "")

    for component in components :
        if component in modified_component_name :
            modified_component_name = component
            break
    else :
        return


    #Making the date into DD/MM/YYYY
    date_list = re.split("[ \n-]", component_date)
    for (i,date) in enumerate(date_list) :
        date_list[i] = date.lower().strip(".")

    status = False
    for month in month_dict.keys() :
        if month in date_list :
            status = True
            break

    if status :
        date_list[0] = date_list[0].strip(number_suffixes)
        date_list[1] = month_dict[date_list[1]]
        modified_component_date = "/".join(date_list[:3])

    else :
        modified_component_date = date_list[0].replace(".", "/")

    return [modified_component_name, modified_component_date]