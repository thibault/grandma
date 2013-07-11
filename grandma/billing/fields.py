from django.db import models


class CurrencyField(models.DecimalField):
    """Store currencies."""

    def __init__(self, *args, **kwargs):
        kwargs.update({
            'decimal_places': 2,
            'max_digits': 7,
        })
        super(CurrencyField, self).__init__(*args, **kwargs)


from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^billing\.fields\.CurrencyField"])
