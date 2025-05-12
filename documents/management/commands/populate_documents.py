from django.core.management.base import BaseCommand
from documents.models import Document
import json
from django.utils import timezone
from datetime import timedelta
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Заполняет модель Document тестовыми данными.'

    def handle(self, *args, **options):
        Document.objects.all().delete()

        documents = [
            {
                'rubrics': json.dumps({"category": "test1"}),
                'text': "Тестовый документ 1",
                'created_date': timezone.now() - timedelta(days=2)
            },
            {
                'rubrics': json.dumps({"category": "test2"}),
                'text': "Тестовый документ 2",
                'created_date': timezone.now() - timedelta(days=1)
            },
            {
                'rubrics': json.dumps({"category": "test3"}),
                'text': "Тестовый документ 3",
                'created_date': timezone.now()
            },
        ]

        for doc_data in documents:
            Document.objects.create(**doc_data)
            self.stdout.write(self.style.SUCCESS(f'Создан документ с текстом: {doc_data["text"]}'))

        call_command('search_index', '--populate')
        self.stdout.write(self.style.SUCCESS('Успешно заполнены документы и обновлён индекс Elasticsearch.'))
