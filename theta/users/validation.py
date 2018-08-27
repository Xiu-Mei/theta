from django.core.exceptions import PermissionDenied


class OfficeAdminValidationMixin:
    def is_office_admin(self):
        if not self.request.user.is_authenticated:
            return False
        if not self.request.user.groups.filter(name='office_admins').exists():
            raise PermissionDenied

        self.office = self.request.user.office
