import logging

from mongoengine import signals
from nefertari.utils import to_dicts


log = logging.getLogger(__name__)


def on_post_save(sender, document, **kw):
    """ Add new document to index or update existing. """
    from nefertari.elasticsearch import ES
    created = kw.get('created', False)
    if created:
        ES(document.__class__.__name__).index(document.to_dict())
    elif not created and document._get_changed_fields():
        document.reload()
        ES(document.__class__.__name__).index(document.to_dict())


def on_post_delete(sender, document, **kw):
    from nefertari.elasticsearch import ES
    ES(document.__class__.__name__).delete(document.id)


def on_bulk_update(model_cls, objects):
    if not getattr(model_cls, '_index_enabled', False):
        return

    if not objects:
        return

    from nefertari.elasticsearch import ES
    es = ES(source=model_cls.__name__)
    documents = to_dicts(objects)
    es.index(documents)

    # Reindex relationships
    for obj in objects:
        es.index_refs(obj)


def setup_es_signals_for(source_cls):
    signals.post_save.connect(on_post_save, sender=source_cls)
    signals.post_delete.connect(on_post_delete, sender=source_cls)
    log.info('setup_es_signals_for: %r' % source_cls)
