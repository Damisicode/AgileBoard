from rest_framework import permissions

class IsBoardAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.admins.all()
    

class IsBoardMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user in obj.members.all()
    

class IsBoardAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow GET, HEAD, and OPTIONS requests for all users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Check if the user is an administrator of the board
        board = None

        # Check if the view has a 'board' attribute (e.g., BoardDetailView)
        if hasattr(view, 'board'):
            board = getattr(view, 'board')

        # Check if the view has a 'get_board' method(e.g., TaskDetailView)
        elif hasattr(view, 'get_board'):
            board = view.get_board()

        if board and request.user in board.admins.all():
            return True
        
        return False

    # def has_object_permission(self, request, view, obj):
    #     if request.method in permissions.SAFE_METHODS:
    #         # Allow read-only permissions for all users (GET, HEAD, OPTIONs)
    #         return True
    #     return IsBoardAdmin().has_object_permission(request, view, obj)