class ComplaintStatusEventService:

    def __init__(self, event_repository):
        self.event_repository = event_repository

    def create_event(self, db, event):
        return self.event_repository.create(db, event)

    def get_events(self, db):
        return self.event_repository.get_all(db)