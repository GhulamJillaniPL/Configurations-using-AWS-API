from enum import Enum
from typing import Optional
from pydantic import BaseModel

class InstanceState(str, Enum):
    PENDING = 'pending'
    RUNNING = 'running'
    STOPPING = 'stopping'
    STOPPED = 'stopped'
    TERMINATED = 'terminated'

class EC2Instance(BaseModel):
    instance_id: str
    instance_type: str
    state: InstanceState
    region: str
    public_ip: Optional[str] = None
    private_ip: Optional[str] = None

class EC2InstanceCreate(BaseModel):
    instance_type: str = "t2.micro"
    region: str = "us-east-1"

class EC2InstanceUpdate(BaseModel):
    instance_type: Optional[str] = None
    state: Optional[InstanceState] = None
