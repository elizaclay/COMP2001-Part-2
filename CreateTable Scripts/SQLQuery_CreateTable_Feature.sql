CREATE TABLE CW2.Feature (
    FeatureID INT IDENTITY, 
    FeatureName VARCHAR(50)

    CONSTRAINT PK_Feature PRIMARY KEY (FeatureID),
    CONSTRAINT UQ_Feature UNIQUE (FeatureName)
)