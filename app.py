import falcon
import json
import MySQLdb as db
import datetime

db_connection = db.connect(user='root', passwd='lenovoflyq420', db='todo', host='91.214.114.115')
cursor = db_connection.cursor()

class NoteResource:

    def on_get(self, req, resp):
        """Handles GET requests"""
        resp.status = falcon.HTTP_200
        try:
            cursor.execute("SELECT * FROM notes")
            result = []
            columns = tuple([i[0] for i in cursor.description])
            
            for row in cursor:
                result.append(dict(zip(columns, row)))
            resp.body = json.dumps(result)
        except db.Error as e:
            resp.body = "ERROR: {}".format(e)
    
    def on_post(self, req, resp):
        """Handles POST requests"""
        try:
            raw_json = req.stream.read()
        except Exception as ex:
            raise falcon.HTTPError(falcon.HTTP_400,
                'Error',
                ex.message)
 
        try:
            result = json.loads(raw_json, encoding="utf-8")
            query = "INSERT INTO notes VALUES('{}', '{}', '{}')".format(
                datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
                result['author'],
                result['note']
            )
            cursor.execute(query)
            db_connection.commit()
        except ValueError:
            raise falcon.HTTPError(falcon.HTTP_400,
                'Invalid JSON',
                'Could not decode the request body. The '
                'JSON was incorrect.')


api = falcon.API()
api.add_route('/notes', NoteResource())
