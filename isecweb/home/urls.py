from django.urls import path
from . import views as view
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', view.index, name='index'),
    path('home/', view.home, name='home-page'),
    path('devreg/', view.dev_reg, name='home-dev'),
    path('telegram/', view.telegram_reg, name='home-tele'),
    path('chats/', view.chat_logs, name='home-chat-logs'),
    path('mediahistory/', view.media, name='home-media'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
