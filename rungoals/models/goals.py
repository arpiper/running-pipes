from bson import ObjectId

class Goals(dict):
    connnection = None

    def init_app(self, connection):
        self.connection = connection.goals

    def save(self, goal):
        if not goal._id:
            resultid = self.connection.insert_one(goal).inserted_id
        else:
            resultid = self.connection.update_one(
                {'_id': ObjectId(goal._id)}, 
                goal
            ).upserted_id
        return resultid

    def get_one(self, goalid):
        return self.connection.find_one({
            '_id': ObjectId(goalid)
        })

    def get_many(self, userid):
        cursor = self.connection.find({
            'userid': userid,
        })
        goals = []
        for goal in cursor:
            goals.append(goal)
        return goals
