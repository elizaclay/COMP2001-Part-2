CREATE TABLE CW2.PathPoint(
    PathPointID INT IDENTITY NOT NULL,
    TrailID INT NOT NULL,
    Latitude DECIMAL (9,6) NOT NULL,
    Longitude DECIMAL (9, 6) NOT NULL,
    PathSequence INT NOT NULL,
    Details VARCHAR (50) NULL,

    CONSTRAINT PK_PathPoint PRIMARY KEY (PathPointID),
    CONSTRAINT FK_TrailPoint FOREIGN KEY (TrailID) REFERENCES CW2.Trail(TrailID) ON DELETE CASCADE,
    CONSTRAINT UQ_PathPoint UNIQUE (TrailID, PathSequence, Longitude, Latitude),
    CONSTRAINT CHK_Latitude CHECK (Latitude >= -90 AND Latitude <= 90),
    CONSTRAINT CHK_Longitude CHECK (Longitude >= -180 AND Longitude <= 180)
)