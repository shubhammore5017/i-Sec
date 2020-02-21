from import_export import resources
from api.models import Chat_Logs

class ChatResource(resources.ModelResource):
    class Meta:
        model = Chat_Logs
