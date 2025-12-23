class ExternalAPIError(Exception):
    """API call error"""

    def __init__(self, service: str, message: str):
        self.service = service 
        self.message = message 
        super().__init__(f"{service}: {message}")

class DataParsingError(Exception):
    """Failure in parsing argument from extracted data"""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)

class InvalidCryptoNameError(Exception):
    """Failure in retrieving information about provided cryptocurrency"""

    def __init__(self, service: str, message: str):
        self.service = service
        self.message = message
        super().__init__(f"{service}: {message}")

class DataBaseConnectionError(Exception):
    """Failure in connection to the database"""

    def __init__(self, message: str):
        self.message = message 

        super().__init__(message)

    
