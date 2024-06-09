from django.contrib import admin
from django.urls import path

from server.views.GIGreenIndexView import getGIGreenIndexAPIView
from server.views.CuttingTreeView import getCuttingTreeImageAPIView
from server.views.HSIIndexView import getHSIIndexAPIView
from server.views.ColorNDVIView import getColorNDVIAPIView
from server.views.NDVIView import getNDVIAPIView
from server.views.SearchHoogweedView import getHoogweedAPIView

urlpatterns = [
    path('api/v1/getColorNDVI/', getColorNDVIAPIView.as_view()),
    path('api/v1/getNDVI/', getNDVIAPIView.as_view()),
    path('api/v1/getHSI/', getHSIIndexAPIView.as_view()),
    path('api/v1/getGIGreen/', getGIGreenIndexAPIView.as_view()),
    path('api/v1/getCuttingTreeImage/', getCuttingTreeImageAPIView.as_view()),
    path('api/v1/getHoogweed/', getHoogweedAPIView.as_view())

]
