from flask import Flask, render_template,request
import pickle
import numpy as np

popular_df = pickle.load(open('popular.pkl', 'rb'))
pivot_table = pickle.load(open('pivot_table.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
fauthor_rating = pickle.load(open('fauthor_rating.pkl', 'rb'))
fpublisher_rating = pickle.load(open('fpublisher_rating.pkl', 'rb'))
app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           bookname=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-L'].values),
                           votes=list(popular_df['number'].values),
                           rating=list(popular_df['avg_Rating'].values)
                           )
#
@app.route('/recommend')
def recommend():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['POST'])
def recommend_books():
    user_input=request.form.get('user_input')

    index = np.where(pivot_table.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:11]
    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pivot_table.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-L'].values))

        data.append(item)
    print(data)
    return render_template('recommend.html',data=data)

@app.route('/author',methods=['GET','POST'])
def recommend_author():
    user_input=request.form.get('user_input')
    df1 = fauthor_rating.query("`Book-Author`==@user_input")
    df1 = df1.sort_values(by=['num_Rating', 'avg_Rating'], ascending=False)
    df1.drop_duplicates(subset='Book-Title', inplace=True)
    temp_df = df1.head(10)
    data = []
    item1 = []
    item2 = []
    item3 = []
    for index, row in temp_df.iterrows():
        item1 = []
        item2 = []
        item3 = []
        item1.append(row['Book-Title'])
        item2.append(row['Book-Author'])
        item3.append(row['Image-URL-L'])
        data.append(list(item1 + item2 + item3))
    print(data)
    return render_template('author.html',data=data)

@app.route('/publisher',methods=['GET','POST'])
def recommend_publisher():
    user_input=request.form.get('user_input')
    df = fpublisher_rating.query("`Publisher`==@user_input")
    df = df.sort_values(by=['num_Rating', 'avg_Rating'], ascending=False)
    df.drop_duplicates(subset='Book-Title', inplace=True)
    temp_df = df.head(10)
    data = []
    item1 = []
    item2 = []
    item3 = []
    for index, row in temp_df.iterrows():
        item1 = []
        item2 = []
        item3 = []
        item1.append(row['Book-Title'])
        item2.append(row['Book-Author'])
        item3.append(row['Image-URL-L'])
        data.append(list(item1 + item2 + item3))
    print(data)
    return render_template('publisher.html',data=data)

if __name__=='__main__':
    app.run(debug=True)