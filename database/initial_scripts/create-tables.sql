create table HOUSES(
HouseID int,
LevelsCount int
);
  
create table LEVELS(
LevelID int,
FloorLevel int, --numer piętra
HouseID int --id domku, do którego należy piętro
);

create table DOORS(
DoorID int,
LevelID int, 
Position_x int
);

create table ROOFS(
RoofID int,
HouseID int,
ChimneysCount int
);

create table WINDOWS(
WindowID int,
LevelID int, 
Position_x int);

create table BLANKS(
BlankID int, 
LevelID int,
Position_x int
);