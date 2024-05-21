from fastapi import FastAPI, HTTPException
import mysql.connector
from mysql.connector import Error

app = FastAPI()

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="mspr_infos"
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

@app.get("/espece/{id_especes}")
def get_espece_details(id_especes: int):
    db = get_db_connection()
    if db is None:
        raise HTTPException(status_code=500, detail="Database connection error")
    
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM espece WHERE id_especes = %s", (id_especes,))
    espece_data = cursor.fetchone()
    cursor.close()
    db.close()

    if espece_data:
        return espece_data
    else:
        raise HTTPException(status_code=404, detail="Espece not found")

if __name__ == "__main__":
    import uvicorn
    from fastapi.responses import JSONResponse
    from fastapi import Request

    uvicorn.run(app, host="localhost", port=8000)

@app.route("/get-espece/{id_especes}")
def get_espece(id_especes):
    response = JSONResponse(content=_fetchEspeceData(id_especes))
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

def _fetchEspeceData(id_especes):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="mspr_infos"
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM espece WHERE id_especes = %s", (id_especes,))
            espece_data = cursor.fetchone()
            cursor.close()
            connection.close()
            return espece_data
        else:
            return {"error": "Cannot connect to database"}
    except Error as e:
        return {"error": f"Error connecting to MySQL: {e}"}
