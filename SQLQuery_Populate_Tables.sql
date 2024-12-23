INSERT INTO CW1.PathPoint (TrailID, Longitude,Latitude,PathSequence,Details)

VALUES
((SELECT TrailID FROM CW1.Trail WHERE trailName = 'Plymouth Circular'),50.40886,-4.07859,1, 'Start/End')