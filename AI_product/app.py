from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import openai

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # change this to your secret key
openai.api_key = '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'  # change this to your OpenAI API key


class URLForm(FlaskForm):
    url = StringField('URLs', validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()
    results = None
    if form.validate_on_submit():
        urls = form.url.data.splitlines()
        reviews = []
        for url in urls:
            params = {
                'token': 'WyAsI2Zt0_tDshEfS95ccg',
                'scraper': 'amazon-product-reviews',
                'format': 'json',
                'url': url,
            }
            response = requests.get('https://api.crawlbase.com/', params=params)
            data = response.json()
            if 'body' in data and 'reviews' in data['body']:
                reviews.extend(item['reviewText'] for item in data['body']['reviews'])

        reviews_text = '\n'.join(reviews)

        # 使用 OpenAI ChatGPT 处理评论文本
        response = openai.Completion.create(
            engine='gpt-3.5-turbo',
            prompt=reviews_text,
            max_tokens=1000,
            n=5,
            stop=None,
            temperature=0.5
        )

        results = [choice['text'].strip() for choice in response['choices']]

    return render_template('index.html', form=form, results=results)


if __name__ == '__main__':
    app.run(debug=True)