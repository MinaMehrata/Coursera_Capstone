
# coding: utf-8

# #  Cluster Toronto Neighbourhood

# ## Read Tabel from URL

# In[59]:


import pandas as pd
tables = pd.read_html('https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M')


# In[60]:


dataframe = tables[0]
dataframe.columns = dataframe.iloc[0]
dataframe = dataframe.iloc[1:]
dataframe.head


# ## ignore not assighted cells in Borough

# In[61]:


dataframe = dataframe[dataframe.Borough != 'Not assigned']
dataframe.head


# ## Same Postal codes combine into one row with the neighborhoods separated with a comma

# In[62]:


df=dataframe.groupby("Postal Code").agg(lambda x:','.join(set(x)))
df.head


# ## If a cell has a borough but a Not assigned neighborhood, then the neighborhood will be the same as the borough.
# 

# In[63]:


df.loc[df['Neighbourhood']=="Not assigned",'Neighbourhood']=df.loc[df['Neighbourhood']=="Not assigned",'Borough']
df.head


# In[64]:


df.shape


# In[65]:


geo_dataframe=pd.read_csv('https://cocl.us/Geospatial_data')
geo_dataframe.head


# In[66]:


df['Latitude']=geo_dataframe['Latitude'].values
df['Longitude']=geo_dataframe['Longitude'].values


# In[67]:


df.head


# In[68]:


import folium # map rendering library
 
# import k-means from clustering stage
from sklearn.cluster import KMeans
 
# Matplotlib and associated plotting modules
import matplotlib.cm as cm
import matplotlib.colors as colors


# In[69]:


# create map of Toronto using latitude and longitude values
latitude = df['Latitude'].mean()
longitude = df['Longitude'].mean()
map_toronto = folium.Map(location=[latitude, longitude], zoom_start=10)
map_toronto


# In[70]:


for lat, lng, borough, neighborhood in zip(
        df['Latitude'], 
        df['Longitude'], 
        df['Borough'], 
        df['Neighbourhood']):
    label = '{}, {}'.format(neighborhood, borough)
    label = folium.Popup(label, parse_html=True)
    folium.CircleMarker(
        [lat, lng],
        radius=5,
        popup=label,
        color='blue',
        fill=True,
        fill_color='#3186cc',
        fill_opacity=0.7,
        parse_html=False).add_to(map_toronto)  
 
map_toronto

