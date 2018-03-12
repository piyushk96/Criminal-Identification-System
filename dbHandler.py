import pymysql

def insertData(data):
    rowId = 0

    db = pymysql.connect("localhost", "criminaluser", "", "criminaldb")
    cursor = db.cursor()
    print("database connected")

    query = "INSERT INTO criminaldata VALUES(0, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % \
            (data["Name"], data["Father's Name"], data["Mother's Name"], data["Gender"],
             data["DOB(yyyy-mm-dd)"], data["Blood Group"], data["Identification Mark"],
             data["Nationality"], data["Mother Tongue"], data["Crimes Done"])

    try:
        cursor.execute(query)
        db.commit()
        print("data inserted")
        rowId = cursor.lastrowid
    except:
        db.rollback()
        print("Data insertion failed")


    db.close()
    print("connection closed")
    return rowId

