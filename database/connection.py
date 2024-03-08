import pymongo

class MongoDBConnection:
    def __init__(self, host, port, username=None, password=None, database_name=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database_name = database_name
        self.client = None

    def connect(self):
        try:
            # Establish connection to MongoDB
            self.client = pymongo.MongoClient(host=self.host, port=self.port)
            # Select the database
            if self.database_name:
                self.db = self.client[self.database_name]
            return True
        except pymongo.errors.ConnectionFailure as e:
            print(f"Failed to connect to MongoDB: {e}")
            return False

    def disconnect(self):
        try:
            if self.client:
                self.client.close()
        except Exception as e:
            print(f"Error while disconnecting from MongoDB: {e}")

