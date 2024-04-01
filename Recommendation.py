import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn.metrics.pairwise import cosine_similarity
warnings.filterwarnings('ignore')
books= pd.read_csv("C:/Users/Vijayvardhan reddy/Desktop/books.csv")
ratings = pd.read_csv("C:/Users/Vijayvardhan reddy/Desktop/ratings.csv")
users = pd.read_csv("C:/Users/Vijayvardhan reddy/Desktop/users.csv")
ratings_name=ratings.merge(books, on="ISBN")
no_of_rating = ratings_name.groupby('Book-Title').count()['Book-Rating'].reset_index()
no_of_rating.rename(columns={'Book-Rating':'num_of_rating'},inplace=True)
average_rating = ratings_name.groupby('Book-Title').mean()['Book-Rating'].reset_index()
average_rating.rename(columns={'Book-Rating':'avg_rating'},inplace=True)
popular_books = no_of_rating.merge(average_rating ,on='Book-Title')
popular_books_df=popular_books[popular_books['num_of_rating']>=500].sort_values('avg_rating',ascending=False)
pop_books = popular_books_df.merge(books ,on='Book-Title').drop_duplicates('Book-Title')[['Book-Title','Book-Author','Year-Of-Publication']]
pop_books.shape
a = ratings_name.groupby('User-ID').count()['Book-Title']>300
geninue_users = a[a].index
geniune_user =ratings_name[ratings_name['User-ID'].isin(geninue_users)]
b = geniune_user.groupby('Book-Title').count()['Book-Rating']>=50
filtered_rat = b[b].index
final_df =geniune_user[geniune_user['Book-Title'].isin(filtered_rat)]
piv_tbl = final_df.pivot_table(index='Book-Title',columns='User-ID')
piv_tbl.fillna(0,inplace=True)
cos_simscore = cosine_similarity(piv_tbl)
def recommend(books_name):
index = np.where(piv_tbl.index==books_name)[0][0]
similar_books = sorted(list(enumerate(cos_simscore[index])),key=lambda x:x[1],reverse=True)[1:6]
for i in similar_books:
print(piv_tbl.index[i[0]])
In [52]:
try:
recommend("Fahrenheit 451")
except:
print("No Similar Books")
