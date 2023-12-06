from model import Model
from view import View
from controller import Controller
import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        # Initialize the main application window
        super().__init__()

        # Set the title of the application
        self.title('S.P.I.D.A.M.')

        # Create a model
        model = Model(self)

        # Create a view and place it on the root window
        view = View(self)
        view.grid(row=0, column=0, padx=10, pady=10)

        # Create a controller
        controller = Controller(model, view)

        # Set the controller to the view
        view.set_controller(controller)


if __name__ == '__main__':
    # Create an instance of the application and start the main loop
    app = App()
    app.mainloop()
