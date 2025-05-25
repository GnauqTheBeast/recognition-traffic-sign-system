from pydantic import BaseModel
from typing import Optional

class BaseResponseModel(BaseModel):
    sample_id: Optional[int] = None 