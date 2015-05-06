from datetime import datetime
import MySQLdb
from config import DB, DB_USER,DB_PASS

def insertState(state):
    conn =  MySQLdb.connect(host="localhost", user=DB_USER, passwd=DB_PASS,db=DB)
    cursor=conn.cursor()
    select_state="SELECT ID FROM ACTIVITY_MODEL WHERE NAME=%s"
    cursor.execute(select_state, (state,))
    ids=cursor.fetchall()
    print ids
    id=ids[0][0]
    print id
    now=datetime.now()
    insert_state="INSERT INTO ACTIVITY (activity_model_id,timestamp) VALUES (%s,%s);"
    cursor.execute(insert_state,(int(id),now))
    conn.commit()

insertState("Cook")