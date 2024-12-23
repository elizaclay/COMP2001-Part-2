CREATE TABLE CW2.Trail(
    TrailID INT IDENTITY NOT NULL,
    TrailName VARCHAR (100) NOT NULL,
    TrailSummary VARCHAR (500) NULL,
    TrailDescription VARCHAR (1000) NULL,
    Distance_km DECIMAL (5,2) NULL,
    ElevationGain_m INT NULL,
    TimeEstimate_min INT NULL,
    DifficultyType INT NULL, 
    RouteType INT NULL, 
    LocationType INT NOT NULL,
    OwnerID INT NOT NULL,

    CONSTRAINT PK_Trail PRIMARY KEY (TrailID),
    CONSTRAINT UQ_TrailName UNIQUE (TrailName),

    CONSTRAINT FK_TrailDifficulty FOREIGN KEY (DifficultyType) REFERENCES CW2.DifficultyDetails(DifficultyID),
    CONSTRAINT FK_TrailRoute FOREIGN KEY (RouteType) REFERENCES CW2.RouteDetails(RouteID),
    CONSTRAINT FK_TrailLocation FOREIGN KEY (LocationType) REFERENCES CW2.LocationDetails(LocationID),
    CONSTRAINT FK_TrailOwner FOREIGN KEY (OwnerID) REFERENCES CW2.TrailUser(UserID)
)