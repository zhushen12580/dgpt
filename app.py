from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import openai
from flask import Flask, request, send_file
from io import BytesIO
import pdfkit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # change this to your secret key
openai.api_key = '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'  # change this to your OpenAI API key


class URLForm(FlaskForm):
    url = StringField('', validators=[DataRequired()])
    submit = SubmitField('确认')


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
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "作为nlp算法模型，分析以下产品信息及评论，找出该产品的用户需求点，格式要求：以分析报告的格式输出且是markdown格式的，层次清晰，重点突出，包含h1标题（产品设计优化方向分析报告）、小字体产品名（简称）、h2摘要、h2主要发现（每条发现标题加粗），主要发现下面增加一条引用的评论、h2结论与建议；产品信息及评论如下："},
                      {"role": "user", "content": reviews_text}]
        )

        results = response['choices'][0]['message']['content']

    return render_template('index.html', form=form, results=results)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
