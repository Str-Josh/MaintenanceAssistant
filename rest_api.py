# API for database management generalization


class MaintenanceAssistantAPI():
    def __init__(self, db):
        self.db = db


    def access_field_filtered(self, modelType, filter_by_cat, filter_by_query):
        try:
            modelType.query.filter_by(filter_by_cat = filter_by_query)
        except Exception:
            raise ValueError("Unexpected error has occurred.")


    def add_row(self, modelType, data = [{}], multiple_addition=False):
        if not data or not data[0]:
            raise ValueError("Data param must contain contents.")
        
        # if modelType not in ["User", "Asset", "Messages", "Activity", "ActivityAssetUser"]:
        #     raise ValueError(f"Expected a valid modelType but got: {modelType}")
        
        if multiple_addition:
            modelTypeInstances = []
            for datum in data:
                modelTypeInstances.append(modelType(**datum))
            self.db.session.add_all(modelTypeInstances)
        else:
            # _ = modelType(data[0])
            self.db.session.add(modelType(data[0]))
        
        try:
            self.db.session.commit()
        except Exception:
            raise Exception("modelType already has element.")


    def delete_row(self, modelType, data = {}):
        if not modelType:
            raise ValueError("modelType must be a valid SQL Table but got: {modelType}.")
        if modelType not in ["User", "Asset", "Messages", "Activity", "ActivityAssetUser"]:
            raise ValueError("modelType must be a valid SQL Table but got: {modelType}.")
        
        if not data:
            raise ValueError("Data param must contain contents.")

        self.db.delete(data)
        try:
            self.db.commit()
        except Exception:
            raise Exception(f"Database already contains a definition for {modelType} with the associated data.")
