from django.core.exceptions import PermissionDenied


class OfficeAdminValidationMixin:
    def is_office_admin(self):
        if not self.request.user.is_authenticated:
            self.redirect = 'account_login'
            return
        if not self.request.user.groups.filter(name='office_admins').exists():
            raise PermissionDenied

        self.office = self.request.user.office
