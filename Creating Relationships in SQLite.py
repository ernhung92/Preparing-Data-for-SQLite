
# coding: utf-8

# # Introduction to the Data

# In[1]:


import sqlite3
import pandas

conn = sqlite3.connect("nominations.db")

# Returns the schema table
schema_query = "pragma table_info(nominations)"
schema = conn.execute(schema_query).fetchall()

for s in schema:
    print(s)


# In[2]:


# Returns the first 10 rows
first_ten_query = "select * from nominations limit 10;"
first_ten = conn.execute(first_ten_query).fetchall()
for r in first_ten:
    print(r)


# # Creating the Ceremonies Table

# In[3]:


# Creates the ceremonies table
create_ceremonies_table = "create table ceremonies(id integer primary key, Year integer, Host text);"
conn.execute(create_ceremonies_table)

# The records we want to be inserted to represent the list of tuples
years_hosts = [(2010, "Steve Martin"),
               (2009, "Hugh Jackman"),
               (2008, "Jon Stewart"),
               (2007, "Ellen DeGeneres"),
               (2006, "Jon Stewart"),
               (2005, "Chris Rock"),
               (2004, "Billy Crystal"),
               (2003, "Steve Martin"),
               (2002, "Whoopi Goldberg"),
               (2001, "Steve Martin"),
               (2000, "Billy Crystal"),
            ]
# INSERT query needed for the placeholder elements 
insert_query = "INSERT INTO ceremonies (Year, Host) VALUES (?,?);"

# years_hosts will be iterated and it will replace the placeholder elements with the values in years_hosts
conn.executemany(insert_query, years_hosts)

print(conn.execute("pragma table_info(ceremonies);").fetchall())
print(conn.execute("select * from ceremonies limit 10;").fetchall())


# # Foreign Key Constraints

# In[4]:


conn.execute("PRAGMA foreign_keys = ON;")


# # Setting up One-to-Many

# In[8]:


create_nominations_two = '''create table nominations_two 
(id integer primary key, 
category text, 
nominee text, 
movie text, 
character text, 
won integer,
ceremony_id integer,
foreign key(ceremony_id) references ceremonies(id));
'''

nom_query = '''
select ceremonies.id as ceremony_id, nominations.category as category, 
nominations.nominee as nominee, nominations.movie as movie, 
nominations.character as character, nominations.won as won
from nominations
inner join ceremonies 
on nominations.year == ceremonies.year
;
'''
joined_nominations = conn.execute(nom_query).fetchall()

conn.execute(create_nominations_two)

insert_nominations_two = '''insert into nominations_two (ceremony_id, category, nominee, movie, character, won) 
values (?,?,?,?,?,?);
'''

conn.executemany(insert_nominations_two, joined_nominations)
print(conn.execute("select * from nominations_two limit 5;").fetchall())


# # Deleting and Renaming Tables

# In[9]:


drop_nominations_query = "DROP TABLE nominations;"
conn.execute(drop_nominations_query)

renaming_nominations_two = "ALTER TABLE nominations_two RENAME TO nominations;"
conn.execute(renaming_nominations_two)


# # Creating a Join Table

# In[17]:


create_movies_table = "create table movies (id integer primary key, movie text);"
conn.execute(create_movies_table)

create_actors_table = "create table actors (id integer primary key, actor text);"
conn.execute(create_actors_table)

create_movies_actors_table = "create table movies_actors (id integer primary key, movie_id integer, actor_id integer, foreign key(movie_id) references movies(id), foreign key(actor_id) references actors(id));"
conn.execute(create_movies_actors_table)

