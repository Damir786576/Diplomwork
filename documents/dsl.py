from django_elasticsearch_dsl import Document, Index
from django_elasticsearch_dsl.registries import registry
from .models import Document as DocumentModel

document_index = Index('documents')


@registry.register_document
class DocumentDocument(Document):
    class Django:
        model = DocumentModel
        fields = [
            'id',
            'text',
        ]

    class Index:
        name = 'documents'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    def get_instances_from_related(self, related_instance):
        """Опционально, для связей."""
        return None
