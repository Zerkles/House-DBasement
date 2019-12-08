INSERT INTO HOUSES (HouseID) VALUES
(DEFAULT);

INSERT INTO LEVELS (FloorLevel, HouseID)VALUES 
(0, 1),
(1, 1),
(0, 2),
(1, 2),
(2, 2),
(0, 3),
(1, 3),
(0, 4),
(1, 4),
(0, 5);

INSERT INTO DOORS (LevelID, Position_x) VALUES
(1, 2),
(2, 1),
(3, 3),
(4, 2),
(5, 1),
(6, 3),
(7, 2),
(8, 2),
(9, 1),
(10, 3);

INSERT INTO ROOFS (HouseID, ChimneysCount) VALUES
(1, 0),
(2, 2),
(3, 1),
(4, 4),
(5, 3);

INSERT INTO WINDOWS (LevelID, Position_x) VALUES
(1, 1),
(1, 3),
(2, 2),
(3, 1),
(3, 2),
(4, 1),
(5, 2),
(6, 1),
(7, 1),
(8, 1),
(8, 3),
(9, 3),
(10, 1);

INSERT INTO BLANKS (LevelID, Position_x) VALUES
(2, 3),
(4, 3),
(5, 3),
(6, 2),
(7, 3),
(9, 2),
(10, 2);