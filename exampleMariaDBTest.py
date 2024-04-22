from time import perf_counter
import os
import mysql.connector
from mysql.connector.aio import connect
import asyncio

QUERY = 'SELECT user,host FROM mysql.user;'

def runSync():
    db = mysql.connector.connect(
        host=HOST,
        port=PORT,
        user=USER,
        password=PASW,
        # buffered=True,
    )
    data = {}
    with db.cursor(dictionary=True) as cursor:
        cursor.execute(QUERY)
        data = cursor.fetchall()
        # for result in data:
        #     print(result)
    db.close()
    return data

async def runAsync():
    results = {}
    # Connect to a MySQL server and get a cursor
    cnx = await connect(host=HOST,
                        port=PORT,
                        user=USER,
                        password=PASW)
    async with await cnx.cursor(dictionary=True) as cursor:
        # Execute a non-blocking query
        await cursor.execute(QUERY)
        # Retrieve the results of the query asynchronously
        results = await cursor.fetchall()
    # await cursor.close() # why call this? isn't htis closed in cntxt mgr?
    await cnx.close()
    return results

    # Close cursor and connection
    
if __name__ == "__main__":
    
    start = perf_counter()
    asyncio.run(runAsync())
    print(f"ASYNC took: {perf_counter() - start:.3f}")
    
    start = perf_counter()
    runSync()
    print(f"SYNC took: {perf_counter() - start:.3f}")