from pydantic import BaseModel, ConfigDict


class LogoutResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    success: bool
    message: str
