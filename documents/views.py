from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Document
from .serializers import DocumentSerializer
from django_elasticsearch_dsl.search import Search


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all().order_by('-created_date')[:20]
    serializer_class = DocumentSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        """Выполняет поиск документов по тексту с использованием Elasticsearch."""
        query = request.query_params.get('q', '')
        if not query:
            return Response({"error": "Query parameter 'q' is required"}, status=400)
        s = Search(index='documents').query("multi_match", fields=['text'], query=query)
        response = s.execute()
        hits = response.hits.hits
        if not hits:
            return Response({"message": "No documents found"}, status=200)
        document_ids = [hit['_id'] for hit in hits]
        documents = Document.objects.filter(id__in=document_ids).order_by('-created_date')[:20]
        serializer = self.get_serializer(documents, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """Удаляет документ из базы данных и индекса Elasticsearch."""
        instance = self.get_object()
        from django_elasticsearch_dsl.registries import registry
        registry.update(instance)
        registry.delete(instance)
        self.perform_destroy(instance)
        return Response(status=204)
