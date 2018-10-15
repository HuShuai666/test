# coding: utf-8
from django.conf.urls import url
from activity.views import ActivityView, ActivityStartAtView, TestView, CornView, NoticeView

urlpatterns = [
    url(r'^activity$', ActivityView.as_view()),
    url(r'^activity/start$', ActivityStartAtView.as_view()),
    url(r'^activity/test', TestView.as_view()),
    url(r'^activity/corn', CornView.as_view()),
    url(r'^activity/notice', NoticeView.as_view()),
]
