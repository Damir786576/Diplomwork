import time
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Document
import json
from django.utils import timezone
from datetime import timedelta
from django.core.management import call_command
import pytest
from .dsl import DocumentDocument


class DocumentTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        call_command('search_index', '--rebuild', '--force')
        time.sleep(5)

    def setUp(self):
        self.client = APIClient()
        call_command('search_index', '--delete', '--force')
        call_command('search_index', '--rebuild', '--force')
        time.sleep(5)
        self.doc1 = Document.objects.create(
            rubrics=json.dumps({"category": "test1"}),
            text="Тестовый документ 1",
            created_date=timezone.now() - timedelta(days=2)
        )
        self.doc2 = Document.objects.create(
            rubrics=json.dumps({"category": "test2"}),
            text="Тестовый документ 2",
            created_date=timezone.now() - timedelta(days=1)
        )
        self.doc3 = Document.objects.create(
            rubrics=json.dumps({"category": "test3"}),
            text="Тестовый документ 3",
            created_date=timezone.now()
        )
        call_command('search_index', '--populate')
        time.sleep(5)

    def test_document_list(self):
        url = reverse('document-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        response_ids = [int(doc['id']) for doc in response.data]
        self.assertEqual(response_ids[0], self.doc3.id)
        print(f"Response IDs: {response_ids}, doc3.id: {self.doc3.id}")

    def test_search_document(self):
        url = reverse('document-search') + '?q=Тестовый'
        time.sleep(5)
        response = self.client.get(url)
        print(f"Search response: {response.data}, status: {response.status_code}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        response_ids = [int(doc['id']) for doc in response.data]
        self.assertEqual(response_ids[0], self.doc3.id)

    def test_search_empty_query(self):
        url = reverse('document-search') + '?q='
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "Query parameter 'q' is required"})

    def test_search_no_results(self):
        url = reverse('document-search') + '?q=несуществующий'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "No documents found"})

    def test_delete_nonexistent_document(self):
        url = reverse('document-detail', kwargs={'pk': 9999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


@pytest.mark.django_db
def test_document_index():
    doc = DocumentDocument()
    assert doc._index._name == 'documents'
