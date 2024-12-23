CREATE PROCEDURE CW2.CreateUser
    @EmailAddress VARCHAR (320),
    @RoleType VARCHAR (5) 

    AS 
    BEGIN 
    
    INSERT INTO CW2.TrailUser (EmailAddress, RoleType)
    VALUES (@EmailAddress, @RoleType)

    END
