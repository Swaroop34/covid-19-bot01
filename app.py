from flask import Flask, request, make_response
import os
import requests
import json
from flask_cors import cross_origin

app = Flask(__name__)

    
# Getting and sending response to dilogflow
@app.route('/webhook', methods=['POST'])
@cross_origin()
def webhook():
    req = request.get_json(silent=True, force=True)

    res = processRequest(req)
    res1 = json.dumps(res, indent=4)
    r = make_response(res1)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
   
    sessionID = req.get('responseId')
    result = req.get("queryResult")
    user_says = result.get("queryText")
    parameters = result.get("parameters")
    state_name = parameters.get("state_name")
    district_name = parameters.get("district_name")
    intent = result.get("intent").get('displayName')
    #    if intent == 'no_of_covid19_cases':
    url = "https://corona-virus-world-and-india-data.p.rapidapi.com/api_india"

    headers = {
        'x-rapidapi-host': "corona-virus-world-and-india-data.p.rapidapi.com",
        'x-rapidapi-key': "65a4901e97msh53dc5860f91c9d0p1c5d8fjsn1400fa81c935"
    }

    response = requests.request("GET", url, headers=headers)
    data = json.loads(response.text)
    
    if intent == 'india_wide_covid19_cases':
        confirmed_cases = data['total_values']['confirmed']
        active_cases = data['total_values']['active']
        deaths = data['total_values']['deaths']
        recovered = data['total_values']['recovered']
        
        show = 'The Covid-19 info of {} are as follows:'.format('India')
        a = 'The no. of active cases-(people in quarantine): {}'.format(active_cases)
        b = 'The total no. of confirmed cases: {}'.format(confirmed_cases)
        c = 'The total no. of deaths: {}'.format(deaths)
        d = 'The number of recovered: {}'.format(recovered)
        fulfillmentText = '{}\n {}\n {}\n {}\n {}\n'.format(show, b, a, c, d)
        return {"fulfillmentText": fulfillmentText}

    
    elif intent == 'state_wise_covid19_cases':
        confirmed_cases = data['state_wise'][state_name]['confirmed']
        active_cases = data['state_wise'][state_name]['active']
        deaths = data['state_wise'][state_name]['deaths']
        recovered = data['state_wise'][state_name]['recovered']

        show = 'The Covid-19 info of {} state are as follows:'.format(state_name)
        a = 'The no. of active cases-(people in quarantine): {}'.format(active_cases)
        b = 'The total no. of confirmed cases: {}'.format(confirmed_cases)
        c = 'The total no. of deaths: {}'.format(deaths)
        d = 'The number of recovered: {}'.format(recovered)
        fulfillmentText = '{}\n {}\n {}\n {}\n {}\n'.format(show, b, a, c, d)
        return {"fulfillmentText": fulfillmentText}

    elif intent == 'district_wise_covid19_cases':
        state_list = data['state_wise']
        for i, j in state_list.items():
            for x in j:
                if x == 'district':
                    for get_district_name in j[x]:
                        if get_district_name == district_name:
                            confirmed_cases = j[x][get_district_name]['confirmed']
                            active_cases = j[x][get_district_name]['active']
                            deaths = j[x][get_district_name]['deceased']
                            recovered = j[x][get_district_name]['recovered']

                            show = 'The Covid-19 info of {} district are as follows:'.format(district_name)
                            a = 'The no. of active cases-(people in quarantine): {}'.format(active_cases)
                            b = 'The total no. of confirmed cases: {}'.format(confirmed_cases)
                            c = 'The total no. of deaths: {}'.format(deaths)
                            d = 'The number of recovered: {}'.format(recovered)
                            fulfillmentText = '{}\n {}\n {}\n {}\n {}\n'.format(show, b, a, c, d)
                            return {"fulfillmentText": fulfillmentText}

    else:
        fulfillmentText = 'Sorry for the incovenience, I did not have the requested data in my database.'
        return {"fulfillmentText": fulfillmentText}


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print("starting app on port %d" % port)
    app.run(debug=False, port=port, host='0.0.0.0')
    # serve(app, host='0.0.0.0', port=5000)
