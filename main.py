from googleapiclient.discovery import build
import re
import requests
from secret import spotifyId, spotifyApiToken, baseAddress, playlistId, ytApiKey ,youtubePlaylistId

# userLikedPlaylistQuery = f'{baseAddress}me/tracks?limit=50'
userPlaylistQuery = f'{baseAddress}playlists/{playlistId}/tracks'

nextPage = 'first'
finalVids = []
iterCount = 0
itemCount = 0

while nextPage:
    vidList = []
    if nextPage == 'first':
        nextPage = None
    service = build('youtube', 'v3', developerKey=ytApiKey)
    playlistData = service.playlistItems().list(part='contentDetails',
                                                playlistId=youtubePlaylistId,
                                                maxResults=50,
                                                pageToken=nextPage
                                                ).execute()

    for i in playlistData['items']:
        vidList.append((i['contentDetails']['videoId']))
    
    vidData = service.videos().list(
        part='snippet', id=','.join(vidList)).execute()
    
    for i in vidData['items']:
        if i['snippet']['channelTitle'].endswith('- Topic'):
            i['snippet']['channelTitle'] = i['snippet']['channelTitle'][:-7]
        finalVids.append(i['snippet']['title'] + ' - ' + i['snippet']['channelTitle'])
    
    iterCount += 1
    itemCount += len(vidList)
    print(f'iteration {iterCount} complete || {itemCount} items done')
    nextPage = playlistData.get('nextPageToken')

cnt = 0
for i in finalVids:
    cnt = cnt + 1
    res = requests.get('https://api.spotify.com/v1/search',
                       params={'type': 'track', 'q': i},
                       headers={
                           'Content-Type': 'application/json',
                           "Authorization": f"Bearer {spotifyApiToken}"
                       }
                       ).json()
    if len(res['tracks']['items']) != 0:
        res2 = requests.post(userPlaylistQuery,
                             params={'uris': res['tracks']['items'][0]['uri']},
                             headers={
                                 'Content-Type': 'application/json',
                                 "Authorization": f"Bearer {spotifyApiToken}"
                             }
                             ).json()
        print(res2)
    print(cnt)
