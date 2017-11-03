#twitch.py
# Handles all requests to twitch api
# Requires pip install requests
import requests
import json
import secrets

def main():

    getFollowers("","")
    getStreamUptime("")

def getFollowers(self, cursor):
    requestString = 'https://api.twitch.tv/kraken/channels/matroxkod/follows?client_id='+secrets.CLIENTID

    # Append a cursor if we have one
    if(len(cursor)>0):
        requestString = requestString+'&cursor='+cursor
    
    # Send the request
    r = requests.get(requestString)

    # Load the content
    x = json.loads(r.content)
    for user in x['follows']:
        print user['user']['display_name'], ' ', user['user']['_id'] , ' ' , user['created_at']

    # Recursively call get followers with new cursor from request if it has been provided
    newCursor = ""
    try:
        newCursor = x['_cursor']
    except:
        pass
    if(len(newCursor)>0):
        getFollowers("",newCursor)

def getStreamUptime(self):
    # Get Stream information
    requestString = 'https://api.twitch.tv/kraken/streams?client_id='+secrets.CLIENTID
    r = requests.get(requestString)
    print r

if __name__ == '__main__':
    main()
