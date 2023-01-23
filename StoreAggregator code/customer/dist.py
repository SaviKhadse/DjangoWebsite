import requests
from main.settings import DISTANCE_API_ENDPOINT_URL, DISTANCE_API_KEY
# from settings import DISTANCE_API_ENDPOINT_URL, DISTANCE_API_KEY

# https://maps.googleapis.com/maps/api/distancematrix/json?destinations=3120 scott boulevard, Santa Clara 95054
# &origins=755 E Capitol ave, Milpitas 95035&units=imperial
# &key=AIzaSyDDTrDwGE2slVlQ-2vZjesTW7FOx-_vSg8&mode=driving


def request_distance(origin: str,
                     destination: str,
                     mode='driving',
                     units='imperial'):

    DISTANCE_REQUEST_API = DISTANCE_API_ENDPOINT_URL + 'json?origins=' + \
        origin + '&destinations=' + destination + '&mode=' + \
        mode + '&units='+units + '&key=' + DISTANCE_API_KEY

    # payload = {}
    headers = {}
    response = requests.request("GET",
                                DISTANCE_REQUEST_API,
                                headers=headers
                                )

    if (response.status_code == 200):
        # print(response.text)
        # return DISTANCE_API_ENDPOINT_URL
        return response.text
    else:
        return "Something went wrong"
