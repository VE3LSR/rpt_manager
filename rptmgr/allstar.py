import urllib3

http = urllib3.PoolManager()

allstarStats = "http://stats.allstarlink.org"

class allstar():
    def __init__(self,nodeId):
        self.nodeID = nodeId

    # Get where the Allstar bubbles exist
    def getBubblesLink(self):
        return "%s/getstatus.cgi?%s" % (allstarStats, self.nodeID)

    # Go out and get the image, and return it -- stats doesn't support SLL, so we need to handle is ourselves
    def getBubblesImg(self):
        response = http.request('GET', self.getBubblesLink())
        # TODO: Check the response code and raise if there is an error
        return response.data

