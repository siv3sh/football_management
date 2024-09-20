-- create database sports_management;
-- use sports_management; 
-- Teams Table
CREATE TABLE Teams (
    TeamID INT PRIMARY KEY,
    TeamName VARCHAR(100) NOT NULL,
    Manager VARCHAR(100) NOT NULL
);

-- Players Table
CREATE TABLE Players (
    PlayerID INT PRIMARY KEY,
    PlayerName VARCHAR(100) NOT NULL,
    TeamID INT,
    Position VARCHAR(50),
    Score INT,
    FOREIGN KEY (TeamID) REFERENCES Teams(TeamID) ON DELETE SET NULL
);

-- Sponsors Table
CREATE TABLE Sponsors (
    SponsorID INT PRIMARY KEY,
    SponsorName VARCHAR(100) NOT NULL
);

-- TeamSponsors Junction Table (Normalization)
CREATE TABLE TeamSponsors (
    TeamID INT,
    SponsorID INT,
    PRIMARY KEY (TeamID, SponsorID),
    FOREIGN KEY (TeamID) REFERENCES Teams(TeamID) ON DELETE CASCADE,
    FOREIGN KEY (SponsorID) REFERENCES Sponsors(SponsorID) ON DELETE CASCADE
);

-- Stadiums Table
CREATE TABLE Stadiums (
    StadiumID INT PRIMARY KEY,
    StadiumName VARCHAR(100) NOT NULL,
    Location VARCHAR(100),
    TeamID INT,
    FOREIGN KEY (TeamID) REFERENCES Teams(TeamID) ON DELETE SET NULL
);

-- Matches Table
CREATE TABLE Matches (
    MatchID INT PRIMARY KEY,
    HomeTeamID INT,
    AwayTeamID INT,
    StadiumID INT,
    Date DATE NOT NULL,
    HomeTeamScore INT,
    AwayTeamScore INT,
    FOREIGN KEY (HomeTeamID) REFERENCES Teams(TeamID) ON DELETE CASCADE,
    FOREIGN KEY (AwayTeamID) REFERENCES Teams(TeamID) ON DELETE CASCADE,
    FOREIGN KEY (StadiumID) REFERENCES Stadiums(StadiumID) ON DELETE SET NULL
);

-- Referees Table
CREATE TABLE Referees (
    RefereeID INT PRIMARY KEY,
    RefereeName VARCHAR(100) NOT NULL,
    ExperienceYears INT NOT NULL
);

-- MatchReferees Junction Table (Normalization)
CREATE TABLE MatchReferees (
    MatchID INT,
    RefereeID INT,
    PRIMARY KEY (MatchID, RefereeID),
    FOREIGN KEY (MatchID) REFERENCES Matches(MatchID) ON DELETE CASCADE,
    FOREIGN KEY (RefereeID) REFERENCES Referees(RefereeID) ON DELETE CASCADE
);

-- TeamStatistics Table
CREATE TABLE TeamStatistics (
    TeamID INT,
    SeasonYear INT,
    Wins INT,
    Losses INT,
    Draws INT,
    GoalsFor INT,
    GoalsAgainst INT,
    PRIMARY KEY (TeamID, SeasonYear),
    FOREIGN KEY (TeamID) REFERENCES Teams(TeamID) ON DELETE CASCADE
);

-- PlayerStatistics Table
CREATE TABLE PlayerStatistics (
    PlayerID INT,
    MatchID INT,
    Goals INT,
    Assists INT,
    MinutesPlayed INT,
    PRIMARY KEY (PlayerID, MatchID),
    FOREIGN KEY (PlayerID) REFERENCES Players(PlayerID) ON DELETE CASCADE,
    FOREIGN KEY (MatchID) REFERENCES Matches(MatchID) ON DELETE CASCADE
);

-- Injuries Table
CREATE TABLE Injuries (
    InjuryID INT PRIMARY KEY,
    PlayerID INT,
    InjuryType VARCHAR(100) NOT NULL,
    DateInjured DATE,
    DateRecovered DATE,
    FOREIGN KEY (PlayerID) REFERENCES Players(PlayerID) ON DELETE SET NULL
);

-- Transfers Table
CREATE TABLE Transfers (
    TransferID INT PRIMARY KEY,
    PlayerID INT,
    FromTeamID INT,
    ToTeamID INT,
    TransferFee DECIMAL(15, 2),
    TransferDate DATE,
    FOREIGN KEY (PlayerID) REFERENCES Players(PlayerID) ON DELETE CASCADE,
    FOREIGN KEY (FromTeamID) REFERENCES Teams(TeamID) ON DELETE CASCADE,
    FOREIGN KEY (ToTeamID) REFERENCES Teams(TeamID) ON DELETE CASCADE
);

-- TrainingSessions Table
CREATE TABLE TrainingSessions (
    SessionID INT PRIMARY KEY,
    TeamID INT,
    Date DATE NOT NULL,
    Location VARCHAR(100),
    Duration INT, -- Duration in minutes
    FOREIGN KEY (TeamID) REFERENCES Teams(TeamID) ON DELETE CASCADE
);

-- SessionAttendance Table
CREATE TABLE SessionAttendance (
    SessionID INT,
    PlayerID INT,
    Attended BOOLEAN NOT NULL,
    PRIMARY KEY (SessionID, PlayerID),
    FOREIGN KEY (SessionID) REFERENCES TrainingSessions(SessionID) ON DELETE CASCADE,
    FOREIGN KEY (PlayerID) REFERENCES Players(PlayerID) ON DELETE CASCADE
);
-- Teams Data
INSERT INTO Teams (TeamID, TeamName, Manager) VALUES
(1, 'Red Dragons', 'Alice Smith'),
(2, 'Blue Eagles', 'Bob Johnson'),
(3, 'Green Warriors', 'Carol Davis'),
(4, 'Yellow Tigers', 'David Wilson'),
(5, 'Black Panthers', 'Emma Brown'),
(6, 'White Lions', 'Frank Harris'),
(7, 'Purple Sharks', 'Grace Clark'),
(8, 'Orange Dragons', 'Hank Lewis'),
(9, 'Silver Foxes', 'Ivy Walker'),
(10, 'Golden Hawks', 'Jack Young');

-- Players Data
INSERT INTO Players (PlayerID, PlayerName, TeamID, Position, Score) VALUES
(1, 'Lionel Messi', 1, 'Forward', 95),
(2, 'Cristiano Ronaldo', 1, 'Forward', 93),
(3, 'Neymar Jr', 2, 'Forward', 89),
(4, 'Kylian Mbappe', 2, 'Forward', 90),
(5, 'Kevin De Bruyne', 3, 'Midfielder', 92),
(6, 'Virgil van Dijk', 3, 'Defender', 88),
(7, 'Sergio Ramos', 4, 'Defender', 87),
(8, 'Paul Pogba', 4, 'Midfielder', 85),
(9, 'Gareth Bale', 5, 'Forward', 84),
(10, 'Eden Hazard', 5, 'Forward', 86);

-- Sponsors Data
INSERT INTO Sponsors (SponsorID, SponsorName) VALUES
(1, 'Nike'),
(2, 'Adidas'),
(3, 'Puma'),
(4, 'Under Armour'),
(5, 'Reebok'),
(6, 'New Balance'),
(7, 'Umbro'),
(8, 'Asics'),
(9, 'Hummel'),
(10, 'Joma');

-- TeamSponsors Data
INSERT INTO TeamSponsors (TeamID, SponsorID) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10);

-- Stadiums Data
INSERT INTO Stadiums (StadiumID, StadiumName, Location, TeamID) VALUES
(1, 'Dragon Stadium', 'City A', 1),
(2, 'Eagle Arena', 'City B', 2),
(3, 'Warrior Field', 'City C', 3),
(4, 'Tiger Park', 'City D', 4),
(5, 'Panther Stadium', 'City E', 5),
(6, 'Lion Stadium', 'City F', 6),
(7, 'Shark Arena', 'City G', 7),
(8, 'Dragon Arena', 'City H', 8),
(9, 'Fox Stadium', 'City I', 9),
(10, 'Hawk Field', 'City J', 10);

-- Matches Data
INSERT INTO Matches (MatchID, HomeTeamID, AwayTeamID, StadiumID, Date, HomeTeamScore, AwayTeamScore) VALUES
(1, 1, 2, 1, '2024-01-05', 2, 1),
(2, 3, 4, 2, '2024-01-06', 1, 3),
(3, 5, 6, 3, '2024-01-07', 0, 2),
(4, 7, 8, 4, '2024-01-08', 3, 3),
(5, 9, 10, 5, '2024-01-09', 1, 1),
(6, 1, 3, 6, '2024-01-10', 2, 2),
(7, 2, 5, 7, '2024-01-11', 0, 4),
(8, 4, 7, 8, '2024-01-12', 3, 0),
(9, 6, 8, 9, '2024-01-13', 1, 2),
(10, 9, 2, 10, '2024-01-14', 4, 1);

-- Referees Data
INSERT INTO Referees (RefereeID, RefereeName, ExperienceYears) VALUES
(1, 'Michael Oliver', 15),
(2, 'Anthony Taylor', 14),
(3, 'Mark Clattenburg', 17),
(4, 'Howard Webb', 20),
(5, 'Pierluigi Collina', 25),
(6, 'Bjorn Kuipers', 12),
(7, 'Cuneyt Cakir', 19),
(8, 'Felix Brych', 16),
(9, 'Daniele Orsato', 13),
(10, 'Szymon Marciniak', 11);

-- MatchReferees Data
INSERT INTO MatchReferees (MatchID, RefereeID) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10);

-- TeamStatistics Data
INSERT INTO TeamStatistics (TeamID, SeasonYear, Wins, Losses, Draws, GoalsFor, GoalsAgainst) VALUES
(1, 2024, 18, 5, 3, 45, 20),
(2, 2024, 17, 6, 3, 40, 22),
(3, 2024, 14, 7, 5, 38, 30),
(4, 2024, 13, 8, 5, 36, 28),
(5, 2024, 12, 9, 5, 33, 31),
(6, 2024, 10, 10, 6, 30, 33),
(7, 2024, 8, 12, 6, 27, 36),
(8, 2024, 6, 14, 6, 23, 39),
(9, 2024, 5, 15, 6, 21, 42),
(10, 2024, 4, 16, 6, 18, 45);

-- PlayerStatistics Data
INSERT INTO PlayerStatistics (PlayerID, MatchID, Goals, Assists, MinutesPlayed) VALUES
(1, 1, 2, 1, 90),
(2, 1, 0, 1, 90),
(3, 2, 1, 0, 88),
(4, 2, 2, 1, 90),
(5, 3, 0, 2, 90),
(6, 3, 0, 0, 90),
(7, 4, 3, 0, 90),
(8, 4, 0, 1, 85),
(9, 5, 1, 0, 90),
(10, 5, 1, 0, 89);

-- Injuries Data
INSERT INTO Injuries (InjuryID, PlayerID, InjuryType, DateInjured, DateRecovered) VALUES
(1, 1, 'Hamstring', '2024-01-20', '2024-02-20'),
(2, 2, 'Ankle Sprain', '2024-02-10', '2024-03-10'),
(3, 3, 'Knee Ligament', '2024-03-15', NULL),
(4, 4, 'Concussion', '2024-01-25', '2024-02-05'),
(5, 5, 'Shoulder Dislocation', '2024-03-01', '2024-04-01'),
(6, 6, 'Achilles Tear', '2024-02-10', '2024-05-10'),
(7, 7, 'Fractured Wrist', '2024-01-30', '2024-03-01'),
(8, 8, 'Back Strain', '2024-02-20', '2024-03-20'),
(9, 9, 'Hamstring', '2024-01-15', '2024-02-15'),
(10, 10, 'Groin Strain', '2024-02-10', '2024-03-10');

-- Transfers Data
INSERT INTO Transfers (TransferID, PlayerID, FromTeamID, ToTeamID, TransferFee, TransferDate) VALUES
(1, 1, 1, 2, 50000000, '2024-01-15'),
(2, 2, 2, 3, 60000000, '2024-01-20'),
(3, 3, 3, 4, 55000000, '2024-01-25'),
(4, 4, 4, 5, 70000000, '2024-01-30'),
(5, 5, 5, 6, 45000000, '2024-02-01'),
(6, 6, 6, 7, 40000000, '2024-02-05'),
(7, 7, 7, 8, 65000000, '2024-02-10'),
(8, 8, 8, 9, 75000000, '2024-02-15'),
(9, 9, 9, 10, 50000000, '2024-02-20'),
(10, 10, 10, 1, 80000000, '2024-02-25');

-- TrainingSessions Data
INSERT INTO TrainingSessions (SessionID, TeamID, Date, Location, Duration) VALUES
(1, 1, '2024-01-10', 'Training Ground A', 120),
(2, 2, '2024-01-11', 'Training Ground B', 110),
(3, 3, '2024-01-12', 'Training Ground C', 100),
(4, 4, '2024-01-13', 'Training Ground D', 90),
(5, 5, '2024-01-14', 'Training Ground E', 130),
(6, 6, '2024-01-15', 'Training Ground F', 115),
(7, 7, '2024-01-16', 'Training Ground G', 105),
(8, 8, '2024-01-17', 'Training Ground H', 125),
(9, 9, '2024-01-18', 'Training Ground I', 100),
(10, 10, '2024-01-19', 'Training Ground J', 110);

-- SessionAttendance Data
INSERT INTO SessionAttendance (SessionID, PlayerID, Attended) VALUES
(1, 1, TRUE),
(1, 2, TRUE),
(2, 3, TRUE),
(2, 4, TRUE),
(3, 5, TRUE),
(3, 6, TRUE),
(4, 7, TRUE),
(4, 8, TRUE),
(5, 9, TRUE),
(5, 10, TRUE);

