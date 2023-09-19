from . import config
import json
import random
import string
import bs4


def list_courses(scp):
    """List all courses for the current user."""

    url = f"{scp.config.URL_BASE}/d2l/le/manageCourses/search/{scp.config.UNKNOWN_1}/GridReloadPartial"

    form_data = {
        'gridPartialInfo$_type': 'D2L.LP.Web.UI.Desktop.Controls.GridPartialArgs',
        'gridPartialInfo$SortingInfo$SortField': 'OrgUnitName',
        'gridPartialInfo$SortingInfo$SortDirection': '0',
        'gridPartialInfo$NumericPagingInfo$PageNumber': '1',
        'gridPartialInfo$NumericPagingInfo$PageSize': '100',
        'searchTerm': '',
        'status': '-1',
        'toStartDate$Year': '2023',
        'toStartDate$Month': '9',
        'toStartDate$Day': '7',
        'toStartDate$Hour': '15',
        'toStartDate$Minute': '0',
        'toStartDate$Second': '0',
        'fromStartDate$Year': '2023',
        'fromStartDate$Month': '9',
        'fromStartDate$Day': '7',
        'fromStartDate$Hour': '15',
        'fromStartDate$Minute': '0',
        'fromStartDate$Second': '0',
        'toEndDate$Year': '2023',
        'toEndDate$Month': '9',
        'toEndDate$Day': '7',
        'toEndDate$Hour': '15',
        'toEndDate$Minute': '0',
        'toEndDate$Second': '0',
        'fromEndDate$Year': '2023',
        'fromEndDate$Month': '9',
        'fromEndDate$Day': '7',
        'fromEndDate$Hour': '15',
        'fromEndDate$Minute': '0',
        'fromEndDate$Second': '0',
        'hasToStartDate': 'False',
        'hasFromStartDate': 'False',
        'hasToEndDate': 'False',
        'hasFromEndDate': 'False',
        'filtersFormId$Value': 'd2l_1_0_248',
        '_d2l_prc$headingLevel': '2',
        '_d2l_prc$scope': '',
        '_d2l_prc$childScopeCounters': 'filtersData:0;FromStartDate:0;ToStartDate:0;FromEndDate:0;ToEndDate:0',
        '_d2l_prc$hasActiveForm': 'false',
        'filtersData$semesterId': 'All',
        'filtersData$departmentId': 'All',
        'isXhr': 'true',
        'requestId': '2',
        'd2l_referrer': scp.get_csrf(),
    }

    # for i in form_data:
    #     print(i+":"+form_data[i])

    response = scp.client.post(url, data=form_data)
    # print(response.request.headers)
    response.raise_for_status()
    text = response.text.removeprefix("while(1);")
    # print(len(text))

    # with open("courses.json", "w") as f:
    #     f.write(text)
    data = json.loads(text)

    return parse_courses_html(data['Payload']['Html'])
        
def random_string(length):
    """Generate a random string of the given length."""
    return ''.join(random.choices(string.ascii_letters, k=length))

def parse_courses_html(html):
    """Parse the HTML of the courses page and return a list of courses."""
    
    bs = bs4.BeautifulSoup(html, "html.parser")
    courses = []

    for row in bs.find('table').find_all('a'):
        id = row['href'].split('/')[-1]
        semester = row.parent.parent.find_all('td')[1].text.strip()
        name = row.text
        courses.append({
            'id': id,
            'name': name,
            'semester': semester
        })
        

    return courses