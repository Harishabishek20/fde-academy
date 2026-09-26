from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


def compute_status(delay_days: int) -> str:
    """Classify a shipment's delay in days into on_time, minor_delay, or major_delay."""
    if delay_days == 0:
        return 'on_time'
    elif delay_days <= 2:
        return 'minor_delay'
    else:
        return 'major_delay'


class Shipment:
    def __init__(self, shipment_id: str, carrier: str, delay_days: int):
        self.shipment_id = shipment_id
        self.carrier = carrier
        self.delay_days = delay_days

    def status(self) -> str:
        return compute_status(self.delay_days)


app = FastAPI()
shipments_db = {}


class ShipmentIn(BaseModel):
    carrier: str
    delay_days: int


@app.get("/shipments/{shipment_id}")
def get_shipment(shipment_id: str):
    if shipment_id not in shipments_db:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return shipments_db[shipment_id]


@app.post("/shipments/{shipment_id}")
def create_shipment(shipment_id: str, shipment: ShipmentIn):
    record = {
        "shipment_id": shipment_id,
        "carrier": shipment.carrier,
        "delay_days": shipment.delay_days,
        "status": compute_status(shipment.delay_days),
    }
    shipments_db[shipment_id] = record
    return record