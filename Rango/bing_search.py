import json
import os
import urllib, urllib2 # Py2.7.x
#import urllib # Py3

def run_query(search_terms):
    bing_api_key = os.environ['api_key']
    if not bing_api_key:
        raise KeyError("Bing Key Not Found")

    root_url = 'https://api.datamarket.azure.com/Bing/Search/'
    service = 'Web'

    # Offset specifies where in the results list to start from.
    # With results_per_page = 10 and offset = 11, this would start from page 2.
    results_per_page = 10
    offset = 0

    # Wrap quotes around our query terms as required by the Bing API.
    # The query we will then use is stored within variable query.
    query = "'{0}'".format(search_terms)

    # Turn the query into an HTML encoded string, using urllib.
    query = urllib.quote(query) # Py2.7.x
    #query = urllib.parse.quote(query) # Py3

    # Construct the latter part of our request's URL.
    # Sets the format of the response to JSON and sets other properties.
    search_url = "{0}{1}?$format=json&$top={2}&$skip={3}&Query={4}".format(root_url,service,results_per_page,offset,query)
    # Setup authentication with the Bing servers.
    # The username MUST be a blank string, and put in your API key!
    username = ''

    # Setup a password manager to help authenticate our request.
    password_mgr = urllib2.HTTPPasswordMgrWithDefaultRealm() # Py2.7.x
    #password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm() # Py3

    password_mgr.add_password(None, search_url, username, bing_api_key)

    # Create our results list which we'll populate.
    results = []
    try:
        # Prepare for connecting to Bing's servers.# Py2.7.x
        handler = urllib2.HTTPBasicAuthHandler(password_mgr)
        opener = urllib2.build_opener(handler)
        urllib2.install_opener(opener)

        # Connect to the server and read the response generated.# Py2.7.x
        response = urllib2.urlopen(search_url).read()
        # Convert the string response to a Python dictionary object.
        json_response = json.loads(response)
        # Loop through each page returned, populating out results list.
        for result in json_response['d']['results']:
            results.append({'title': result['Title'],
                            'link': result['Url'],
                            'summary': result['Description']})

    except:
        print "Error when querying the Bing API"

    return results



def main():
	print("Enter a query ")
	query = raw_input()
	results = run_query(query)
	for result in results:
		print result['title']
		print '-'*len(result['title'])
		print result['summary']
		print result['link']
		print


if __name__ == '__main__':
	main()
