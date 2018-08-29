class Users():

    # Connection to the mongodb users collection.
    connection = None
    
    def init_app(self, connection):
        self.connection = connection.users

    def get_one(self, userid):
        return self.connection.find_one({
            '_id': userid
        })

    def save(self, user):
        if not user._id:
            resultid = self.connection.insert_one(user).inserted_id
        else:
            resultid = self.connection.update_one(
                {'_id': ObjectId(user._id)},
                user
            ).upserted_id
        return resultid

