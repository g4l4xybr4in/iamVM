from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

# Function to establish connection to PostgreSQL database
def connect_to_database():
    try:
        connection = psycopg2.connect(
            dbname="your_dbname",
            user="your_username",
            password="your_password",
            host="your_host",
            port="your_port"
        )
        return connection
    except psycopg2.Error as e:
        print("Error connecting to PostgreSQL database:", e)
        return None

# Create tables if they don't exist
def create_tables(cursor):
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS credentials (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fullName VARCHAR(255),
                email VARCHAR(255),
                DOB DATE,
                birthTime TIME,
                birthLocation VARCHAR(255)
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS beforeKids (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timeTogetherBefore INTEGER,
                numDatesBefore INTEGER,
                numIntimacyBefore INTEGER,
                numFightsBefore INTEGER
            );         
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS afterKids (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timeTogetherAfter INTEGER,
                numDatesAfter INTEGER,
                numIntimacyAfter INTEGER,
                numFightsAfter INTEGER
            );         
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS idealMarriage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timeTogetherIdeal INTEGER,
                numDatesIdeal INTEGER,
                numIntimacyIdeal INTEGER,
                numFightsIdeal TEXT,
                idealMarriage TEXT
            );         
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS generalQuestions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                marriageChange TEXT,
                changeFeeling TEXT,
                negotiation TEXT,
                fightResult TEXT,
                reocurringIssues TEXT,
                frusturatedTime TEXT,
                relationalImpact TEXT,
                conflictResolved TEXT,
                parentExpectations TEXT,
                addressIssue TEXT,
                issueLength TEXT,
                idealSupport TEXT,
                optimalResources TEXT,
                upbringing TEXT
            );         
        ''')

        print("Tables created successfully")
    except psycopg2.connector.Error as e:
        print("Error creating tables:", e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/templates/form.html')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    fullName = request.form.get('fullName')
    email = request.form.get('email')
    DOB = request.form.get('DOB')
    birthTime = request.form.get('birthTime')
    birthLocation = request.form.get('birthLocation')
    time_together_before = request.form.get('timeTogetherBefore')
    num_dates_before = request.form.get('numDatesBefore')
    num_intimacy_before = request.form.get('numIntimacyBefore')
    num_fights_before = request.form.get('numFightsBefore')
    time_together_after = request.form.get('timeTogetherAfter')
    num_dates_after = request.form.get('numDatesAfter')
    num_intimacy_after = request.form.get('numIntimacyAfter')
    num_fights_after = request.form.get('numFightsAfter')
    timeTogetherIdeal = request.form.get('timeTogetherIdeal')
    numDatesIdeal = request.form.get('numDatesIdeal')
    numIntimacyIdeal = request.form.get('numIntimacyIdeal')
    numFightsIdeal = request.form.get('numFightsIdeal')
    idealMarriage = request.form.get('idealMarriage')
    marriageChange = request.form.get('marriageChange')
    changeFeeling = request.form.get('changeFeeling')
    negotiation = request.form.get('negotiation')
    fightResult = request.form.get('fightResult')
    reocurringIssues = request.form.get('reocurringIssues')
    frusturatedTime = request.form.get('frusturatedTime')
    relationalImpact = request.form.get('relationalImpact')
    conflictResolved = request.form.get('conflictResolved')
    parentExpectations = request.form.get('parentExpectations')
    addressIssue = request.form.get('addressIssue')
    issueLength = request.form.get('issueLength')
    idealSupport = request.form.get('idealSupport')
    optimalResources = request.form.get('optimalResources')
    upbringing = request.form.get('upbringing')

    try:
        # Connect to the database
        connection = connect_to_database()
        if connection is None:
            return "Failed to connect to the database"

        # Create a cursor object
        cursor = connection.cursor()

        # Create tables if they don't exist
        create_tables(cursor)

        # Execute SQL insert statement
        cursor.execute('''
            INSERT INTO credentials (fullName, email, DOB, birthTime, birthLocation)
            VALUES (%s, %s, %s, %s, %s);
        ''', (fullName, email, DOB, birthTime, birthLocation))
        cursor.execute('''
            INSERT INTO beforeKids (timeTogetherBefore, numDatesBefore, numIntimacyBefore, numFightsBefore)
            VALUES (%s, %s, %s, %s);
        ''', (time_together_before, num_dates_before, num_intimacy_before, num_fights_before))
        cursor.execute ('''
            INSERT INTO afterKids (timeTogetherAfter, numDatesAfter, numIntimacyAfter, numFightsAfter)
            VALUES (%s, %s, %s, %s);
        ''', (time_together_after, num_dates_after, num_intimacy_after, num_fights_after))
        cursor.execute ('''
            INSERT INTO idealMarriage (timeTogetherIdeal, numDatesIdeal, numIntimacyIdeal, numFightsIdeal, idealMarriage)
            VALUES (%s, %s, %s, %s, %s);
        ''', (timeTogetherIdeal, numDatesIdeal, numIntimacyIdeal, numFightsIdeal, idealMarriage))
        cursor.execute ('''
            INSERT INTO generalQuestions (marriageChange, changeFeeling, negotiation, fightResult, reocurringIssues, frusturatedTime,relationalImpact, conflictResolved, parentExpectations, addressIssue, issueLength, idealSupport, optimalResources, upbringing)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        ''', (marriageChange, changeFeeling, negotiation, fightResult, reocurringIssues, frusturatedTime,relationalImpact, conflictResolved, parentExpectations, addressIssue, issueLength, idealSupport, optimalResources, upbringing))


        # Commit the transaction
        connection.commit()

        # Close cursor and database connection
        cursor.close()
        connection.close()

        return redirect('/')
    except psycopg2.connector.Error as e:
        print("Error executing SQL statement:", e)
        return "An error occurred while processing your request"

if __name__ == '__main__':
    app.run(debug=True)
