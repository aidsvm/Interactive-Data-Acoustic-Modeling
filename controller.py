class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Connect the View to the Controller
        # self.view.controller = self

    def load_audio(self, file_path):
        self.model.file_path = file_path
        time, waveform = self.model.load_audio()

        self.view.update_filename_label(os.path.basename(dst))
        self.view.update_rt60_label(sample_data['rt60'])
        self.view.update_waveform_plot(sample_data['waveform'])
        self.view.update_additional_plot(sample_data['additional_data'])
