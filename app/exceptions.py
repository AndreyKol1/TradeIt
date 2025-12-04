
class ExternalAPIError(Exception):
    def __init__(self, service: str, message: str):
        self.service = service 
        self.message = message 
        super().__init__(f"{service}: {message}")

class DataParsingError(Exception):
    """Failure in parsing argument from extracted data"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

    
