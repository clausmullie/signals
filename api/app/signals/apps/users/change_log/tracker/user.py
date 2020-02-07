from django.contrib.gis.db import models

from change_log.tracker import BaseChangeTracker


class UserChangeTracker(BaseChangeTracker):
    def changed_data(self):
        """
        Override the default ChangeTracker.

        This custom ChangeTracker for Users is used to make sure the changes are stored correctly in the JSON
        field (data) of the change_log.
        """
        _changed_data = dict()  # Here we are going to keep track of the changes

        for field in self.instance._meta.get_fields():
            # The value of the field that is currently saved to the database
            if isinstance(field, (models.OneToOneRel)):
                continue
            elif isinstance(field, (models.ManyToManyRel, models.ManyToOneRel)):
                field_name = field.get_accessor_name()
                new_value = list(getattr(self.instance, field_name).values_list('pk', flat=True))
            elif isinstance(field, (models.ManyToManyField)):
                field_name = field.name
                new_value = list(getattr(self.instance, field_name).values_list('pk', flat=True))
            else:
                field_name = field.name
                new_value = getattr(self.instance, field_name)

            # Contains the value the field had when the instance was initialized
            prev_value = self.data.get(field_name)

            # Duh! Let's check if the values are different
            if new_value != prev_value:
                # Let's do some magic
                if isinstance(field, (models.CharField, models.TextField, models.BooleanField)):
                    # Let's just use the json representation of these fields
                    _changed_data[field_name] = new_value
                elif isinstance(field, (models.ManyToManyRel, models.ManyToOneRel, models.ManyToManyField)):
                    new_value = new_value or []
                    prev_value = prev_value or []
                    _changed_data[field_name] = list(set(new_value) - set(prev_value))

        return _changed_data
