def get_continent_by_name(self, db: Session, continent_name: str):
    continent = db.query(Continent).filter(Continent.continent == continent_name).first()
    return continent.continent_id


def get_locations_by_continent(self, db: Session, continent_id: int):
    return db.query(Location).filter(Location.continent_id == continent_id).all()

@router.get("/continent-in-locations/{continent_name}", response_model=dict, tags=["continents & locations"])
def get_locations_by_continent(continent_name: str, db: Session = Depends(get_sync_db)):
    continent_id = continent_controller.get_continent_by_name(db, continent_name)
    if not continent_id:
        raise HTTPException(status_code=404, detail="Continent not found")

    locations = continent_controller.get_locations_by_continent(db, continent_id)
    return {"continent": continent_id, "locations": locations}