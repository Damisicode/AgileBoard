from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .serializers import UserSerializer, BoardSerializer, StageSerializer, TaskSerializer, SubTaskSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import generics, status
from ..models import Board, Stage, Task, SubTask
from rest_framework.permissions import IsAuthenticated
from .permissions import IsBoardAdminOrReadOnly, IsBoardAdmin, IsBoardMember, IsStageMember
from rest_framework.views import APIView


class UserViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def list(self, request):
        queryset = get_user_model().objects.all()
        serializer = UserSerializer(queryset, context={'request': request}, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = get_user_model().objects.all()
        user = get_object_or_404(queryset, id=pk)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)
    

    class Meta:
        fields = ['id', 'username', 'email']


class BoardListCreateAPIView(generics.ListCreateAPIView):
    """
    Concrete Generic view for Getting all Boards and Creating new board
    """

    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated, IsBoardMember]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # Call the custom create method
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        # Call the custom create method from the serializer
        serializer.save()


class BoardRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Concrete Generic view for getting each board, updating the board, and deleting the board
    """

    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated, IsBoardMember]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Check if the user making the request is an admin of the board
        if request.user not in instance.admins.all():
            return Response({"detail": "You do not have permission to delete this board."}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class BoardMemberAPIView(generics.GenericAPIView):
    """
    Generic API view for adding and removing member from a board
    """

    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated, IsBoardAdminOrReadOnly]

    def get_object(self):
        return generics.get_object_or_404(Board, id=self.kwargs['id'])
    
    def post(self, request, id, action):
        board = self.get_object()
        username = request.data.get('username')

        if action == 'add_member' and IsBoardAdmin().has_object_permission(request, self, board):
            # Add member to the board
            if username:
                user = generics.get_object_or_404(get_user_model(), username=username)

                if user not in board.members.all():
                    board.members.add(user)
                    return Response({'detail': 'Member added successfully.'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'detail': 'User is already a member of the board.'}, status=status.HTTP_400_BAD_REQUEST)
                
            else:
                return Response({'detail': 'username is required.'}, status=status.HTTP_400_BAD_REQUEST)
            
        elif action == 'remove_member' and IsBoardAdmin().has_object_permission(request, self, board):
            # Remove member from the board
            if username:
                user = generics.get_object_or_404(get_user_model(), id=username)

                if user in board.members.all():
                    board.members.remove(user)
                    return Response({'detail': 'Member removed successfully.'}, status=status.HTTP_200_OK)
                
                else:
                    return Response({'detail': 'User is not a member of the board.'}, status=status.HTTP_400_BAD_REQUEST)
                
            else:
                return Response({'detail': 'User ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)


class BoardAdminAPIView(generics.GenericAPIView):
    """
    Generic API view for adding and removing admin from a board
    """

    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    permission_classes = [IsAuthenticated, IsBoardAdminOrReadOnly]

    def get_object(self):
        return generics.get_object_or_404(Board, id=self.kwargs['id'])
    
    def post(self, request, id, action):
        board = self.get_object()
        username = request.data.get('username')

        if action == 'add_admin' and IsBoardAdmin().has_object_permission(request, self, board):
            # Add admin to the board
            if username:
                user = generics.get_object_or_404(get_user_model(), username=username)

                if user not in board.admins.all():
                    board.admins.add(user)
                    return Response({'detail': 'Admin added successfully.'}, status=status.HTTP_201_CREATED)
                else:
                    return Response({'detail': 'User is already a admin of the board.'}, status=status.HTTP_400_BAD_REQUEST)
                
            else:
                return Response({'detail': 'username is required.'}, status=status.HTTP_400_BAD_REQUEST)
            
        elif action == 'remove_admin' and IsBoardAdmin().has_object_permission(request, self, board):
            # Remove member from the board
            if username:
                user = generics.get_object_or_404(get_user_model(), id=username)

                if user in board.admins.all():
                    board.admins.remove(user)
                    return Response({'detail': 'Admin removed successfully.'}, status=status.HTTP_200_OK)
                
                else:
                    return Response({'detail': 'User is not a admin of the board.'}, status=status.HTTP_400_BAD_REQUEST)
                
            else:
                return Response({'detail': 'User ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)


class StageDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Generic View to Retrieve, Update, and Destroy a Stage in a board
    """

    queryset = Stage.objects.all()
    serializer_class = StageSerializer
    permission_classes = [IsAuthenticated, IsStageMember]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Check if the user making the request is an admin of the board
        if request.user not in instance.board.admins.all():
            return Response({"detail": "You do not have permission to delete this board."}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class StageListView(generics.ListCreateAPIView):
    """
    Generic View to List and create stage in a board
    """

    queryset = Stage.objects.all()
    serializer_class = StageSerializer
    permission_classes = [IsAuthenticated, IsBoardMember]

    def get_queryset(self):
        """ Function to get the filter stages for a particular board """

        board_id = self.kwargs['pk']
        board = get_object_or_404(Board, id=board_id)
        return Stage.objects.filter(board=board)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Generic view to Retrieve, Update, and Delete a Task
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsBoardMember]
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Check if the user making the request is an admin of the board
        if request.user not in instance.stage.board.admins.all():
            return Response({"detail": "You do not have permission to delete this board."}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def get_board(self):
        return get_object_or_404(Task, id=self.kwargs.get('id')).stage.board


class TaskListView(generics.ListCreateAPIView):
    """
    Generic view to List and create a task in a particular stage
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsBoardMember]

    def get_queryset(self):
        """ Function to filter tasks for a particular Stage """

        stage_id = self.kwargs.get('stage_id')
        stage = get_object_or_404(Stage, id=stage_id)
        return Task.objects.filter(stage=stage)
    
    def get_board(self):
        return get_object_or_404(Stage, id=self.kwargs.get('stage_id')).board


class AssignTaskToUserAPIView(generics.UpdateAPIView):
    """
    Generic API view to update the members assigned to a particular task
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsBoardAdmin]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        task = self.get_object()
        usernames = request.data.get('usernames', [])

        users = get_user_model().objects.filter(username__in=usernames)
        task.assignees.set(users)

        return Response({'detail': 'Task assigned successfully.'}, status=status.HTTP_200_OK)
    
    def get_board(self):
        return get_object_or_404(Task, id=self.kwargs.get('id')).stage.board
    

class SubTaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Generic view to Retrieve, Update, and Delete a Task
    """

    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    permission_classes = [IsAuthenticated, IsBoardMember]
    lookup_field = 'id'

    def get_board(self):
        return get_object_or_404(SubTask, id=self.kwargs.get('id')).task.stage.board


class SubTaskListView(generics.ListCreateAPIView):
    """
    Generic view to List and create a task in a particular stage
    """

    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    permission_classes = [IsAuthenticated, IsBoardMember]

    def get_queryset(self):
        """ Function to filter tasks for a particular Stage """

        task_id = self.kwargs.get('task_id')
        task = get_object_or_404(Task, id=task_id)
        return SubTask.objects.filter(task=task)
    
    def get_board(self):
        return self.get_object().task.stage.board


class AssignSubTaskToUserAPIView(generics.UpdateAPIView):
    """
    Generic API view to update the members assigned to a particular task
    """
    
    queryset = Task.objects.all()
    serializer_class = SubTaskSerializer
    permission_classes = [IsAuthenticated, IsBoardAdmin]
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        subtask = self.get_object()
        user_ids = request.data.get('user_ids', [])

        users = get_user_model().objects.filter(id__in=user_ids)
        subtask.assignees.set(users)

        return Response({'detail': 'SubTask assigned successfully.'}, status=status.HTTP_200_OK)
    
    def get_board(self):
        return get_object_or_404(SubTask, id=self.kwargs.get('id')).task.stage.board


class ChangeTaskStageView(APIView):
    """
    APIView to change the stage of the tasks
    """
    
    permission_classes = [IsAuthenticated, IsBoardAdmin]

    def put(self, request, task_id, new_stage_id):
        try:
            task = get_object_or_404(Task, id=task_id)
            new_stage = get_object_or_404(Stage, id=new_stage_id)
        except Task.DoesNotExist or Stage.DoesNotExist:
            return Response({"detail": "Task or Stage not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Update the task's stage
        task.stage = new_stage
        task.save()

        # Serialize and return the updated task
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)