import customtkinter as ctk

class AboutScreen(ctk.CTkFrame):
    '''
    Shows information about the application.
    '''
    
    def __init__(self, root, screen_changer):
        super().__init__(root, width=root.winfo_width(), height=root.winfo_height())
        self._screen_changer = screen_changer

        # widget creation
        _back_button = ctk.CTkButton(self, text='Back', command=lambda: self._screen_changer('MainScreen'))
        _about_frame = ctk.CTkFrame(self, width=root.winfo_width() * .5, height=root.winfo_height() * .8)

        # loads text from 'help.txt' file and puts it into the about_frame
        with open('help.txt', 'r') as file:
            sections = file.read().split('\n')

        for i in range(0, len(sections)):
            if i % 2 == 0:
                _header_label = ctk.CTkLabel(_about_frame, text=sections[i], font=ctk.CTkFont(size=25))
                _header_label.grid(row=i, column=0, padx=5, pady=5)
            else:
                _body_label = ctk.CTkLabel(_about_frame, text=sections[i], font=ctk.CTkFont(size=15), wraplength=500)
                _body_label.grid(row=i, column=0, padx=5, pady=15)

        # widget placement
        _back_button.place(relx=.5, rely=0.95, anchor=ctk.CENTER)
        _about_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)