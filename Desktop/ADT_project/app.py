from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
from flask import jsonify 
app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For flashing messages

# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'k@l@mth0di'
app.config['MYSQL_DB'] = 'sports_management'

# Initialize MySQL
mysql = MySQL(app)

# Dashboard
@app.route('/')
def dashboard():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute("SELECT COUNT(*) AS count FROM Teams")
        teams_count = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(*) AS count FROM Players")
        players_count = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(*) AS count FROM Matches")
        matches_count = cursor.fetchone()['count']

        # Fetching top players for the dashboard
        cursor.execute("SELECT PlayerName, Score FROM Players ORDER BY Score DESC LIMIT 5")
        top_players = cursor.fetchall()

    except Exception as e:
        flash(f"Error: {e}", "danger")
        return redirect(url_for('dashboard'))

    return render_template('dashboard.html', teams_count=teams_count, players_count=players_count, matches_count=matches_count, top_players=top_players)

# Teams Management

@app.route('/teams')
def teams():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute("SELECT * FROM Teams")
        teams_data = cursor.fetchall()
    except Exception as e:
        flash(f"Error: {e}", "danger")
        return redirect(url_for('teams'))

    return render_template('teams.html', teams=teams_data)

@app.route('/teams/view/<int:team_id>', methods=['GET'])
def view_team(team_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    try:
        cursor.execute("""
            SELECT * FROM Teams
            WHERE TeamID = %s
        """, (team_id,))
        
        team = cursor.fetchone()

        if team:
            return jsonify({
                'team_name': team['TeamName'],
                'manager': team['Manager'],
                
            })
        else:
            return jsonify({'error': 'Team not found'}), 404

    except Exception as e:
        print(f"Error fetching team details: {e}")
        return jsonify({'error': str(e)}), 500
    
    finally:
        cursor.close()

@app.route('/teams/add', methods=['GET', 'POST'])
def add_team():
    if request.method == 'POST':
        team_name = request.form['team_name']
        manager = request.form['manager']
        cursor = mysql.connection.cursor()

        try:
            # Manually increment TeamID by getting the current maximum and adding 1
            cursor.execute("SELECT IFNULL(MAX(TeamID), 0) + 1 AS NewTeamID FROM Teams")
            new_team_id = cursor.fetchone()[0]  # Access by index since it's a tuple

            # Insert the new team with manually incremented TeamID
            cursor.execute("INSERT INTO Teams (TeamID, TeamName, Manager) VALUES (%s, %s, %s)", 
                           (new_team_id, team_name, manager))
            mysql.connection.commit()

            flash('Team added successfully!', 'success')
        except Exception as e:
            mysql.connection.rollback()
            flash(f"Error: {e}", "danger")
        finally:
            cursor.close()

        return redirect(url_for('teams'))

    return render_template('add_team.html')



@app.route('/teams/edit/<int:team_id>', methods=['GET', 'POST'])
def edit_team(team_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        team_name = request.form['team_name']
        manager = request.form['manager']
        try:
            cursor.execute("UPDATE Teams SET TeamName=%s, Manager=%s WHERE TeamID=%s", (team_name, manager, team_id))
            mysql.connection.commit()
            flash('Team updated successfully!', 'success')
        except Exception as e:
            mysql.connection.rollback()
            flash(f"Error: {e}", "danger")
        return redirect(url_for('teams'))

    try:
        cursor.execute("SELECT * FROM Teams WHERE TeamID=%s", [team_id])
        team = cursor.fetchone()
    except Exception as e:
        flash(f"Error: {e}", "danger")
        return redirect(url_for('teams'))

    return render_template('edit_team.html', team=team)

@app.route('/teams/delete/<int:team_id>')
def delete_team(team_id):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("DELETE FROM Teams WHERE TeamID=%s", [team_id])
        mysql.connection.commit()
        flash('Team deleted successfully!', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f"Error: {e}", "danger")
    return redirect(url_for('teams'))

# Players Management

@app.route('/players')
def players():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute("""
            SELECT Players.PlayerID, Players.PlayerName, Teams.TeamName, Players.Position, Players.Score
            FROM Players
            JOIN Teams ON Players.TeamID = Teams.TeamID
        """)
        players_data = cursor.fetchall()
    except Exception as e:
        flash(f"Error: {e}", "danger")
        return redirect(url_for('players'))

    return render_template('players.html', players=players_data)

@app.route('/players/add', methods=['GET', 'POST'])
def add_player():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    if request.method == 'POST':
        # Collect form data
        player_name = request.form['player_name']
        team_id = request.form['team_id']
        position = request.form['position']
        score = request.form['score']

        try:
            # Manually generate the next PlayerID by finding the max current PlayerID
            cursor.execute("SELECT MAX(PlayerID) AS max_id FROM Players")
            result = cursor.fetchone()
            if result and result['max_id'] is not None:
                next_player_id = result['max_id'] + 1  # Increment max PlayerID by 1
            else:
                next_player_id = 1  # Start with PlayerID 1 if no players exist

            # Insert data into the Players table with the manually incremented PlayerID
            cursor.execute("""
                INSERT INTO Players (PlayerID, PlayerName, TeamID, Position, Score)
                VALUES (%s, %s, %s, %s, %s)
            """, (next_player_id, player_name, team_id, position, score))
            mysql.connection.commit()  # Commit changes
            flash('Player added successfully!', 'success')
        except Exception as e:
            mysql.connection.rollback()  # Rollback in case of error
            flash(f"Error: {e}", 'danger')
        finally:
            cursor.close()  # Ensure the cursor is closed

        return redirect(url_for('players'))  # Redirect to the players list after POST

    # Fetch teams to populate the dropdown in GET request
    cursor.execute("SELECT TeamID, TeamName FROM Teams")
    teams = cursor.fetchall()
    cursor.close()  # Close the cursor after fetching data

    # Render the form with team data
    return render_template('add_player.html', teams=teams)

@app.route('/players/view/<int:player_id>', methods=['GET'])
def view_player(player_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    try:
        print(f"Fetching details for Player ID: {player_id}")  # Debugging line
        
        # Fetch player details along with team information
        cursor.execute("""
            SELECT Players.PlayerID, Players.PlayerName, Teams.TeamName, Players.Position, Players.Score
            FROM Players
            JOIN Teams ON Players.TeamID = Teams.TeamID
            WHERE Players.PlayerID = %s
        """, (player_id,))
        
        player = cursor.fetchone()

        if player:
            return jsonify({
                'player_name': player['PlayerName'],
                'team_name': player['TeamName'],
                'position': player['Position'],
                'score': player['Score'],
            })
        else:
            return jsonify({'error': 'Player not found'}), 404

    except Exception as e:
        print(f"Error fetching player details: {e}")  # Improved error logging
        return jsonify({'error': str(e)}), 500
    
    finally:
        cursor.close()




@app.route('/players/edit/<int:player_id>', methods=['GET', 'POST'])
def edit_player(player_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        player_name = request.form['player_name']
        team_id = request.form['team_id']
        position = request.form['position']
        score = request.form['score']

        try:
            cursor.execute("UPDATE Players SET PlayerName=%s, TeamID=%s, Position=%s, Score=%s WHERE PlayerID=%s", (player_name, team_id, position, score, player_id))
            mysql.connection.commit()
            flash('Player updated successfully!', 'success')
        except Exception as e:
            mysql.connection.rollback()
            flash(f"Error: {e}", "danger")
        return redirect(url_for('players'))

    try:
        cursor.execute("SELECT * FROM Players WHERE PlayerID=%s", [player_id])
        player = cursor.fetchone()
        cursor.execute("SELECT TeamID, TeamName FROM Teams")
        teams = cursor.fetchall()
    except Exception as e:
        flash(f"Error: {e}", "danger")
        return redirect(url_for('players'))

    return render_template('edit_player.html', player=player, teams=teams)

@app.route('/players/delete/<int:player_id>')
def delete_player(player_id):
    cursor = mysql.connection.cursor()
    try:
        cursor.execute("DELETE FROM Players WHERE PlayerID=%s", [player_id])
        mysql.connection.commit()
        flash('Player deleted successfully!', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f"Error: {e}", "danger")
    return redirect(url_for('players'))

# Matches Management

@app.route('/matches')
def matches():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    try:
        cursor.execute("""
            SELECT Matches.MatchID, HomeTeam.TeamName AS HomeTeam, 
                   AwayTeam.TeamName AS AwayTeam, Stadiums.StadiumName, 
                   Matches.Date AS MatchDate
            FROM Matches
            JOIN Teams AS HomeTeam ON Matches.HomeTeamID = HomeTeam.TeamID
            JOIN Teams AS AwayTeam ON Matches.AwayTeamID = AwayTeam.TeamID
            JOIN Stadiums ON Matches.StadiumID = Stadiums.StadiumID
        """)
        matches_data = cursor.fetchall()
    except Exception as e:
        flash(f"Error: {e}", "danger")
        return redirect(url_for('matches'))

    return render_template('matches.html', matches=matches_data)


@app.route('/matches/add', methods=['GET', 'POST'])
def add_match():
    if request.method == 'POST':
        home_team_id = request.form['home_team_id']
        away_team_id = request.form['away_team_id']
        stadium_id = request.form['stadium_id']
        date = request.form['date']
        home_team_score = request.form['home_team_score']
        away_team_score = request.form['away_team_score']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        # Check if Home and Away teams are the same
        if home_team_id == away_team_id:
            flash('Home and Away teams cannot be the same!', 'danger')
            return redirect(url_for('add_match'))

        try:
            # Manually handle MatchID (if necessary)
            cursor.execute("SELECT MAX(MatchID) AS max_id FROM Matches")
            result = cursor.fetchone()
            if result and result['max_id'] is not None:
                next_match_id = result['max_id'] + 1  # Increment MatchID by 1
            else:
                next_match_id = 1  # Start with MatchID 1 if no matches exist

            # Insert match data, including manually handled MatchID
            cursor.execute("""
                INSERT INTO Matches (MatchID, HomeTeamID, AwayTeamID, StadiumID, Date, HomeTeamScore, AwayTeamScore)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (next_match_id, home_team_id, away_team_id, stadium_id, date, home_team_score, away_team_score))
            mysql.connection.commit()
            flash('Match added successfully!', 'success')
        except Exception as e:
            mysql.connection.rollback()  # Rollback in case of an error
            flash(f"Error: {e}", 'danger')
        finally:
            cursor.close()  # Ensure the cursor is closed

        return redirect(url_for('matches'))

    # Fetch teams to populate dropdowns for home and away team
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT TeamID, TeamName FROM Teams")
    teams = cursor.fetchall()

    # Fetch stadiums to populate the stadium dropdown
    cursor.execute("SELECT StadiumID, StadiumName FROM Stadiums")
    stadiums = cursor.fetchall()
    cursor.close()  # Ensure the cursor is closed after fetching data

    return render_template('add_match.html', teams=teams, stadiums=stadiums)


@app.route('/matches/edit/<int:match_id>', methods=['GET', 'POST'])
def edit_match(match_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    if request.method == 'POST':
        # Get form data
        home_team_id = request.form['home_team_id']
        away_team_id = request.form['away_team_id']
        stadium_id = request.form['stadium_id']
        date = request.form['date']
        home_team_score = request.form['home_team_score']
        away_team_score = request.form['away_team_score']

        # Ensure home and away teams are different
        if home_team_id == away_team_id:
            flash('Home and Away teams cannot be the same!', 'danger')
            return redirect(url_for('edit_match', match_id=match_id))

        try:
            # Update match data
            cursor.execute("""
                UPDATE Matches
                SET HomeTeamID=%s, AwayTeamID=%s, StadiumID=%s, Date=%s, HomeTeamScore=%s, AwayTeamScore=%s
                WHERE MatchID=%s
            """, (home_team_id, away_team_id, stadium_id, date, home_team_score, away_team_score, match_id))
            mysql.connection.commit()
            flash('Match updated successfully!', 'success')
        except Exception as e:
            mysql.connection.rollback()  # Rollback in case of an error
            flash(f"Error: {e}", "danger")
        finally:
            cursor.close()

        return redirect(url_for('matches'))

    try:
        # Fetch the match details to prefill the form
        cursor.execute("SELECT * FROM Matches WHERE MatchID=%s", [match_id])
        match = cursor.fetchone()

        # Fetch teams and stadiums to populate dropdowns
        cursor.execute("SELECT TeamID, TeamName FROM Teams")
        teams = cursor.fetchall()
        cursor.execute("SELECT StadiumID, StadiumName FROM Stadiums")
        stadiums = cursor.fetchall()
    except Exception as e:
        flash(f"Error: {e}", "danger")
        return redirect(url_for('matches'))
    finally:
        cursor.close()

    # Render the edit form with current match data
    return render_template('edit_match.html', match=match, teams=teams, stadiums=stadiums)


@app.route('/matches/delete/<int:match_id>', methods=['POST', 'GET'])
def delete_match(match_id):
    cursor = mysql.connection.cursor()

    try:
        # Delete the match from the Matches table
        cursor.execute("DELETE FROM Matches WHERE MatchID = %s", [match_id])
        mysql.connection.commit()
        flash('Match deleted successfully!', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash(f"Error: {e}", 'danger')
    finally:
        cursor.close()

    return redirect(url_for('matches'))

@app.route('/matches/view/<int:match_id>', methods=['GET'])
def view_match(match_id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    try:
        # Fetch match details
        cursor.execute("""
            SELECT Matches.*, HomeTeam.TeamName AS home_team, AwayTeam.TeamName AS away_team, Stadiums.StadiumName AS stadium
            FROM Matches
            JOIN Teams AS HomeTeam ON Matches.HomeTeamID = HomeTeam.TeamID
            JOIN Teams AS AwayTeam ON Matches.AwayTeamID = AwayTeam.TeamID
            JOIN Stadiums ON Matches.StadiumID = Stadiums.StadiumID
            WHERE MatchID = %s
        """, [match_id])
        match = cursor.fetchone()

        # Return match details as JSON
        return jsonify({
            'home_team': match['home_team'],
            'away_team': match['away_team'],
            'stadium': match['stadium'],
            'date': match['Date'],
            'home_team_score': match['HomeTeamScore'],
            'away_team_score': match['AwayTeamScore']
        })
    except Exception as e:
        flash(f"Error fetching match details: {e}", 'danger')
        return jsonify({}), 500
    finally:
        cursor.close()


# Analytics for Player Performance
@app.route('/analytics')
def analytics():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    try:
        # Fetching top-performing players
        cursor.execute("""
            SELECT PlayerName, Score FROM Players ORDER BY Score DESC LIMIT 5
        """)
        top_players = cursor.fetchall()
    except Exception as e:
        flash(f"Error: {e}", "danger")
        return redirect(url_for('analytics'))

    return render_template('analytics.html', top_players=top_players)

if __name__ == '__main__':
    app.run(debug=True)
