from django.apps import AppConfig


class EsSearchConfig(AppConfig):
    name = 'es_search'

    def ready(self):
        import es_search.signals


