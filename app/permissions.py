from rest_framework import permissions

class TMPermissions(permissions.BasePermission):
    '''
    This determines whether a user is authorized to create modules,edit modules,delete modules
    '''

    def has_permission(self, request, view):
        if request.user.user_type == 'TM':
            return True
        elif request.user.user_type == 'STUD':
            return False
        else:
            return False