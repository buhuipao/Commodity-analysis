# _*_ coding: utf-8 _*_

from flask import Flask, render_template, session, url_for, redirect, flash
from flask_bootstrap import Bootstrap

from flask_wtf import FlaskForm as Form
from wtforms import StringField, FloatField, BooleanField, SubmitField
from wtforms.validators import Required, Length


from bokeh import plotting
from bokeh.resources import CDN
from bokeh import embed


app = Flask(__name__)
bootstrap = Bootstrap(app)
app.secret_key = 'my-very-long-secret-key'


def make_my_plot():
    x = [1, 2, 3, 4, 5]
    y = [6, 7, 2, 4, 5]
    p = plotting.figure(title="simple line example", x_axis_label='x', y_axis_label='y')
    p.line(x, y, legend="Temp.", line_width=2)
    return p


@app.route('/info', methods=['GET'])
def plot():
    plot = make_my_plot()
    image = embed.file_html(plot, CDN, u"标题").decode('utf-8')
    return render_template('info.html', image=image)


class SearchForm(Form):
    price = FloatField('Limit_price', validators=[Required()])
    key_word = StringField('Key_word', validators=[Required(), Length(1, 64)])
    refresh = BooleanField('Forced refresh search')
    submit = SubmitField('Search')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        old_word = session.get('key_word')
        old_price = session.get('price')
        if old_word is not None and old_price is not None and old_word == form.key_word.data and old_price == form.price.data:
            flash('It seems like you searched the same keyword and price for the two time!')
        session['price'] = form.price.data
        session['key_word'] = form.key_word.data
        session['refresh'] = form.refresh.data
        session['search'] = True
        # return redirect(url_for('index'))
    else:
        session['refresh'] = False
        session['search'] = False
    return render_template('index.html', form=form, refresh=session.get('refresh'), search=session.get('search'), price=session.get('price'), key_word=session.get('key_word'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
