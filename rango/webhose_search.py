import json, urllib, urllib2, os

def read_webhose_key():
    """ Read the Webhose API key from search.key file.
    """

    webhose_api_key = None
    print(os.getcwd())
    try:
        with open('search.key', 'r') as f:
            webhose_api_key = f.readline().strip()
    except:
        raise IOError('search.key file not found')

    return webhose_api_key

def run_query(search_terms, size=10):
    """
    Given a string containing search terms (query) and a number of
    results to return (10 by default) returns a list of results from
    the Webhose API with each result consisting of a title, link and summary
    """

    webhose_api_key = read_webhose_key()

    if not webhose_api_key:
        raise KeyError('Webhose key not found')

    root_url = 'http://webhose.io/search'

    # Format the query string - escape special characters
    query_string = urllib.quote(search_terms)

    search_url = ('{root_url}?token={key}&format=json&q={query}'
                  '&sort=relevancy&size={size}').format(
                    root_url=root_url,
                    key=webhose_api_key,
                    query=query_string,
                    size=size
    )

    print(search_url)
    results = []

    try:
        # Connect to the Webhose API, convert the reponse to a Python dictionary
        response = urllib2.urlopen(search_url).read()
        json_response = json.loads(response)

        # Loop through the posts, appending each to the results list as a new dictionary
        # We restrict summaries to the first 200 characters
        for post in json_response['posts']:
            results.append({'title': post['title'],
                            'link': post['url'],
                            'summary': post['text'][:200]})
    except:
        print("Error when querying the Webhose API")

    return results



















