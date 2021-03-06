from collections import OrderedDict
from plenum.common.messages.fields import NonNegativeNumberField, \
    IterableField, NonEmptyStringField
from plenum.common.messages.node_messages import ViewChangeDone

EXPECTED_ORDERED_FIELDS = OrderedDict([
    ("viewNo", NonNegativeNumberField),
    ("name", NonEmptyStringField),
    ("ledgerInfo", IterableField)
])


def test_hash_expected_type():
    assert ViewChangeDone.typename == "VIEW_CHANGE_DONE"


def test_has_expected_fields():
    actual_field_names = OrderedDict(ViewChangeDone.schema).keys()
    assert actual_field_names == EXPECTED_ORDERED_FIELDS.keys()


def test_has_expected_validators():
    schema = dict(ViewChangeDone.schema)
    for field, validator in EXPECTED_ORDERED_FIELDS.items():
        assert isinstance(schema[field], validator)
