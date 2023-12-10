# Import the Model, View, and Controller classes from respective modules
from model import Model
from view import View
from controller import Controller

# Import the tkinter module and alias it as tk
import tkinter as tk


# Create a class for the main application, inheriting from tkinter's Tk class
class App(tk.Tk):
    def __init__(self):
        # Initialize the main application window using the Tk constructor
        super().__init__()

        # Set the title of the application
        self.title('S.P.I.D.A.M.')

        # Create an instance of the Model class, passing the current instance of App
        model = Model(self)

        # Create an instance of the View class, passing the current instance of App
        view = View(self)

        # Place the View widget in the main window with grid layout and padding
        view.grid(row=0, column=0, padx=10, pady=10)

        # Create an instance of the Controller class, passing the Model and View instances
        controller = Controller(model, view)

        # Set the controller for the view
        view.set_controller(controller)


# Check if the script is being run as the main program
if __name__ == '__main__':
    # Create an instance of the App class, initiating the application
    app = App()

    # Start the main event loop of the Tkinter application
    app.mainloop()
