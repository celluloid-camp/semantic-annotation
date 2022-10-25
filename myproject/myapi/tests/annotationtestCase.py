
import unittest
from django.test import Client
from django.urls import reverse

class AnnotationTest(unittest.TestCase):

 def test_get_annotation(self):
      # Get Annotation.
      self.client = Client()
      response = self.client.get('/ontology?idAnnotation=1')
      self.assertEqual(response.status_code, 200)
      self.assertEqual(response.json()['concept'], "Staging")
def test_post_annotation(self):
        # Create Annotation.
      self.client = Client()
      response = self.client.post('/annotation/', {
          'projectId': 'projet1',
           'userId': 'ryma',
           'commentaire': '',
           'stopTime': '1',
           'startTime': '2',
           'objet':"['Staging']",
           'userName': 'Ryma boussaha',
          'relation': 'hasStaging',
         'annotationId': '117'})
      self.assertEqual(response.status_code, 404)
if __name__ == '__main__':
  unittest.main()