import django_filters
from user.models import User


class UserFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = User
        fields = {
            'id': ['exact', 'in', ],
            'name': ['exact', 'in','contains' ],
            'password': ['exact', 'in', ],
            'token': ['exact', 'in', ],
        }

