import customtkinter as ctk
import os

class HelpScreen(ctk.CTkFrame):
    '''
    Shows information about the application.
    '''
    def __init__(self, root, screen_changer):
        super().__init__(root, width=root.winfo_width(), height=root.winfo_height())
        self._screen_changer = screen_changer
        _scroll_frame_wid = self.cget('width') // 4.5
        _scroll_frame_hei = self.cget('height') * .73
        
        # this screen's widgets
        _help_label = ctk.CTkLabel(self, text='Help', font=ctk.CTkFont(size=40))
        _about_label = ctk.CTkLabel(self, text='About', font=ctk.CTkFont(size=25))
        _launch_label = ctk.CTkLabel(self, text='Launch Screen', font=ctk.CTkFont(size=25))
        _settings_label = ctk.CTkLabel(self, text='Settings Screen', font=ctk.CTkFont(size=25))
        _about_frame = ctk.CTkFrame(self, width=_scroll_frame_wid, height=_scroll_frame_hei)
        _launch_frame = ctk.CTkFrame(self, width=_scroll_frame_wid, height=_scroll_frame_hei)
        _settings_frame = ctk.CTkFrame(self, width=_scroll_frame_wid, height=_scroll_frame_hei)
        _back_button = ctk.CTkButton(self, text='Back', command=lambda: self._screen_changer('MainScreen'))
        
        # placing widgets on this screen
        _help_label.place(relx=.5, rely=0.05, anchor=ctk.CENTER)
        _about_label.place(relx=.25, rely=0.15, anchor=ctk.CENTER)
        _launch_label.place(relx=.5, rely=0.15, anchor=ctk.CENTER)
        _settings_label.place(relx=.75, rely=0.15, anchor=ctk.CENTER)
        _about_frame.place(relx=.25, rely=0.55, anchor=ctk.CENTER)
        _launch_frame.place(relx=.5, rely=0.55, anchor=ctk.CENTER)
        _settings_frame.place(relx=.75, rely=0.55, anchor=ctk.CENTER)
        _back_button.place(relx=.5, rely=0.95, anchor=ctk.CENTER)

        # about section of help
        _about_text = self._remove_newline(os.path.join('assets', 'about.txt'))
        _about_label_text = ctk.CTkTextbox(_about_frame, width=_scroll_frame_wid, height=_scroll_frame_hei, font=ctk.CTkFont(size=15), wrap=ctk.WORD)
        _about_label_text.insert('0.0', _about_text)
        _about_label_text.grid(row=0, column=0, padx=5, pady=5)
        _about_label_text.config(state=ctk.DISABLED)
        
        # launch section of help
        _launch_text = self._remove_newline(os.path.join('assets', 'launch.txt'))
        _launch_label_text = ctk.CTkTextbox(_launch_frame, width=_scroll_frame_wid, height=_scroll_frame_hei, font=ctk.CTkFont(size=15), wrap=ctk.WORD)
        _launch_label_text.insert('0.0', _launch_text)
        _launch_label_text.grid(row=0, column=0, padx=5, pady=5)
        _launch_label_text.config(state=ctk.DISABLED)
        
        # settings section of help
        _settings_text = self._remove_newline(os.path.join('assets', 'settings.txt'))
        _settings_label_text = ctk.CTkTextbox(_settings_frame, width=_scroll_frame_wid, height=_scroll_frame_hei, font=ctk.CTkFont(size=15), wrap=ctk.WORD)
        _settings_label_text.insert('0.0', _settings_text)
        _settings_label_text.grid(row=0, column=0, padx=5, pady=5)
        _settings_label_text.config(state=ctk.DISABLED)
    
    def _remove_newline(self, text_file):
        with open(text_file, "r") as file:
            content = file.read()
        
        # remove newline characters
        content.replace('\n', ' ')
        
        # put back the newline characters for double spaces
        return content.replace('  ', '\n')