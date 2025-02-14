from fastapi import HTTPException, status


class ReportNotFoundException(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Report not found"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class CommentNotFoundException(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Comment not found"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class FishNotFoundException(HTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Fish not found"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class SelfReportStarException(HTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "You can't star your own report"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class FishAlreadyExistsException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "This fish already exists in the report"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)
