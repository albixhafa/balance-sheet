from import_export import fields, resources, widgets
from import_export.widgets import ForeignKeyWidget
from .models import Gldetail, Glpost, Entity, Period
from django.contrib.auth.models import User

class GldetailResource(resources.ModelResource):

    entity = fields.Field(
            column_name='entity',
            attribute = 'entity',
            widget=widgets.ForeignKeyWidget(Entity, 'entity')
    )
    
    period = fields.Field(
            column_name='period',
            attribute = 'period',
            widget=ForeignKeyWidget(Period, 'period')
    )

    username = fields.Field(
            column_name='username',
            attribute = 'username',
            widget=ForeignKeyWidget(User, 'username')
    )

    class Meta:
        model = Gldetail
        exclude = ('id')
        import_id_fields = ('entity', 'period', 'glnum')