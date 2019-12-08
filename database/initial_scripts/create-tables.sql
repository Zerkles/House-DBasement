create table HOUSES(
HouseID serial,
LevelsCount int,
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