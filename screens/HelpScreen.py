import customtkinter as ctk

class HelpScreen(ctk.CTkFrame):
    '''
    Shows information about the application.
    '''
    def __init__(self, root, screen_changer):
        super().__init__(root, width=root.winfo_width(), height=root.winfo_height())
        self._screen_changer = screen_changer
        _scroll_frame_wid = self.cget('width') // 4.5
        _scroll_frame_hei = self.cget('height') * .73
        print(f'{_scroll_frame_hei} {_scroll_frame_wid}')
        
        # this screen's widgets
        _help_label = ctk.CTkLabel(self, text='Help', font=ctk.CTkFont(size=40))
        _about_label = ctk.CTkLabel(self, text='About', font=ctk.CTkFont(size=25))
        _launch_label = ctk.CTkLabel(self, text='Launch Screen', font=ctk.CTkFont(size=25))
        _settings_label = ctk.CTkLabel(self, text='Settings Screen', font=ctk.CTkFont(size=25))
        _about_frame = ctk.CTkScrollableFrame(self, width=_scroll_frame_wid, height=_scroll_frame_hei)
        _launch_frame = ctk.CTkScrollableFrame(self, width=_scroll_frame_wid, height=_scroll_frame_hei)
        _settings_frame = ctk.CTkScrollableFrame(self, width=_scroll_frame_wid, height=_scroll_frame_hei)
        _back_button = ctk.CTkButton(self, text='Back', command=lambda: self._screen_changer('MainScreen'))

        # about section of help
        
        # launch section of help
        
        # settings section of help
        
        # placing widgets on this screen
        _help_label.place(relx=.5, rely=0.05, anchor=ctk.CENTER)
        _about_label.place(relx=.25, rely=0.15, anchor=ctk.CENTER)
        _launch_label.place(relx=.5, rely=0.15, anchor=ctk.CENTER)
        _settings_label.place(relx=.75, rely=0.15, anchor=ctk.CENTER)
        _about_frame.place(relx=.25, rely=0.55, anchor=ctk.CENTER)
        _launch_frame.place(relx=.5, rely=0.55, anchor=ctk.CENTER)
        _settings_frame.place(relx=.75, rely=0.55, anchor=ctk.CENTER)
        _back_button.place(relx=.5, rely=0.95, anchor=ctk.CENTER)