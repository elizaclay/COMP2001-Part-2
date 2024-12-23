CREATE TABLE CW2.TrailFeature(
    TrailID INT NOT NULL,
    FeatureID INT NOT NULL,

    PRIMARY KEY  (TrailID, FeatureID),

    CONSTRAINT FK_TrailLink FOREIGN KEY (TrailID) REFERENCES CW2.Trail(TrailID),
    CONSTRAINT FK_FeatureLink FOREIGN KEY (FeatureID) REFERENCES CW2.Feature(FeatureID)
)