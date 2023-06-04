from flask import render_template, redirect, url_for, flash
import string
from random import choice

from . import app, db
from .forms import URLForm
from .models import URLMap


def get_unique_short_id():
    str_ = string.ascii_letters
    for i in range(1, 10):
        str_ += str(i)
    new_str = ''
    while len(new_str) <= 5:
        new_str += choice(str_)
    return new_str


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if form.validate_on_submit():
        '''if URLMap.query.filter_by(original=form.original_link.data).first():
            flash(f'Имя "{form.original_link.data}" уже занято!')
            return render_template('index.html', form=form)'''
        short = None
        if form.custom_id.data:
            short = form.custom_id.data
        else:
            short = get_unique_short_id()
        if URLMap.query.filter_by(short=short).first():
            short = get_unique_short_id()
        url = URLMap(
            original=form.original_link.data,
            short=short,
        )
        db.session.add(url)
        db.session.commit()
        flash(url_for('short_view', short=short, _external=True))
    return render_template('index.html', form=form)


@app.route('/<string:short>')
def short_view(short):
    original = URLMap.query.filter_by(short=short).first_or_404().original
    return redirect(original)
