import requests
from google.protobuf.json_format import MessageToDict
from google.transit import gtfs_realtime_pb2
import json

def print_feed_from_url(url):
    response = requests.get(url)

    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)

    feed_dict = MessageToDict(feed)
    print(json.dumps(feed_dict, indent=2))

if __name__ == "__main__":
    gtfs_rt_url = 'https://www.ztm.poznan.pl/pl/dla-deweloperow/getGtfsRtFile?file=feeds.pb'
    print_feed_from_url(gtfs_rt_url)
