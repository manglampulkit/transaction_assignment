from django.urls import path

from .views import (
    TransactionCreateView,
    UserSummaryView,
    RankingView,
    home_page,
    summary_page,
    ranking_page
)

urlpatterns = [

    path('', home_page, name='home'),

    path(
        'summary-page/',
        summary_page,
        name='summary-page'
    ),

    path(
        'ranking-page/',
        ranking_page,
        name='ranking-page'
    ),

    path(
        'transaction/',
        TransactionCreateView.as_view(),
        name='transaction'
    ),

    path(
        'summary/<str:user_id>/',
        UserSummaryView.as_view(),
        name='summary'
    ),

    path(
        'ranking/',
        RankingView.as_view(),
        name='ranking'
    ),
]