from rest_framework import serializers
from ..models import Board, Task, Stage, SubTask
from django.contrib.auth import get_user_model
from django.urls import reverse, NoReverseMatch


class UserSerializer(serializers.ModelSerializer):
    # tasks = serializers.HyperlinkedRelatedField(many=True, view_name='task-detail', read_only=True)
    class Meta:
        model = get_user_model()
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
        }


class SubTaskSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='subtask-detail', lookup_field='id')
    assignees = UserSerializer(many=True, read_only=True)

    class Meta:
        model = SubTask
        fields = '__all__'

    def create(self, validated_data):
        Task = validated_data['Task']
        
        # Calculate the next order value based on existing tasks in the same stage
        next_order = Task.objects.filter(Task=Task).count() + 1
        validated_data['order'] = next_order

        subtask = super().create(validated_data)
        return subtask


class TaskSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(view_name='task-detail', lookup_field='id')
    assignees = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        stage = validated_data['stage']
        
        # Calculate the next order value based on existing tasks in the same stage
        next_order = Task.objects.filter(stage=stage).count() + 1
        validated_data['order'] = next_order

        task = super().create(validated_data)
        return task


class StageSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='stage-detail',
        lookup_field='pk'      # (('name', 'name'), ('board.id', 'id'))
    )
    tasks = TaskSerializer(many=True, read_only=True)
    class Meta:
        model = Stage
        fields = ['name', 'url', 'createdat', 'updatedat', 'board', 'tasks', 'order']
        read_only_fields = ['board']

    def create(self, validated_data):
        # Extract the board instance from the context
        board = self.context.get('board')

        # Calculate the next order value based on existing tasks in the same stage
        # next_order = Task.objects.filter(board=board).count() + 1
        # validated_data['order'] = next_order

        # Ensure that the board instance is available
        if board is None:
            raise serializers.ValidationError("Board instance is required for creating a stage.")

        # Set the board field before creating the stage
        validated_data['board'] = board

        # Create the stage
        stage = Stage.objects.create(**validated_data)

        return stage


class BoardSerializer(serializers.HyperlinkedModelSerializer):

    url = serializers.HyperlinkedIdentityField(
        view_name='board-detail',       #  board-retrieve-update-destroy
        # lookup_field='id',
    )
    stages = StageSerializer(many=True)
    admins = UserSerializer(many=True, required=False)
    members = UserSerializer(many=True, required=False)

    class Meta:
        model = Board
        fields = ['id', 'url', 'name', 'admins', 'members', 'stages']

    def create(self, validated_data):
        print(f"Request Data: {self.context['request'].data}")
        print(f"validated_data: {validated_data}")
        # Extract creator from the request
        creator = self.context['request'].user if 'request' in self.context else None

        # Set the creator as an admin
        # admins_data = [{'id': creator.id}] if creator else []
        # validated_data['admins'] = admins_data

        stages_data = validated_data.pop('stages', [])
        print(f"stages_data: {stages_data}")

        board = Board.objects.create(**validated_data)

        # # Add admins and members to the board
        # board.admins.add(self.request.user)

        # Set the admins using the set() method
        if creator:
            board.admins.set([creator])

        stage_serializer = StageSerializer(data=stages_data, many=True, context={'board': board})
        stage_serializer.is_valid(raise_exception=True)
        stage_serializer.save()

        # stage_objects = []
        # for stage_name in stage_data:
        #     stage_objects.append(Stage(name=stage_name, board=board))
        # stage_objects = [Stage(board=board, **stage_data) for stage_data in stages_data]

        # Stage.objects.bulk_create(stage_objects)

        return board
    
    def update(self, instance, validated_data):
        stages_data = validated_data.pop('stages', [])

        # Update board fields
        instance.name = validated_data.get('name', instance.name)
        instance.save()

        # Update or create columns
        for stage_data in stages_data:
            stage_id = stage_data.get('id')
            if stage_id:
                # If stage ID exists, update the existing stage
                stage = Stage.objects.get(id=stage_id, board=instance)
                stage.name = stage_data.get('name', stage.name)
                stage.save()
            else:
                # If no stage ID, create a new stage
                Stage.objects.create(board=instance, **stage_data)

        return instance
    
    def _get_users_by_username(self, users_data):
        User = get_user_model()
        usernames = [user_data['username'] for user_data in users_data]
        existing_users = []
        for username in usernames:
            existing_users.append(User.objects.get(username=username))
        return existing_users


        # User = get_user_model()
        # usernames = [user_data['username'] for user_data in users_data]
        # return User.objects.filter(username_in=usernames)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for field in ['admins', 'members']:
            if data[field] is None:
                data[field] = []
        return data