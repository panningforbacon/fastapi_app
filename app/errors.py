class AppError(Exception):
    status_code = 500
    code = "internal_error"


class NotFoundError(AppError):
    status_code = 404
    code = "not_found"


class PermissionDeniedError(AppError):
    status_code = 403
    code = "permission_denied"
