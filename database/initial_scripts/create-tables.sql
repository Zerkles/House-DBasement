create table HOUSES(
HouseID int NOT NULL AUTO_INCREMENT,
LevelsCount int
);
  
create table LEVELS(
LevelID int NOT NULL AUTO_INCREMENT ,
FloorLevel int, --numer piętra
HouseID int --id domku, do którego należy piętro
);

create table DOORS(
DoorID int NOT NULL AUTO_INCREMENT,
LevelID int, 
Position_x int
);

create table ROOFS(
RoofID int NOT NULL AUTO_INCREMENT,
HouseID int,
ChimneysCount int
);

create table WINDOWS(
WindowID int NOT NULL AUTO_INCREMENT,
LevelID int, 
Position_x int);

create table BLANKS(
BlankID int NOT NULL AUTO_INCREMENT, 
LevelID int,
Position_x int
);