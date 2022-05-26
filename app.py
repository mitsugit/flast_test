from flask import Flask, render_template, request, flash, redirect, url_for
import os
from datetime import datetime
from dotenv import load_dotenv
import psycopg2

from flask_paginate import Pagination, get_page_parameter


load_dotenv()
connection = psycopg2.connect(os.environ["DATABASE_URL_local"])

SELECT_ALL_MOVIES = "SELECT * FROM movies;"

SELECT_ALL_PERSON = "SELECT * FROM person;"

SEARCH_MOVIE = """SELECT * FROM movies WHERE index = %s;"""

SEARCH_PERSON = """SELECT * FROM person WHERE index = %s;"""

UPDATE_MOVIE = """UPDATE movies SET title = %s, release_timestamp = %s WHERE index = %s;"""

UPDATE_PERSON = """UPDATE person SET first_name = %s, last_name = %s , email = %s , gender = %s , 
                data_of_birth = %s, country_of_birth = %s  WHERE index = %s;"""

INSERT_MOVIE = "INSERT INTO movies (title, release_timestamp) VALUES (%s, %s)"

# name__ を 入れ て おく こと で Flask 自身 が ディレクトリ の 場所 を 認識 する こと が でき ます。
app = Flask(__name__)

# columns = ["index", "title", "datetime"]

person_columns = ["index", "first_name", "last_name", "email", "gender", "data_of_birth", "country_of_birth"]


def get_person(index):
    if index == '':
        with connection:
            cursor = connection.cursor()
            cursor.execute(SELECT_ALL_PERSON)
            return cursor.fetchall()

    elif index == '1':
        query = "SELECT * FROM person order by index"
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    elif index == '2':
        query = "SELECT * FROM person order by index DESC"
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

    else:
        with connection:
            cursor = connection.cursor()
            cursor.execute(SEARCH_PERSON, (index,))
            return cursor.fetchall()


def update_person(index, first_name, last_name, email, gender, data_of_birth, country_of_birth ):
    with connection:
        cursor = connection.cursor()
        cursor.execute(UPDATE_MOVIE, (first_name, last_name, email, gender, data_of_birth, country_of_birth, index))


# 新規作成画面を展開
@app.route('/')
def test():
    records = get_person('')
    datas = [dict(zip(person_columns, data)) for data in records]

    datas = sorted(datas, key=lambda x: x['index'])

    # # ページネーション
    # page = request.args.get(get_page_parameter(), type=int, default=1)
    # res = records[(page - 1) * 10: page * 10]
    #
    # pagination = Pagination(page=page, total=len(records), per_page=10, css_framework='bootstrap4')

    title = 'test ： 新規作成'

    test_list = ['1', '2', '3']

    return render_template('test.html', title=title, datas=datas, test_list=test_list)


@app.route('/pagination_test')
def pagination():
    records = get_person('')
    datas = [dict(zip(person_columns, data)) for data in records]

    datas = sorted(datas, key=lambda x: x['index'])

    # 表示しているページのページ番号を取得
    # default=1を変更することで、デフォルトで表示するページを変更
    page = request.args.get(get_page_parameter(), type=int, default=1)
    # 1ページに表示させるレコードの件数を指定（今回は50件）
    rows = datas[(page - 1)*50: page*50]

    # page:現在のページ
    # total:すべてのレコード件数
    # per_page:1ページに表示させるレコードの件数
    # css_framework:CSSフレームワーク（bootstrap,foundation,semantic,bulmaに対応）
    pagination = Pagination(page=page, total=len(datas),  per_page=50, css_framework='bootstrap5')

    return render_template('paginate-sample.html', rows=rows, pagination=pagination)


    title = 'test ： 新規作成'

    return render_template('test.html', title=title, datas=datas)




# 編集画面の展開
@app.route('/edit/<int:index>', methods=['GET'])
def edit(index):
    record = get_person(index)
    data = dict(zip(person_columns, record[0]))

    print(record[0])
    print(data)

    title = '変種 ： 編集画面'
    return render_template('edit.html', title=title, data=data)


# 編集（更新）データの保存
@app.route('/update', methods=['POST'])
def update():
    index = request.form['id']
    edit_data = get_person(index)

    favs = request.args.getlist("fav")


    # title = request.form['title']
    # content = request.form['content']

    # UPDATE_PERSON(index, title, content)

    return redirect(url_for('test'))


@app.route('/checkbox_test', methods=['POST'])
def checkbox_test():
    # index = request.form['id']
    # edit_data = get_person(index)
    faves = request.form.getlist("check_list")
    print("checkは")
    print(faves)
    print(   faves[0]  )
    print(faves[0].split(','))

    return redirect(url_for('checkbox_test'))


@app.route('/checkbox_test', methods=['GET'])
def checkbox_page():
    records = get_person('')
    datas = [dict(zip(person_columns, data)) for data in records]
    datas = sorted(datas, key=lambda x: x['index'])
    page = request.args.get(get_page_parameter(), type=int, default=1)
    rows = datas[(page - 1)*10: page*10]
    pagination = Pagination(page=page, total=len(datas),  per_page=10, css_framework='bootstrap5')

    return render_template('checkbox_test.html', rows=rows, pagination=pagination)

# 挿入
def add_movie(title):
    release_timestamp = datetime.datetime.today().strftime("%d-%m-%Y")
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(INSERT_MOVIE, (title, release_timestamp))


@app.route('/filter_test', methods=['GET'])
def filtering():
    
    if request.args.get('ordertest'):
        order = request.args.get('order')
        print(order)
        records = get_person(order)
    else:
        order='1'
        records = get_person('')
    datas = [dict(zip(person_columns, data)) for data in records]
    # datas = sorted(datas, key=lambda x: x['index'])
    page = request.args.get(get_page_parameter(), type=int, default=1)
    rows = datas[(page - 1)*10: page*10]
    pagination = Pagination(page=page, total=len(datas),  per_page=10, css_framework='bootstrap5')
    
    return render_template('filter_test.html',rows=rows, pagination=pagination,order=order)


@app.route('/jquery_test', methods=['GET'])
def jqtest():
    
    if request.args.get('ordertest'):
        order = request.args.get('order')
        print(order)
        records = get_person(order)
    else:
        order='1'
        records = get_person('')
    datas = [dict(zip(person_columns, data)) for data in records]
    # datas = sorted(datas, key=lambda x: x['index'])
    page = request.args.get(get_page_parameter(), type=int, default=1)
    rows = datas[(page - 1)*10: page*10]
    pagination = Pagination(page=page, total=len(datas),  per_page=10, css_framework='bootstrap5')
    
    return render_template('jquery_test.html',rows=rows, pagination=pagination,order=order)


@app.route('/capsule_test', methods=['GET'])
def capsule():
    if request.args.get('ordertest'):
        order = request.args.get('order')
        print(order)
        records = get_person(order)
    else:
        order = '1'
        records = get_person('')
    datas = [dict(zip(person_columns, data)) for data in records]
    # datas = sorted(datas, key=lambda x: x['index'])
    page = request.args.get(get_page_parameter(), type=int, default=1)
    rows = datas[(page - 1) * 10: page * 10]
    pagination = Pagination(page=page, total=len(datas), per_page=10, css_framework='bootstrap5')

    return render_template('capsule_test.html', rows=rows, pagination=pagination, order=order)


# アプリケーションの起動
if __name__ == '__main__':
    app.run(debug=True)
