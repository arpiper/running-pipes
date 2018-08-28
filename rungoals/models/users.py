class Users():

    # Connection to the mongodb users collection.
    connection = None
    
    def init_app(self, connection):
        self.connection = connection.users

    def get_one(self, userid):
        return self.connection.find_one({
            '_id': userid
        })

