import logging
from typing import List
from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from pydantic import BaseModel
from distance_between_two_coordinates import calculate_distance

# Configure logging
logging.basicConfig(level=logging.INFO)

# Create FastAPI instance
app = FastAPI()

# Database connection URL
DATABASE_URL = "sqlite:///./addresses.db"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()

# SQLAlchemy models
class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    street = Column(String, index=True)
    city = Column(String, index=True)
    state = Column(String, index=True)
    country = Column(String, index=True)
    pin_code = Column(Integer, index=True)
    latitude = Column(Float)
    longitude = Column(Float)

# Pydantic models
class AddressBase(BaseModel):
    street: str
    city: str
    state: str
    country: str
    pin_code: int
    latitude: float
    longitude: float

class AddressCreate(AddressBase):
    pass

class AddressResponse(AddressBase):
    id: int

    class Config:
        from_attributes = True

# Dependency to get database session
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD operations
def create_address(db: Session, address: AddressCreate) -> AddressResponse:
    db_address = Address(**address.dict())
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return db_address

def get_address(db: Session, address_id: int) -> AddressResponse:
    address = db.query(Address).filter(Address.id == address_id).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")
    return address

def update_address(db: Session, address_id: int, address: AddressCreate) -> AddressResponse:
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    for attr, value in address.dict().items():
        setattr(db_address, attr, value)
    db.commit()
    db.refresh(db_address)
    return db_address

def delete_address(db: Session, address_id: int) -> dict:
    db_address = db.query(Address).filter(Address.id == address_id).first()
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    db.delete(db_address)
    db.commit()
    return {"message": "Address deleted successfully"}

# FastAPI endpoints
@app.post("/addresses/", response_model=AddressResponse,
          description="This API create a new address")
async def create_new_address(address: AddressCreate, db: Session = Depends(get_db)) -> AddressResponse:
    logging.info("Creating new address: %s", address)
    return create_address(db, address)

@app.get("/addresses/{address_id}", response_model=AddressResponse, 
         description="This API fetches the details of specified address")
async def read_address(address_id: int, db: Session = Depends(get_db)) -> AddressResponse:
    logging.info("Reading address with ID: %s", address_id)
    return get_address(db, address_id)

@app.put("/addresses/{address_id}", response_model=AddressResponse,
         description="This API updates an existing address")
async def update_existing_address(address_id: int, address: AddressCreate, db: Session = Depends(get_db)) -> AddressResponse:
    logging.info("Updating address with ID: %s", address_id)
    return update_address(db, address_id, address)

@app.delete("/addresses/{address_id}",
            description="This API deletes an existing address")
async def delete_existing_address(address_id: int, db: Session = Depends(get_db)) -> dict:
    logging.info("Deleting address with ID: %s", address_id)
    return delete_address(db, address_id)

@app.get("/list-addresses/", 
         response_model=List[AddressResponse], 
         description="This API fetches all addresses in the database with pagination enabled")
async def read_addresses(limit: int = Query(10, ge=1, le=100), offset: int = Query(0, ge=0), db: Session = Depends(get_db)) -> List[AddressResponse]:
    logging.info("Reading addresses with limit: %s and offset: %s", limit, offset)
    return db.query(Address).offset(offset).limit(limit).all()

@app.get("/addresses/within_distance/", 
         response_model=List[AddressResponse],
         description='''This API fetches the list of addresses within in a distance from the specified coordinates''')
async def read_addresses_within_distance(latitude: float, longitude: float, distance: float, db: Session = Depends(get_db)) -> List[AddressResponse]:
    logging.info("Reading addresses within distance. Latitude: %s, Longitude: %s, Distance: %s", latitude, longitude, distance)
    addresses = db.query(Address).all()
    addresses_within_distance = []
    for address in addresses:
        if calculate_distance(latitude, longitude, address.latitude, address.longitude) <= distance:
            addresses_within_distance.append(AddressResponse(**address.__dict__))
    return addresses_within_distance
