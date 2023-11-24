CREATE TABLE player (
	player_id INT auto_increment PRIMARY KEY,
    mail_id VARCHAR(255),
    dob VARCHAR(50),
    age INT, deposits INT, mobile BIGINT(10),
    naame VARCHAR(50)
);

CREATE TABLE developer (
	dev_id  INT auto_increment primary key,
	dev_name VARCHAR(40), 
    mail_id VARCHAR(100),
    mobile_no BIGINT(10),
    game_name VARCHAR(200)
);

CREATE TABLE game (
	game_id INT auto_increment PRIMARY KEY, 
    game_name VARCHAR(200), 
    ppm INT NOT NULL, 
    category VARCHAR(30), 
    no_of_players INT NOT NULL,
	dev_id INT NOT NULL,
    foreign key (dev_id) references developer(dev_id)
);

CREATE TABLE tournament(
	tourn_id INT auto_increment PRIMARY KEY,
    game_id INT, 
    tourn_name VARCHAR(100), 
    game_name VARCHAR(200), 
    Entry_fee INT NOT NULL, 
    wint_id INT NULL ,
    prize INT NOT NULL,
    foreign key (game_id) references game(game_id)
);

CREATE TABLE team (
    team_id INT auto_increment PRIMARY KEY,
    tourn_id INT,
    team_name VARCHAR(200),
    game_name VARCHAR(200),
    foreign key (tourn_id) references tournament(tourn_id)
);
CREATE TABLE team_player (
    player_id INT,
    team_id INT,
    PRIMARY KEY (player_id, team_id)
);

CREATE TABLE matches (
	match_id INT auto_increment PRIMARY KEY, 
    wint_id INT NULL, 
    game_name VARCHAR(200), 
    team1_id INT, team2_id INT, tourn_id INT,
    foreign key (tourn_id) references tournament(tourn_id),
	foreign key (team1_id) references team(team_id),
    foreign key (team2_id) references team(team_id)
);


CREATE TABLE leaderboard (
	player_id INT,
    points INT NOT NULL, 
    game_name VARCHAR(200), 
    player_name VARCHAR(20),
    foreign key (player_id) references player(player_id)
);

CREATE TABLE games_played (
	player_id INT,
    game_id INT,
	foreign key (player_id) references player(player_id),
	foreign key (game_id) references game(game_id)
);

CREATE TABLE multiplayer_developers AS
SELECT
    d.dev_id,
    d.dev_name,
    g.game_id,
    g.game_name,
    g.category
FROM
    developer d
JOIN
    game g ON d.dev_id = g.dev_id
WHERE
    g.category = 'multiplayer';
    

CREATE TABLE singleplayer_developers AS
SELECT
    d.dev_id,
    d.dev_name,
    g.game_id,
    g.game_name,
    g.category
FROM
    developer d
JOIN
    game g ON d.dev_id = g.dev_id
WHERE
    g.category = 'Singleplayer';
    

DELIMITER //

CREATE PROCEDURE GetMatchDetailsByTournament(IN tourn_id_param INT)
BEGIN
    SELECT
        m.match_id,
        m.game_name,
        m.team1_id,
        t1.team_name AS team1_name,
        m.team2_id,
        t2.team_name AS team2_name
    FROM
        matches m
    INNER JOIN
        team t1 ON m.team1_id = t1.team_id
    INNER JOIN
        team t2 ON m.team2_id = t2.team_id
    WHERE
        m.tourn_id = tourn_id_param;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE GetTopScorersPerGame()
BEGIN
    SELECT
        l.game_name,
        l.player_id,
        p.naame AS player_name,
        l.points
    FROM (
        SELECT
            game_name,
            player_id,
            points,
            RANK() OVER (PARTITION BY game_name ORDER BY points DESC) AS ranking
        FROM
            leaderboard
    ) l
    JOIN
        player p ON l.player_id = p.player_id
    WHERE
        l.ranking = 1;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE GetTeamsByTournament(IN tourn_id_param INT)
BEGIN
    SELECT
        t.team_id,
        t.team_name
    FROM
        team t
    WHERE
        t.tourn_id = tourn_id_param;
END //

DELIMITER ;

DELIMITER //

CREATE TRIGGER UpdatePlayerDeposits
AFTER INSERT ON games_played
FOR EACH ROW
BEGIN
    DECLARE game_ppm INT;
    
    -- Get the ppm value of the game
    SELECT ppm INTO game_ppm
    FROM game
    WHERE game_id = NEW.game_id;

    -- Update player's deposits based on ppm value
    UPDATE player
    SET deposits = deposits - game_ppm
    WHERE player_id = NEW.player_id;
END //

DELIMITER ;





