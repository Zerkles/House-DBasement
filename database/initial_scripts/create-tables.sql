create table HOUSES(
HouseID serial,
LevelsCount int,
HousesCount int,
ImageURL VARCHAR(128)
);
  
create table LEVELS(
LevelID serial,
LevelFloor int, --numer piętra
HouseID int --id domku, do którego należy piętro
);

create table DOORS(
DoorID serial,
LevelID int,
Position_x int
);

create table ROOFS(
RoofID serial,
HouseID int,
ChimneysCount int
);

create table WINDOWS(
WindowID serial,
LevelID int,
Position_x int);

create table BLANKS(
BlankID serial, 
LevelID int,
Position_x int
);


CREATE FUNCTION count_houses() RETURNS TRIGGER AS $$
BEGIN
    
    UPDATE HOUSES SET HousesCount = ((SELECT COUNT(*) FROM HOUSES) - 1) WHERE 1=1;

    Return NULL;
END;
$$ LANGUAGE 'plpgsql' ;

CREATE TRIGGER counter AFTER INSERT ON HOUSES
    EXECUTE PROCEDURE count_houses();