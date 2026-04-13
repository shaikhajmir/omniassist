from motor.motor_asyncio import AsyncIOMotorClient

# Replace with your MongoDB connection string
# For local dev without a DB setup, we'll use a mocked memory store list if it fails.
MONGO_URL = "mongodb://localhost:27017"

class Database:
    def __init__(self):
        try:
            self.client = AsyncIOMotorClient(MONGO_URL, serverSelectionTimeoutMS=2000)
            self.db = self.client.omniassist
            self.alerts_collection = self.db.alerts
            self.connected = True
        except Exception:
            self.connected = False
            self.mock_db = []

    async def insert_alert(self, alert_data):
        if self.connected:
            try:
                result = await self.alerts_collection.insert_one(alert_data)
                alert_data['_id'] = str(result.inserted_id)
                return alert_data
            except Exception:
                # Fallback to mock
                pass
        self.mock_db.append(alert_data)
        return alert_data

    async def get_alerts(self):
        if self.connected:
            try:
                cursor = self.alerts_collection.find().sort("timestamp", -1).limit(50)
                alerts = await cursor.to_list(length=50)
                for alert in alerts:
                    alert['_id'] = str(alert['_id'])
                return alerts
            except Exception:
                pass
        return self.mock_db

db = Database()
