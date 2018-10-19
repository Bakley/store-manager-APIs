from flask import jsonify


import unittest
import app, json

from app.api.v1.models import products

class TestStoreApp(unittest.TestCase):

    """Setup the test client"""
    def setUp(self):
        app.create_app().testing = True
        self.app = app.create_app().test_client() 

        '''This data shall be used for testing purposes'''
        self.sample_data = {
            "product_id" : 1,
            "product_name" : "Soap",
            "product_price" : 450,
            "description" : "Jamaa soap Utapenda",
            "quantity" : 30,
            "product_image" : "image/d.jpg"
        } 

        products.append(self.sample_data)
        
    def test_whether_returns_status_code_on_products_query(self):
        self.assertEqual(self.app.get('/api/v1/products').status_code, 200)
    
    def test_returns_message_if_no_products(self):
        response = self.app.get('/api/v1/products')
        assert response.status_code == 200
    
    """Returns 404 if the url is malformed and does not fetch data"""
    def test_malformed_url_on_products_query(self):
        response = self.app.get('/api/v1/produc')
        self.assertEqual(response.status_code, 404)

    def test_adds_a_new_product(self):
        response = self.app.post('/api/v1/products', data = json.dumps(self.sample_data), content_type='application/json')
        self.assertEqual(response.status_code,201)

    def test_malformed_post_one_product_url(self):
        response = self.app.post('/api/v1/products//', data = json.dumps(self.sample_data), content_type='application/json')
        self.assertEqual(response.status_code,404)
    
    '''Test whether the api fetches a product successfull'''
    def test_get_a_product_by_id(self):
        response = self.app.get('/api/v1/products/1')
        self.assertEqual(response.status_code,200)

    def test_malformed_url_on_a_given_product_query_by_id(self):
        response = self.app.get('/api/v1/products/1/wsd')
        self.assertEqual(response.status_code,404)
    
    def test_gives_error_feedback_if_product_id_out_of_bounds(self):
        response = self.app.get('/api/v1/products/0')
        res = json.loads(response.data)
        self.assertEqual(res['Message'],"The product requested is not in store")