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
WindowsCount int,
Width int,
Height int
);

create table DOOR(
DoorID int,
DoorStyle int,
Width int,
Height int);

create table ROOF(
RoofID int,
RoofStyle int,
Width int,
Height int);
  
create table WALL(
WallID int,
WallStyle int,
Width int,
Height int);

create table CHIMNEY(
WallID int,
ChimneyStyle int,
Width int,
Height int);

create table WINDOWS(
WindowID int,
WindowStyle int,
Width int,
Height int);
