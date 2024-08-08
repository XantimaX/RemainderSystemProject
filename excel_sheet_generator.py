from pandas import DataFrame
import paths
def create_excel_sheet(details):
    course_names ,components, dates = [], [], []
    for detail in details :
        course_names.append(detail[0])
        components.append(detail[1])
        dates.append(detail[2])

    data = {
        "Course Names" : course_names,
        "Component Names" : components,
        "Dates" : dates
    }
    df = DataFrame(data)

    df.to_excel(rf"{paths.DIRECTORY_TO_EXCEL_SHEETS}\output.xlsx", sheet_name= "sheet1", index=False)
    return "output.xlsx"