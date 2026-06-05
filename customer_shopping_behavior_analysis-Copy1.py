#!/usr/bin/env python
# coding: utf-8

# In[11]:


import pandas as pd 
df = pd.read_csv(r"C:\Users\devdi\Downloads\customer_shopping_behavior.csv")


# In[12]:


df.head()


# In[13]:


df.info()


# In[14]:


df.describe()


# In[15]:


df.isnull().sum()


# In[18]:


df['Review Rating']=df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))


# In[19]:


df.isnull().sum()


# In[24]:


df.columns=df.columns.str.lower()
df.columns=df.columns.str.replace(' ','_')
df=df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})


# In[25]:


df.columns


# In[28]:


#create a new column age_group 
labels=['Young Adult','Adult','Middle Aged','Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels=labels)


# In[32]:


df[['age', 'age_group']].head(10)


# In[34]:


#new columns purchase_frequency_days
frequency_mapping = {
    'Fortnightly': 14,
    'Weekly': 7,
    'Monthly': 30,
    'Quarterly': 90,
    'Bi-Weekly': 14,
    'Annually': 365,
    'Every 3 Months': 90
}
df['purchase_frequency_days']=df['frequency_of_purchases'].map(frequency_mapping)


# In[35]:


df[['purchase_frequency_days','frequency_of_purchases']].head(10)


# In[39]:


(df['discount_applied']==df['promo_code_used']).all()


# In[42]:


df=df.drop('promo_code_used',axis=1)


# In[43]:


df.columns


# In[45]:


pip install pyodbc sqlalchemy


# In[49]:


from sqlalchemy import create_engine

engine = create_engine(
    r"mssql+pyodbc://@DESKTOP-OABAA6P\SQLEXPRESS/customer_behavior"
    r"?driver=ODBC+Driver+17+for+SQL+Server"
    r"&trusted_connection=yes"
)


# In[50]:


df.to_sql(
    name='customer',      # table name to create in SQL Server
    con=engine,
    if_exists='replace',  # replace existing table
    index=False
)

