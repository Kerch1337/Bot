
class DbSessionMiddleware:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def __call__(self, handler, event, data):
        with self.session_factory() as session:
            data["session"] = session
            return handler(event, data)