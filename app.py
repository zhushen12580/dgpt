# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
import openai
from flask import Flask, request, send_file
from io import BytesIO
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # change this to your secret key
openai.api_key = os.getenv('KEY')
token = os.getenv('TOKEN')



class URLForm(FlaskForm):
    url = StringField('', validators=[DataRequired()])
    submit = SubmitField('确认')

@app.route('/')
def welcome():
    return render_template('welcome.html')  # The welcome.html is your new welcome page

@app.route('/index', methods=['GET', 'POST'])
def index():
    form = URLForm()
    results = None
    product_review_top = []
    if form.validate_on_submit():
        urls = form.url.data.splitlines()#
        reviews = []
        for url in urls:
            asin_start_index = url.find('/dp/') + 4
            asin_end_index = url.find('/', asin_start_index)
            asin = url[asin_start_index:asin_end_index]
            page_number = 1
            
            while page_number<9:
                url_detail = f"https://www.amazon.com/product-reviews/{asin}/ref=cm_cr_arp_d_paging_btm_next_{page_number}?ie=UTF8&reviewerType=all_reviews&pageNumber={page_number}"
                params = {
                    'token': token,
                    'scraper': 'amazon-product-reviews',
                    'format': 'json',
                    'url': url_detail,
                }
                response = requests.get('https://api.crawlbase.com/', params=params)
                data = response.json()
                if 'body' in data and 'reviews' in data['body']:
                    reviews.extend(item['reviewText'] for item in data['body']['reviews'] if len(item['reviewText']) > 36)
                if data['body']['pagination']['nextPage']=='null':
                    break
                if 'body' in data and 'productReviewTop' in data['body']:
                    product_review_top = data['body']['productReviewTop']
                page_number += 1

        reviews_text = '\n'.join(reviews)

        # 使用 OpenAI ChatGPT 处理评论文本
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "作为nlp算法模型，分析以下产品信息及评论，找出该产品的用户需求点及产品优化空间，格式要求：以分析报告的格式输出且是markdown格式的，层次清晰，简洁明要，包含h1标题（产品设计优化方向分析报告）、小字体产品名（简称）、h2摘要、h2主要发现（每条发现标题加粗），主要发现下面增加一条引用的评论、h2结论与建议；产品信息及评论如下："},
                      {"role": "user", "content": reviews_text}]
        )

        results = response['choices'][0]['message']['content']

    return render_template('index.html', form=form, results=results,stars=product_review_top)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)