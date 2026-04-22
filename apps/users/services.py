# apps/users/services.py
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from common.services import BaseService
from common.exceptions import (
    ServiceException,
    NotFoundException, 
    PermissionDeniedException
)

User = get_user_model()


class RegisterUserService(BaseService):

    def __init__(self, email, username, password, confirm_password, phone="", role= ""):
        self.email    = email
        self.username = username
        self.password = password
        self.confirm_password = confirm_password
        self.phone = phone
        self.role = role or User.Role.MERCHANT

    def execute(self):
        self._validate()
        return self._create()

    def _validate(self):
        if self.password != self.confirm_password:
            raise ServiceException("Passwords do not match")
        
        # validate password strength
        validate_password(self.password)
        
        if User.objects.filter(email=self.email).exists():
            raise ServiceException("Email already registered")
        if User.objects.filter(username=self.username).exists():
            raise ServiceException("Username already taken")
        # admin cannot self register — only created manually
        if self.role == "admin":
            raise ServiceException("Cannot register as admin")


    def _create(self):
        return User.objects.create_user(
            email=self.email,
            username=self.username,
            password=self.password,
            phone=self.phone,
            role=self.role,
        )


class LoginUserService(BaseService):

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def execute(self):
        user = authenticate(username=self.email, password=self.password)
        if not user:
            raise ServiceException("Invalid email or password")
        if not user.is_active:
            raise ServiceException("Account is deactivated")
        return user


class UpdateProfileService(BaseService):

    def __init__(self, user, **data):
        self.user = user
        self.data = data

    def execute(self):
        if not self.data:
            raise ServiceException("No fields to update")
        for field, value in self.data.items():
            setattr(self.user, field, value)
        self.user.save(update_fields=list(self.data.keys()))
        return self.user


class ChangePasswordService(BaseService):

    def __init__(self, user, old_password, new_password):
        self.user = user
        self.old_password = old_password
        self.new_password = new_password

    def execute(self):
        self._validate()
        self._change()

    def _validate(self):
        if not self.user.check_password(self.old_password):
            raise ServiceException("Old password is incorrect")
        if self.old_password == self.new_password:
            raise ServiceException("New password must be different")

    def _change(self):
        self.user.set_password(self.new_password)
        self.user.save(update_fields=["password"])


class DeactivateUserService(BaseService):
    """Admin only — deactivate any user."""

    def __init__(self, admin, user_id):
        self.admin   = admin
        self.user_id = user_id

    def execute(self):
        self._validate()
        user = self._get_user()
        user.is_active = False
        user.save(update_fields=["is_active"])
        return user

    def _validate(self):
        if not self.admin.is_super_admin:
            raise PermissionDeniedException("Only admin can deactivate users")

    def _get_user(self):
        try:
            return User.objects.get(id=self.user_id)
        except User.DoesNotExist:
            raise NotFoundException("User not found")