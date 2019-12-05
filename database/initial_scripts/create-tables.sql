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
FloorStyle int,
WindowID int,
WindowsCount int
);

create table DOOR(
DoorID int,
DoorStyle int);

create table ROOF(
RoofID int,
RoofStyle int);
  
create table WALL(
WallID int,
WallStyle int);

create table CHIMNEY(
WallID int,
ChimneyStyle int);

create table WINDOWS(
WindowID int,
WindowStyle int);
