function selectComponent() {
    var selectedComponent = document.getElementById("components").value;

    console.log('Selected Component:', selectedComponent);

    // Handle the "Game Developers" option
    if (selectedComponent === "game-developers") {
        gamedevelopers();
    } else if (selectedComponent === "matches") {
        matches();
    }else if (selectedComponent === "teams") {
        teams();
    }else if (selectedComponent === "team-players") {
        teamplayers();
    }else if (selectedComponent === "tournaments") {
        tournament();
    }else if (selectedComponent === "our-players") {
        ourplayers();
    }else {
        // For other options, display a default message
        document.querySelector('.display-panel').innerHTML = `<p>Displaying ${selectedComponent} content...</p>`;
    }
}

function ourplayers() {
    // Make an AJAX request to fetch players data
    $.ajax({
        url: '/get_players',
        type: 'GET',
        success: function (data) {
            // Clear existing content in the our-players table
            $('#players-table-body').empty();

            // Append new rows to the players table
            data.forEach(function (row) {
                $('#players-table-body').append(row);
            });

            // Display the players table
            $('#players-table').show();

        },
        error: function (error) {
            console.log('Error loading players data:', error);
        }
    });
}

function tournament(){
    // Make an AJAX request to fetch tournaments data
    $.ajax({
        url: '/get_tournament',
        type: 'GET',
        success: function (data) {
            // Clear existing content in the tournaments table
            $('#tournaments-table-body').empty();

            // Append new rows to the tournaments table
            data.forEach(function (row) {
                $('#tournaments-table-body').append(row);
            });

            // Display the tournaments table
            $('#tournaments-table').show();

        },
        error: function (error) {
            console.log('Error loading tournaments data:', error);
        }
    });
}

function teamplayers(){
    // Make an AJAX request to fetch teamplayers data
    $.ajax({
        url: '/get_teamplayers',
        type: 'GET',
        success: function (data) {
            // Clear existing content in the teams table
            $('#teamplayers-table-body').empty();

            // Append new rows to the matches table
            data.forEach(function (row) {
                $('#teamplayers-table-body').append(row);
            });

            // Display the matches table
            $('#teamplayers-table').show();

        },
        error: function (error) {
            console.log('Error loading teamplayers data:', error);
        }
    });
}

function teams(){
     // Make an AJAX request to fetch teams data
     $.ajax({
        url: '/get_teams',
        type: 'GET',
        success: function (data) {
            // Clear existing content in the teams table
            $('#teams-table-body').empty();

            // Append new rows to the matches table
            data.forEach(function (row) {
                $('#teams-table-body').append(row);
            });

            // Display the matches table
            $('#teams-table').show();

        },
        error: function (error) {
            console.log('Error loading teams data:', error);
        }
    });
}

function matches(){
    // Make an AJAX request to fetch matches data
    $.ajax({
        url: '/get_matches',
        type: 'GET',
        success: function (data) {
            // Clear existing content in the matches table
            $('#matches-table-body').empty();

            // Append new rows to the matches table
            data.forEach(function (row) {
                $('#matches-table-body').append(row);
            });

            // Display the matches table
            $('#matches-table').show();

        },
        error: function (error) {
            console.log('Error loading matches data:', error);
        }
    });
}

function gamedevelopers(){
    // Make an AJAX request to fetch developer data
    console.log('Making AJAX request for Game Developers');
    $.ajax({
        url: '/get_developers',
        type: 'GET',
        success: function (data) {
            // Clear existing content in the developer table
            $('#developer-table-body').empty();

            // Append new rows to the developer table
            data.forEach(function (row) {
                $('#developer-table-body').append(row);
            });

            // Display the developer table
            $('#developer-table').show();

        },
        error: function (error) {
            console.log('Error loading developer data:', error);
        }
    });
}

