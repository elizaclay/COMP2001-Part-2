import pyodbc
from config import db, ma, conn, cursor


### TRAIL USER TABLE #################################################
columns = [
    'UserID INT IDENTITY(1,1) PRIMARY KEY',
    'EmailAddress VARCHAR(320) UNIQUE, NOT NULL',
    'RoleType VARCHAR(5) NOT NULL'
]
create_table_cmd = f"CREATE TABLE CW2.TrailUser ({','.join(columns)})"
cursor.execute(create_table_cmd)
cursor.commit()

#### TRAIL TABLE #######################################################
columns = [
    'TrailID INT IDENTITY(1,1) PRIMARY KEY',
    'TrailName VARCHAR(100) UNIQUE NOT NULL',
    'TrailLocation VARCHAR(100) NOT NULL',
    'TrailSummary VARCHAR(500)',
    'TrailDescription VARCHAR(1000)',
    'Difficulty VARCHAR(10)',
    'RouteType VARCHAR(20)',
    'Distance_km DECIMAL(5,2)',
    'ElevationGain_m INT',
    'TimeEstimate_min INT',
    'OwnerID INT NOT NULL FOREIGN KEY REFERENCES CW2.TrailUser(UserID)',
    'Timestamp DATETIME DEFAULT GETDATE()'
]
create_table_cmd = f"CREATE TABLE CW2.Trail ({','.join(columns)})"
cursor.execute(create_table_cmd)
cursor.commit()

#### PATHPOINT TABLE ################################################
columns = [
    'PathPointID INT IDENTITY(1,1) PRIMARY KEY',
    'Latitude DECIMAL(9,6) NOT NULL',
    'Longitude DECIMAL(9,6) NOT NULL',
    'Details VARCHAR(50)',
    'Timestamp DATETIME DEFAULT GETDATE()'
]
create_table_cmd = f"CREATE TABLE CW2.PathPoint ({','.join(columns)})"
cursor.execute(create_table_cmd)
cursor.commit()

### FEATURE TABLE ####################################################
columns = [
    'FeatureID INT IDENTITY(1,1) PRIMARY KEY',
    'FeatureName VARCHAR(50) UNIQUE NOT NULL',
    'Timestamp DATETIME DEFAULT GETDATE()'
]
create_table_cmd = f"CREATE TABLE CW2.Feature ({','.join(columns)})"
cursor.execute(create_table_cmd)
cursor.commit()

### TRAILPOINT LINK TABLE ##############################################
columns = [
    'TrailID INT NOT NULL FOREIGN KEY REFERENCES CW2.Trail(TrailID) ON DELETE CASCADE',
    'PathPointID INT NOT NULL FOREIGN KEY REFERENCES CW2.PathPoint(PathPointID) ON DELETE CASCADE',
    'Timestamp DATETIME DEFAULT GETDATE()',
    'PRIMARY KEY (TrailID, PathPointID)'
]
create_table_cmd = f"CREATE TABLE CW2.TrailPoint ({','.join(columns)})"
cursor.execute(create_table_cmd)
cursor.commit()

### TRAILFEATURE LINK TABLE #############################################
columns = [
    'TrailID INT NOT NULL FOREIGN KEY REFERENCES CW2.Trail(TrailID) ON DELETE CASCADE',
    'FeatureID INT NOT NULL FOREIGN KEY REFERENCES CW2.Feature(FeatureID) ON DELETE CASCADE',
    'Timestamp DATETIME DEFAULT GETDATE()',
    'PRIMARY KEY (TrailID, FeatureID)'
]
create_table_cmd = f"CREATE TABLE CW2.TrailFeature ({','.join(columns)})"
cursor.execute(create_table_cmd)
cursor.commit()


cursor.close()
print("Build script finished")
