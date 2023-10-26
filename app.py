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
import requests
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # change this to your secret key
openai.api_key = os.getenv('KEY')
openai.api_base = "https://gpt666.eu.org/v1"
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

            #url_detail = f"https://www.amazon.com/product-reviews/{asin}/ref=cm_cr_arp_d_paging_btm_next_{page_number}?ie=UTF8&reviewerType=all_reviews&pageNumber={page_number}"

            try:
                url_detail1 = f"https://www.amazon.com/product-reviews/{asin}/ref=cm_cr_unknown?ie=UTF8&reviewerType=all_reviews&filterByStar=one_star&pageNumber=1"
                print(url_detail1)
                params = {
                    'token': token,
                    'scraper': 'amazon-product-reviews',
                    'format': 'json',
                    'url': url_detail1,
                }
                response = requests.get('https://api.crawlbase.com/', params=params)
                data = response.json()
                if 'body' in data and 'reviews' in data['body']:
                    reviews.extend(item['reviewText'] for item in data['body']['reviews'] if (len(item['reviewText']) > 36 & len(item['reviewText'])<800))
            except:
                continue
            try:
                url_detail1 = f"https://www.amazon.com/product-reviews/{asin}/ref=cm_cr_unknown?ie=UTF8&reviewerType=all_reviews&filterByStar=five_star&pageNumber=1"
                params = {
                    'token': token,
                    'scraper': 'amazon-product-reviews',
                    'format': 'json',
                    'url': url_detail1,
                }
                response = requests.get('https://api.crawlbase.com/', params=params)
                data = response.json()
                if 'body' in data and 'reviews' in data['body']:
                    reviews.extend(item['reviewText'] for item in data['body']['reviews'] if len(item['reviewText']) > 36 & len(item['reviewText'])<800)
            except:
                continue
                
            try:
                url_detail1 = f"https://www.amazon.com/product-reviews/{asin}/ref=cm_cr_unknown?ie=UTF8&reviewerType=all_reviews&filterByStar=two_star&pageNumber=1"
                params = {
                    'token': token,
                    'scraper': 'amazon-product-reviews',
                    'format': 'json',
                    'url': url_detail1,
                }
                response = requests.get('https://api.crawlbase.com/', params=params)
                data = response.json()
                if 'body' in data and 'reviews' in data['body']:
                    reviews.extend(item['reviewText'] for item in data['body']['reviews'] if (len(item['reviewText']) > 36 & len(item['reviewText'])<800))
            except:
                continue
            try:
                url_detail1 = f"https://www.amazon.com/product-reviews/{asin}/ref=cm_cr_unknown?ie=UTF8&reviewerType=all_reviews&filterByStar=three_star&pageNumber=1"
                params = {
                    'token': token,
                    'scraper': 'amazon-product-reviews',
                    'format': 'json',
                    'url': url_detail1,
                }
                response = requests.get('https://api.crawlbase.com/', params=params)
                data = response.json()
                if 'body' in data and 'reviews' in data['body']:
                    reviews.extend(item['reviewText'] for item in data['body']['reviews'] if (len(item['reviewText']) > 36 & len(item['reviewText'])<800))
            except:
                continue
            try:
                url_detail1 = f"https://www.amazon.com/product-reviews/{asin}/ref=cm_cr_unknown?ie=UTF8&reviewerType=all_reviews&filterByStar=four_star&pageNumber=1"
                params = {
                    'token': token,
                    'scraper': 'amazon-product-reviews',
                    'format': 'json',
                    'url': url_detail1,
                }
                response = requests.get('https://api.crawlbase.com/', params=params)
                data = response.json()
                if 'body' in data and 'reviews' in data['body']:
                    reviews.extend(item['reviewText'] for item in data['body']['reviews'] if (len(item['reviewText']) > 36 & len(item['reviewText'])<800))
            except:
                continue
            # try:
            #     url_detail1 = f"https://www.amazon.com/product-reviews/{asin}/ref=cm_cr_unknown?ie=UTF8&reviewerType=all_reviews&filterByStar=four_star&pageNumber=2"
            #     params = {
            #         'token': token,
            #         'scraper': 'amazon-product-reviews',
            #         'format': 'json',
            #         'url': url_detail1,
            #     }
            #     response = requests.get('https://api.crawlbase.com/', params=params)
            #     data = response.json()
            #     if 'body' in data and 'reviews' in data['body']:
            #         reviews.extend(item['reviewText'] for item in data['body']['reviews'] if (len(item['reviewText']) > 36 & len(item['reviewText'])<800))
            # except:
            #     continue

            if 'body' in data and 'productReviewTop' in data['body']:
                product_review_top = data['body']['productReviewTop']
                print(product_review_top)

        reviews_text = '\n'.join(reviews)


        url = "http://120.79.81.153/api/conversation/talk"

        headers = {
            "Content-Type": "application/json",
        }

        data = {
            "prompt": "作为nlp算法模型，分析以下产品信息及评论，找出该产品的用户需求点，格式要求：以分析报告的格式输出且是markdown格式的，层次清晰，重点突出，包含h1标题（产品设计优化方向分析报告）、小字体产品名（简称）、h2摘要、h2主要发现（每条发现标题加粗），主要发现下面增加一条引用的评论,并指出有多少条相似观点、h2结论与建议；产品信息及评论如下：产品信息："+reviews_text,
            "model": "gpt-4-plugins",
            "message_id": str(uuid.uuid4()),  # 自动生成UUID
            "parent_message_id": str(uuid.uuid4()),  # 首次请求时生成新的UUID，之后可根据需要更新
            "stream":False
        }
        print(reviews_text)

        if len(reviews_text)<20000:
            response = requests.post(url, headers=headers, json=data,timeout=3000)
            if response.status_code == 200:
                result = response.json()
                results =  response.json()['message']['content']['parts'][0]
                print(result)
            else:
                print("请求失败:", response.status_code, response.text)
        else:
            chat_completion = openai.ChatCompletion.create(
            model="gpt-4-32k", messages=[{"role": "user", "content": "作为nlp算法模型，分析以下产品信息及评论，找出该产品的用户需求点，格式要求：以分析报告的格式输出且是markdown格式的，层次清晰，重点突出，包含h1标题（产品设计优化方向分析报告）、小字体产品名（简称）、h2摘要、h2主要发现（每条发现标题加粗），主要发现下面增加一条引用的评论,并指出有多少条相似观点、h2结论与建议；产品信息及评论如下：产品信息："+reviews_text}],timeout=3200.0)
            results = chat_completion.choices[0]['message']['content']
            print(results)

    return render_template('index.html', form=form, results=results,stars=product_review_top)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
