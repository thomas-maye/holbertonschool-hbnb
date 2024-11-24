from app.services.facade import HBnBFacade

facade = None  # Placeholder for the facade instance

def initialize_facade(app):
    global facade
    with app.app_context():
        facade = HBnBFacade()  # Initialize the HBnBFacade
