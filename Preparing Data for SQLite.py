
# coding: utf-8

# # Introduction to the Data

# In[1]:


import pandas

data = pandas.read_csv("academy_awards.csv", encoding="ISO-8859-1")
data.head(5)


# In[2]:


data["Unnamed: 5"].value_counts()


# In[3]:


data["Unnamed: 6"].value_counts()


# In[4]:


data["Unnamed: 7"].value_counts()


# In[5]:


data["Unnamed: 8"].value_counts()


# In[6]:


data["Unnamed: 9"].value_counts()


# In[7]:


data["Unnamed: 10"].value_counts()


# # Filtering the Data

# In[8]:


# Cleaning up the "Year" column
data["Year"] = data["Year"].str[0:4]
data["Year"] = data["Year"].astype("int64")


# In[9]:


later_than_2000 = data[data["Year"] > 2000]
award_categories = ["Actor -- Leading Role", "Actor -- Supporting Role", "Actress -- Leading Role", "Actress -- Supporting Role"]
nominations = later_than_2000[later_than_2000["Category"].isin(award_categories)]
nominations


# # Cleaning up the Won? and Unnamed Columns

# In[10]:


# Turn the warning message off
pandas.options.mode.chained_assignment = None
replacements = { "NO": 0, "YES": 1 }
nominations["Won?"] = nominations["Won?"].map(replacements)

nominations.rename(columns={'Won?': 'Won'}, inplace=True)

# Make sure to restart and run all to avoid NaN's returns
nominations.head(5)


# In[11]:


# Dropping the unnecessary columns
drop_cols = ["Unnamed: 5", "Unnamed: 6","Unnamed: 7", "Unnamed: 8", "Unnamed: 9", "Unnamed: 10"]
final_nominations = nominations.drop(drop_cols, axis=1)
final_nominations.head(5)


# # Cleaning up the Additional Info Column

# In[12]:


additional_info_one = final_nominations["Additional Info"].str.rstrip("'}")
additional_info_two = additional_info_one.str.split(" {'")
movie_names = additional_info_two.str[0]
characters = additional_info_two.str[1]
print(movie_names)
print(characters)


# In[13]:


final_nominations["Movie"] = movie_names
final_nominations["Character"] = characters

final_nominations = final_nominations.drop("Additional Info", axis=1)

final_nominations.head()


# # Exporting to SQLite

# In[14]:


import sqlite3
conn = sqlite3.connect("nominations.db")
final_nominations.to_sql("nominations_sql_table", conn, index=False)


# # Verifying in SQL

# In[15]:


query1 = "PRAGMA TABLE_INFO(nominations_sql_table);"
query2 = "select * from nominations_sql_table limit 10;"
print(conn.execute(query1).fetchall())
print(conn.execute(query2).fetchall())
conn.close()

