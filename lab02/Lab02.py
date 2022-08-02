import csv
import requests
from bs4 import BeautifulSoup
from pprint import pprint
from typing import Any, Dict, List, Union

def problem_1(name: str) -> List[Dict[str, Union[str, List[str]]]]:
    # TODO Write your code for Problem 1 here.
    name = name.replace(" ", "_")
    url = "https://how-i-met-your-mother.fandom.com/wiki/" + name
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    infobox = soup.find("table", {"class": "infobox"})
    information = []
    for cell in infobox.find_all("td"):
        text =  cell.text
        key = text.split(":")[0]
        value = text.replace(key, "").replace(":", "")
        if key=='' or value=='':
            pass
        else:
            information.append({"attribute": key, "value": value})
    return information

def info_collector(links: List[str]) -> List[Dict[str,str]]:
    course = []
    for url in links:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        page_info = soup.find_all("a", {"class": "regular"})
        for info in page_info:
            if info.text not in  ["Home","long","medium"]:
                course.append(
                    {
                        "Name of Course":info.text,
                        "URL":info.get("href")
                    }
                )
    return course

def problem_2_1() -> List[Dict[str, str]]:
    base_url = "https://www.lsf.uni-saarland.de/qisserver/rds?state=wtree&search=1&trex=step&root120221=320944|310559|318658|311255&P.vx=kurz"

    # TODO Write your code for Problem 2.1 here.
    response = requests.get(base_url + "&language=en")
    soup = BeautifulSoup(response.text, 'lxml')
    course_types = soup.find_all("a", {"class": "ueb"})
    links = []
    for course_type in course_types[-5:]:
        link = course_type.get("href")
        link = str(link) + "&language=en"
        links.append(link)

    courses = info_collector(links)
    return courses

def get_additional_links(url: str) -> List[str]:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    basic_info_table = soup.find("table",{"summary":"Grunddaten zur Veranstaltung"})
    bi_tbody = basic_info_table.find_all("tr")
    links = []
    for row in bi_tbody:
        td = row.find("td",{"class":"mod_n_basic"})
        a = td.find("a",{"class":"regular"})
        if a is not None:
            result = a.text.strip()
            links.append(result)
    return links

def get_responsible_instructors(url: str) ->  Union[List[str], Any]:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    ri_info_table = soup.find("table",{"summary":"Verantwortliche Dozenten"})
    try:
        ri_tbody = ri_info_table.find_all("tr")
        ri = []
        for row in ri_tbody:
            td1 = row.find("td",{"class":"mod_n_odd"})
            td2 = row.find("td",{"class":"mod_n_even"})
            if td1 is not None:
                a1 = td1.find("a",{"class":"regular"})
                if a1 is not None:
                    result = a1.text.strip()
                    result = ' '.join(result.split())
                    ri.append(result)
                else:
                    pass
            else:
                pass
            
            if td2 is not None:
                a2 = td2.find("a",{"class":"regular"})
                if a2 is not None:
                    result = a2.text.strip()
                    result = ' '.join(result.split())
                    ri.append(result)
                else:
                    pass
            else:
                pass

        return ri
    except AttributeError:
        ri = "Not available"
        return ri
    

def problem_2_2(url: str) -> Dict[str, Union[str, List[str]]]:
    # TODO Write your code for Problem 2.2 here.
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    information = {}
    
    coursetype = ""
    number = ""
    term = ""
    eop = ""
    turnus = ""
    credit = ""
    language = ""
    long_text = ""
    short_text = ""
    hpt = ""
    mp = ""
    assignment = ""
    ap =  ""
    
    basic_info_table = soup.find("table",{"summary":"Grunddaten zur Veranstaltung"})
    bi_tbody = basic_info_table.find_all("tr")
    for row in bi_tbody:
        ths = row.find_all("th",{"class":"mod"})
        tds = row.find_all("td",{"class":"mod_n_basic"})
        for n, th in enumerate(ths):
            td = tds[n]
            if th is not None:
                if th.text == "Type of Course":
                    coursetype = td.text.strip()
                elif th.text == "Number":
                    number = td.text
                elif th.text == "Term":
                    term = td.text.strip()
                elif th.text == "Expected no. of participants":
                    eop = td.text.strip()
                elif th.text == "Turnus":
                    turnus = td.text.strip()
                elif th.text == "Credits":
                    credit = td.text.strip()
                elif th.text == "Language":
                    language = td.text.strip()
                elif th.text == "Long text":
                    long_text = td.text.strip()
                elif th.text == "Short text":
                    short_text = td.text.strip()
                elif th.text == "Hours per week in term":
                    hpt = td.text.strip()
                elif th.text == "Max. participants":
                    mp = td.text.strip()
                elif th.text == "Assignment":
                    assignment = td.text.strip()
                else:
                    ap = td.text.strip()
                    ap = ' '.join(ap.split())

           
    
    links = get_additional_links(url)
    
    ri = get_responsible_instructors(url)
    
    information = {
        "Type of Course": coursetype,
        "Number": number,
        "Term": term,
        "Expected no. of participants": eop,
        "Turnus": turnus,
        "Credits": credit,
        "Additional Links": links,
        "Language": language,
        "Long text": long_text,
        "Short text": short_text,
        "Hours per week in term": hpt,
        "Max. participants": mp,
        "Assignment": assignment,
        "application period": ap,
        "Responsible Instructors": ri
    }
   
    return information 

def problem_2_3() -> None:
    # TODO Write your code for Problem 2.3 here.
    courses_list = problem_2_1()
    courses = {}
    for course in courses_list:
        courses.update({course["Name of Course"]:course["URL"]})
    #all_course_info = []
    header =  ["Name of Course","Type of Course", "Number", "Term", "Expected no. of participants", "Turnus", "Credits", "Additional Links", "Language", "Long text", "Short text", "Hours per week in term", "Max. participants", "Assignment", "application period", "Responsible Instructors"]
    csv.DictWriter(open("courses.csv", "w", newline=""), header).writeheader()
    for key, value in courses.items():
        this_course_info = {}
        this_course_info["Name of Course"] = key
        information = problem_2_2(value)
        for inner_key, inner_value in information.items():
            if isinstance(inner_value, list):
                inner_value_whole_string = ""
                for item in inner_value:
                    inner_value_whole_string += item + "\n"
                this_course_info[inner_key] = inner_value_whole_string
            else:
                this_course_info[inner_key] = inner_value
        
        #all_course_info.append(this_course_info)
        csv.DictWriter(open("courses.csv", "a", newline=""),header).writerow(this_course_info)
    


def main():
    # You can call your functions here to test their behaviours.
    pprint(problem_1("Tracy McConnell"), sort_dicts=False, indent=4)
    #pprint(problem_2_1(), sort_dicts=False, indent=4)
    #pprint(problem_2_2("https://www.lsf.uni-saarland.de/qisserver/rds?state=verpublish&status=init&vmfile=no&publishid=136384&moduleCall=webInfo&publishConfFile=webInfo&publishSubDir=veranstaltung&language=en"), sort_dicts=False, indent=4)
    #problem_2_3()
if __name__ == "__main__":
    main()
    
    