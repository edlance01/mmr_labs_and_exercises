
from gui_module.base_controller import BaseController
from gui_module.app import app


class RealController(BaseController):

    def retrieve_response(self, user_input):
        print(f"The user input was: {user_input}")
        response = user_input.lower()
        return response

    if __name__ == "__main__":
        app.run(debug=True, port=8082)  # Run the Flask app with debugging enabled on
