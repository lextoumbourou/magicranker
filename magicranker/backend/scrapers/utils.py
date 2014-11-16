import urllib2
import time

USER_AGENT = (
    'Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1')


def get_page(url):
    """
    Gets the contents of a web page with some resilience to temporary errors
    """
    headers = {'User-Agent': USER_AGENT}
    request = urllib2.Request(url, headers=headers)

    # Keep looping until you get a 200 response but only 3 times
    for i in range(3):
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError:
            # Sleep for 1 second to give web server a break
            time.sleep(1)
            continue
        html = response.read()
        response.close()
        return html
    return False
