create table HOUSE(
HouseID int,
FloorID int,
FloorsCount int,
DoorID int,
RoofID int,
WallID int,
ChimneyID int
);
  
create table FLOOR(
FloorID int,
FloorLevel int, --numer piętra
HouseID int --id domku, do którego należy piętro
);

create table DOOR(
DoorID int,
FloorID int, 
Position_x int
);

create table ROOF(
RoofID int,
HouseID int,
Chimney_Count int
);

create table WINDOWS(
WindowID int,
FloorID int, 
Position_x int);

create table BLANK(
BlankID int, 
FloorID int,
Position_x int
);