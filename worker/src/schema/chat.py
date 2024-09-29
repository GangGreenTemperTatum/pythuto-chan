from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional
import uuid


class Message(BaseModel):
    id = str(uuid.uuid4()) # the integer gathers the prior X number of messages in the cache to give the model context
    msg: str
    timestamp = str(datetime.now())