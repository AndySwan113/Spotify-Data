#!/usr/bin/env python
# coding: utf-8

# In[201]:


import pandas as pd


# In[202]:


conda install -c conda-forge spotipy


# In[203]:


import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="0e58969e0fc64ff7ae10502c99ccc90a",
                                                           client_secret="6ba5290e0a104d53a21d3ffbede39c57"))


# In[204]:


playlist_link = "https://open.spotify.com/playlist/3ePVmSDXLKMUf1fMa9E1ET"
playlist_URI = playlist_link.split("/")[-1].split("?")[0]
track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]

playlist_link2 = "https://open.spotify.com/playlist/4j8vuFq6uuNhrhcbQXb0QN"
playlist_URI2 = playlist_link2.split("/")[-1].split("?")[0]


# In[205]:


r = sp.playlist_tracks(playlist_URI)
t = r['items']
while r['next']:
    r = sp.next(r)
    t.extend(r['items'])
    
r = sp.playlist_tracks(playlist_URI2)
t2 = r['items']
while r['next']:
    r = sp.next(r)
    t2.extend(r['items'])
        
t3 = t + t2


# In[206]:


track_name = []
artist_name = []
artist_pop = []
artist_genres = []
album = []
track_pop = []
dance = []
energy = []
speechiness = []
acousticness = []
release_date = []

count = 0


for track in t3:
    #URI
    try:

        track_uri = track["track"]["uri"]
        
        al = sp.album(track["track"]["album"]["id"])

        #Track name
        track_name.append(track["track"]["name"])
        #Main Artist
        artist_uri = track["track"]["artists"][0]["uri"]
        artist_info = sp.artist(artist_uri)
        #Name, popularity, genre
        artist_name.append(track["track"]["artists"][0]["name"])
        artist_pop.append(artist_info["popularity"])
        artist_genres.append(artist_info["genres"])
        #Album
        album.append(track["track"]["album"]["name"])
        #Popularity of the track
        track_pop.append(track["track"]["popularity"])
    
        count += 1
        print(count)
        
        features = sp.audio_features(track["track"]["id"])
        
        release_date.append(al["release_date"])
        dance.append(features[0]["danceability"])
        energy.append(features[0]["energy"])
        speechiness.append(features[0]["speechiness"])
        acousticness.append(features[0]["acousticness"])
        
        
    except:
        continue

print(release_date)
    


# In[207]:


print(release_date)
print(dance)


# In[208]:


spotify_df = pd.DataFrame({'artist_name' : artist_name, 'track_name' : track_name, 'track_pop' : track_pop, 'album' : album, 'artist_pop' : artist_pop, 'artist_genres' : artist_genres, 'dance' : dance, 'energy': energy, 'speeciness': speechiness, 'acousticness': acousticness, "release_date": release_date})
print(spotify_df.shape)
spotify_df.head(20)


# In[209]:


spotify_df.drop_duplicates(subset=['track_name'])
   


# In[210]:


spotify_df['artist_genres'].value_counts()


# In[211]:


spotify_genres = pd.DataFrame(spotify_df['artist_genres'].tolist()).fillna('').add_prefix('genre_')


# In[212]:


spotify_df = pd.concat([spotify_df, spotify_genres], axis=1)


# In[215]:


spotify_df


# In[227]:


spotify_df['genre_0'].value_counts() 


# In[214]:


spotify_df.to_csv('spotify.csv')

