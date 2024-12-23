CREATE TABLE CW2.Difficulty (
    DifficultyID INT IDENTITY NOT NULL,
    DifficultyName VARCHAR(10) NOT NULL, 

    CONSTRAINT PK_DifficultyDetails PRIMARY KEY (DifficultyID),
    CONSTRAINT UQ_Difficulty UNIQUE (DifficultyName),
    CONSTRAINT CHK_Difficulty CHECK (DifficultyName IN ('Easy', 'Medium', 'Hard'))
)