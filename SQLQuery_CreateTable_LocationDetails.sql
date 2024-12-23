CREATE TABLE CW2.LocationDetails (
    LocationID INT NOT NULL IDENTITY,
    City VARCHAR(100) NOT NULL,
    StateProvince VARCHAR(100) NOT NULL,
    Country VARCHAR(100) NOT NULL,

    CONSTRAINT PK_LocationDetails PRIMARY KEY (LocationID),
    CONSTRAINT UQ_Location UNIQUE (City, StateProvince, Country)
)