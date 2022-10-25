
import unittest
from django.test import Client
from django.urls import reverse

class OntologyTest(unittest.TestCase):
    def test_get_globalConcept(self):
        # Create Annotation.
        self.client = Client()
        response = self.client.get('/concept')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['concept'], [
        "Emotion",
        "Staging",
        "Acting",
        "Dramaturgy",
        "Judgement",
        "Annotation Libre"
    ])

    def test_get_subConcept(self):
        # Create Annotation.
        self.client = Client()
        response = self.client.get('/conceptSubClass?concept=Emotion')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['concept'], [
        "PhysicalSensation",
        "Involvement",
        "Feeling"
    ])
if __name__ == '__main__':
  unittest.main()