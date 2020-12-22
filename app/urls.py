from django.urls import path

from app.views import IndexView, RevokeView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('revoke/', RevokeView.as_view(), name='revoke-self'),
    path('revoke/<int:entry_id>/', RevokeView.as_view(), name='revoke'),
]
