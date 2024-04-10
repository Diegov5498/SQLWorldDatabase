import sqlite3
import mysql.connector
import random

# Connect to the MySQL server
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="password",
    database="world"
)
cursor = conn.cursor()

#Create a random triplet of values
def randomTriplet()->list:
    return [random.randint(0,1000) for _ in range(3)]

#Create a random percent
def randomPercent(min, max)->float:
    number = random.randint(min,max)
    decimal = round(random.random(),2)
    return number+decimal

#Get a list of table names
def printTableNames()->None:
    # Execute the query to retrieve table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    # Fetch all rows from the cursor
    rows = cursor.fetchall()
    # Extract table names from the rows
    tableNames = [row[0] for row in rows]
    
    print(tableNames)


#Generate Olympic Medals Table and Values
def generateOlympicMedals():
    #Create table if it does not exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS OlympicMedals (
                    countryCode CHAR(3) PRIMARY KEY,
                    gold INTEGER,
                    silver INTEGER,
                    bronze INTEGER
                )''')
    #Get a list of distinct countries
    cursor.execute("SELECT DISTINCT code FROM Country")
    countries = cursor.fetchall()
    #Iterate through each country and insert a medal value for each
    for country in countries:
        medals = randomTriplet()
        data = {
            'CountryCode': country[0],
            'Gold': medals[0],
            'Silver': medals[1],
            'Bronze': medals[2]
            }
        #Insert
        cursor.execute('''INSERT INTO OlympicMedals (CountryCode,Gold,Silver,Bronze)
                        VALUES (%(CountryCode)s, %(Gold)s, %(Silver)s, %(Bronze)s)''', data)
    #Add total column at the end
    cursor.execute('''ALTER TABLE OlympicMedals
                  ADD COLUMN totalMedals INTEGER GENERATED ALWAYS AS (Gold+Silver+Bronze);''')
    #Commit
    conn.commit()
    print("Successfully Added OlympicMedals Table")

#Create Continent
def generateContinent():
    #Create table if it does not exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS Continent (
                    Continent VARCHAR(20) PRIMARY KEY,
                    SurfaceArea FLOAT,
                    Population INTEGER,
                    GNP FLOAT
                   )''')
    #List of continents
    continents = ['North America', 'South America', 'Oceania', 'Asia', 'Europe', 'Africa', 'Antartica']
    #Iterate for each value
    for continent in continents:
        #Get surface area
        cursor.execute("SELECT SUM(SurfaceArea) FROM Country WHERE continent = %s", (continent,))
        surfaceArea = cursor.fetchone()[0]
        #Get population
        cursor.execute("SELECT SUM(Population) FROM Country WHERE continent = %s", (continent,))
        population = cursor.fetchone()[0]
        #Get GNP
        cursor.execute("SELECT SUM(GNP) FROM Country WHERE continent = %s", (continent,))
        gnp = cursor.fetchone()[0]
        data = {
            'Continent': continent[0],
            'SurfaceArea': surfaceArea,
            'Population': population,
            'GNP': gnp
            }
        #Insert into table
        cursor.execute('''INSERT INTO Continent (Continent,SurfaceArea,Population,GNP)
                            VALUES(%(Continent)s, %(SurfaceArea)s, %(Population)s, %(GNP)s)''', data)
    #Commit
    conn.commit()
    print("Successfully Added Continent Table")

def generateHealth():
    #Create table if it does not exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS Health (
                    CityID INTEGER PRIMARY KEY,
                    Mortality FLOAT,
                    Birth FLOAT,
                    Obesity FLOAT,
                    STI FLOAT,
                    Diabetes FLOAT
                    CoVid FLOAT
                   )''')
    #Get a list of distinct cities
    cursor.execute("SELECT DISTINCT ID FROM City")
    cities = cursor.fetchall()
    #Iterate through each city and enter values for health
    for city in cities:
        #Mortality per thousand
        mortality = random.randint(0,3)
        #Birth rate per thousand
        birth = random.randint(5,50)
        #Obesity
        obesity = randomPercent(0,75)
        #STI
        sti = randomPercent(0,35)
        #Diabetes
        diabetes = randomPercent(2,25)
        #CoVid
        covid = randomPercent(1,5)
        #Insert into table
        cursor.execute('''INSERT INTO Health (CityID,Mortality,Birth,Obesity,STI,Diabetes,CoVid)
                            VALUES (?,?,?,?,?,?,?)''', (city[0],mortality,birth,obesity,sti,diabetes,covid))
    #Commit
    conn.commit()

#Main Function
def main():
    if conn.is_connected():
        print("Connected to MySQL server")
        #generateOlympicMedals()
        generateContinent()
        #generateHealth()
    else:
        print("Execution Unsuccessful")

    conn.close()

#Execute
if __name__ == "__main__":
    main()
