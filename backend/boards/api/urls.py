from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    BoardListCreateAPIView,
    BoardRetrieveUpdateDestroyAPIView,
    BoardMemberAPIView,
    StageListView,
    StageDetailView,
    TaskListView,
    TaskDetailView,
    AssignTaskToUserAPIView,
    SubTaskListView,
    SubTaskDetailView,
    AssignSubTaskToUserAPIView,
    ChangeTaskStageView,
)

board_router = DefaultRouter()
board_router.register(r'users', UserViewSet)

urlpatterns = [
    path('', BoardListCreateAPIView.as_view(), name='boards-list-create'),
    path('<uuid:pk>', BoardRetrieveUpdateDestroyAPIView.as_view(), name='board-detail'),
    path('<uuid:id>/add_member/', BoardMemberAPIView.as_view(), {'action': 'add_member'}, name='board-add-member'),
    path('<uuid:id>/remove_member/', BoardMemberAPIView.as_view(), {'action': 'remove_member'}, name='board-remove-member'),
    path('<uuid:pk>/stages', StageListView.as_view(), name='board-stages'),
    path('stage/<uuid:pk>', StageDetailView.as_view(), name='stage-detail'),
    path('<uuid:stage_id>/tasks/', TaskListView.as_view(), name='stage-tasks'),
    path('task/<uuid:id>', TaskDetailView.as_view(), name='task-detail'),
    path('task/<uuid:id>/assign_users/', AssignTaskToUserAPIView.as_view(), name='assign-task-to-user'),
    path('<uuid:task_id>/subtasks/', SubTaskListView.as_view(), name='stage-subtasks'),
    path('subtask/<uuid:id>', SubTaskDetailView.as_view(), name='subtask-detail'),
    path('subtask/<uuid:id>/assign_users/', AssignSubTaskToUserAPIView.as_view(), name='assign-subtask-to-user'),
    path('task/<uuid:task_id>/change-stage/<uuid:new_stage_id>/', ChangeTaskStageView.as_view(), name='change-task-stage'),
]