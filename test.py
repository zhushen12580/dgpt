import requests

params = (
    ('token', 'WyAsI2Zt0_tDshEfS95ccg'),
    ('scraper', 'amazon-product-reviews'),
    ('format', 'json'),
    ('url', 'https://www.amazon.com/PandaEar-Silicone-Babies-Toddlers-Waterproof/product-reviews/B08GFCX964/ref=cm_cr_getr_d_paging_btm_prev_1?ie=UTF8&reviewerType=all_reviews'),
)

response = requests.get('https://api.crawlbase.com/', params=params)
data = response.json()
reviews = [item['reviewText'] for item in data['body']['reviews']]
#列表转字符串
reviews = ''.join(reviews)
print(reviews)