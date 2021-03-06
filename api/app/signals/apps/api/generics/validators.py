from rest_framework.serializers import ValidationError

from signals.apps.signals.models import Signal


class NearAmsterdamValidatorMixin:

    def validate_geometrie(self, value):
        fail_msg = 'Location coordinates not anywhere near Amsterdam. (in WGS84)'

        lat_not_in_adam_area = not 50 < value.coords[1] < 55
        lon_not_in_adam_area = not 1 < value.coords[0] < 7

        if lon_not_in_adam_area or lat_not_in_adam_area:
            raise ValidationError(fail_msg)
        return value


class SignalSourceValidator(object):
    def __init__(self, *args, **kwargs):
        self.serializer_field = None

    def __call__(self, value):
        user = self.serializer_field.context['request'].user

        # If there is no user only the Signal.SOURCE_DEFAULT_ANONYMOUS_USER can be given as a source
        if not user and value.lower() != Signal.SOURCE_DEFAULT_ANONYMOUS_USER:
            raise ValidationError('Invalid source given for anonymous user')

        # If there is no user and the previous check did not raised an ValidationError we can use
        # the value. Otherwise we need to do some more checks
        if not user:
            return value

        # If the user is not authenticated only the Signal.SOURCE_DEFAULT_ANONYMOUS_USER can be
        # given as a source
        if not user.is_authenticated and value.lower() != Signal.SOURCE_DEFAULT_ANONYMOUS_USER:
            raise ValidationError('Invalid source given for anonymous user')

        # If the user is authenticated the Signal.SOURCE_DEFAULT_ANONYMOUS_USER CANNOT be given
        # as a source
        if user.is_authenticated and value.lower() == Signal.SOURCE_DEFAULT_ANONYMOUS_USER:
            raise ValidationError('Invalid source given for authenticated user')

        return value

    def set_context(self, serializer_field):
        self.serializer_field = serializer_field
