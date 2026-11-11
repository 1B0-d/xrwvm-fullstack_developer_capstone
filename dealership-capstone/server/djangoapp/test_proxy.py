import json
from unittest.mock import patch

import requests
from django.contrib.auth.models import User
from django.test import TestCase


class ProxyTests(TestCase):
    @patch('djangoapp.views.get_request')
    def test_dealers_and_details(self, get_request):
        get_request.return_value = [{'id': 3}]
        self.assertEqual(self.client.get('/djangoapp/get_dealers').json()['dealers'], [{'id': 3}])
        get_request.assert_called_with('/fetchDealers')
        self.client.get('/djangoapp/get_dealers/TX')
        get_request.assert_called_with('/fetchDealers/TX')
        self.assertEqual(self.client.get('/djangoapp/dealer/3').json()['dealer'], [{'id': 3}])
        get_request.assert_called_with('/fetchDealer/3')
        get_request.side_effect = requests.ConnectionError()
        self.assertEqual(self.client.get('/djangoapp/get_dealers').status_code, 502)

    @patch('djangoapp.views.analyze_review_sentiments', return_value={'sentiment': 'positive'})
    @patch('djangoapp.views.get_request', return_value=[{'review': 'Fantastic services'}])
    def test_reviews(self, get_request, sentiment):
        response = self.client.get('/djangoapp/reviews/dealer/3')
        self.assertEqual(response.json()['reviews'][0]['sentiment'], 'positive')
        get_request.assert_called_once_with('/fetchReviews/dealer/3')
        sentiment.assert_called_once_with('Fantastic services')

    @patch('djangoapp.views.post_review')
    def test_add_review_requires_login(self, post_review):
        url = '/djangoapp/add_review'
        self.assertEqual(self.client.post(url, '{}', content_type='application/json').status_code, 403)
        post_review.assert_not_called()
        self.client.force_login(User.objects.create_user(username='tester'))
        self.assertEqual(self.client.post(url, 'bad', content_type='application/json').status_code, 400)
        data = {'dealership': 3, 'review': 'Good'}
        self.assertEqual(self.client.post(url, json.dumps(data), content_type='application/json').json()['status'], 200)
        post_review.assert_called_once_with(data)
        post_review.side_effect = requests.ConnectionError()
        self.assertEqual(self.client.post(url, '{}', content_type='application/json').status_code, 502)

    @patch('djangoapp.restapis.requests.get')
    def test_sentiment_text_is_url_encoded(self, get):
        from .restapis import analyze_review_sentiments
        analyze_review_sentiments('A/B? good')
        url = get.call_args.args[0]
        self.assertTrue(url.endswith('/analyze/A%2FB%3F%20good'))
