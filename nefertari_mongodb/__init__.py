import logging

import mongoengine

from .documents import (
    BaseDocument, ESBaseDocument, BaseMixin,
    get_document_cls, get_document_classes)
from .serializers import JSONEncoder, ESJSONSerializer
from .metaclasses import ESMetaclass
from .utils import (
    relationship_fields, is_relationship_field,
    get_relationship_cls, objectify_acl)
from .fields import (
    BigIntegerField,
    BooleanField,
    DateField,
    DateTimeField,
    ChoiceField,
    FloatField,
    IntegerField,
    IntervalField,
    BinaryField,
    DecimalField,
    PickleField,
    SmallIntegerField,
    StringField,
    TextField,
    TimeField,
    UnicodeField,
    UnicodeTextField,
    Relationship,
    IdField,
    ForeignKeyField,

    ListField,
    DictField,
    ACLField,
)


log = logging.getLogger(__name__)


def includeme(config):
    """ Include required packages. """
    pass


def setup_database(config):
    """ Setup db engine and db itself. Create db if it doesn't exist. """
    settings = config.registry.settings
    mongoengine.connect(settings['mongodb.db'],
                        host=settings['mongodb.host'],
                        port=int(settings['mongodb.port']))
