# _*_ coding: utf-8 _*_

from flask_bootstrap import Bootstrap
from flask import Flask, render_template, session
from flask import url_for, redirect, flash, request

from forms import SearchForm
from plots import make_my_plot
from search import Search
from sql import db


app = Flask(__name__)
bootstrap = Bootstrap(app)
app.secret_key = 'my-very-long-and-hard-secret-key'


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        old_word = session.get('key_word')
        old_price = session.get('price')
        if old_word == form.key_word.data and \
           old_price == form.price.data:
            flash('It seems like you searched the same keyword and \
                    price for the two time!')
        session['price'] = form.price.data
        session['key_word'] = form.key_word.data
        return redirect(url_for('search',
                        key_word=form.key_word.data,
                        price=form.price.data, refresh=form.refresh.data))

    return render_template('index.html', form=form)


@app.route('/search/', methods=['GET', 'POST'])
def search():
    # 如果不强制刷新直接从数据库里查询返回结果
    form = SearchForm()
    if form.validate_on_submit():
        old_word = session.get('key_word')
        old_price = session.get('price')
        if old_word == form.key_word.data and \
           old_price == form.price.data:
            flash('It seems like you searched the same keyword and \
                    price for the two time!')
        session['price'] = form.price.data
        session['key_word'] = form.key_word.data
        return redirect(url_for('search',
                        key_word=form.key_word.data,
                        price=form.price.data,
                        refresh=form.refresh.data))

    key_word = request.args.get('key_word', None)
    price = float(request.args.get('price', '0'))
    refresh = request.args.get('refresh', 'False')
    page = int(request.args.get('page', 1))
    if refresh == 'True':
        result, end_page = Search(price, key_word, page), 5
    else:
        data = db.search_goods(price, key_word)
        end_page = len(data)/8 if len(data) % 8 == 0 else len(data)/8 + 1
        # 考虑取到最后一页数据不满8个会报错
        try:
            result = data[8*(page-1):8*page]
        except:
            result = data[8*(page-1):]
    end_page_list = range(1, end_page+1)
    prev_page = page - 1 if page - 1 else 1
    next_page = page + 1 if page + 1 <= end_page else end_page
    return render_template(
            'search.html',
            form=form,
            key_word=key_word,
            price=price,
            refresh=refresh,
            page=page,
            result=result,
            end_page_list=end_page_list,
            prev_page=prev_page,
            next_page=next_page)


@app.route('/info/', methods=['GET'])
def plot():
    goods_name = request.args.get('goods_name', None)
    key_word = request.args.get('key_word', None)
    data = db.find_one_goods(key_word, goods_name)
    image = make_my_plot(data)
    return render_template(
            'info.html',
            image=image,
            data=data)


@app.errorhandler(500)
def service_error(e):
    return render_template('500.html'), 500


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
