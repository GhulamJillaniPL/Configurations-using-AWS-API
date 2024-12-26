from fastapi import APIRouter, HTTPException, Depends
from ..services.aws_service import AWSService
from ..models import EC2Instance, EC2InstanceCreate, EC2InstanceUpdate

router = APIRouter()
aws_service = AWSService()

@router.post("/instances", response_model=EC2Instance)
async def create_instance(instance_data: EC2InstanceCreate):
    try:
        instance = aws_service.create_instance(
            instance_type=instance_data.instance_type,
            region=instance_data.region
        )
        return instance
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/instances/{instance_id}", response_model=EC2Instance)
async def get_instance(instance_id: str):
    try:
        instance = aws_service.get_instance(instance_id)
        return instance
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/instances/{instance_id}", response_model=EC2Instance)
async def update_instance(instance_id: str, instance_data: EC2InstanceUpdate):
    try:
        instance = aws_service.update_instance(
            instance_id=instance_id,
            instance_type=instance_data.instance_type,
            state=instance_data.state
        )
        return instance
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/instances/{instance_id}")
async def delete_instance(instance_id: str):
    try:
        aws_service.delete_instance(instance_id)
        return {"message": f"Instance {instance_id} has been terminated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
