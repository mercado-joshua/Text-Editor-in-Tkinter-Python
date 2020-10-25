#===========================
# Imports
#===========================

import tkinter as tk
from tkinter import ttk, colorchooser as cc, Menu, Spinbox as sb, scrolledtext as st, messagebox as mb, filedialog as fd

import os

#===========================
# Main App
#===========================

class SearchTopLevel(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.init_config()
        self.init_UI()
        self.init_events()

    # ==========================================
    def init_config(self):
        self.title('Find Text')
        self.transient(self.parent)
        self.resizable(False, False)

    # ==========================================
    def init_events(self):
        self.protocol('WM_DELETE_WINDOW', self.close_window)

    # ==========================================
    def init_UI(self):
        self.frame = ttk.Frame(self)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        label = ttk.Label(self.frame, text='Find All:')
        label.pack(anchor=tk.NW)

        self.search = tk.StringVar()
        self.entry = ttk.Entry(self.frame, width=25, textvariable=self.search)
        self.entry.pack(anchor=tk.NW)
        self.entry.focus_set()

        self.ignore_case = tk.IntVar()
        checkbutton = ttk.Checkbutton(self.frame, text='Ignore Case', variable=self.ignore_case)
        checkbutton.pack(anchor=tk.NW)

        button = ttk.Button(self.frame, text='Find All', underline=0, command=self.search_output)
        button.pack(anchor=tk.NW)

    def search_output(self):
        needle = self.search.get()
        case = self.ignore_case.get()

        self.parent.textarea.tag_remove('match', '1.0', tk.END)
        matches_found = 0

        if needle:
            start_pos = '1.0'

            while True:
                start_pos = self.parent.textarea.search(needle, start_pos, nocase=case, stopindex=tk.END)

                if not start_pos:
                    break

                end_pos = f'{start_pos}+{len(needle)}c'
                self.parent.textarea.tag_add('match', start_pos, end_pos)
                matches_found += 1
                start_pos = end_pos

            self.parent.textarea.tag_config('match', foreground='red', background='yellow')

        self.entry.focus_set()
        self.title(f'{matches_found} matches found')

    def close_window(self):
        self.parent.textarea.tag_remove('match', '1.0', tk.END)
        self.destroy()
        return 'break'

class App(tk.Tk):
    """Main Application."""
    icons = ['new', 'open', 'save', 'cut', 'copy', 'paste', 'undo', 'redo', 'find']
    color_schemes = {
        'Default': '#000000.#FFFFFF',
        'Greygarious' : '#83406A.#D1D4D1',
        'Aquamarine' : '#5B8340.#D1E7E0',
        'Bold Beige' : '#4B4620.#FFF0E1',
        'Cobalt Blue' : '#ffffBB.#3333aa',
        'Olive Green' : '#D1E7E0.#5B8340',
        'Night Mode' : '#FFFFFF.#000000',
        }
    filename = None

    # ==========================================
    def __init__(self):
        super().__init__()
        self.init_config()
        self.init_UI()
        self.init_events()

    def init_config(self):
        self.geometry('850x550+0+0')
        self.iconbitmap('notepad.ico')
        self.title('Footprint Editor')
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

    def init_events(self):
        self.protocol('WM_DELETE_WINDOW', self.mb_exit)
        self.textarea.bind('<KeyPress-F1>', self.mb_help)
        self.textarea.bind('<Control-Y>', self.redo)
        self.textarea.bind('<Control-y>', self.redo)
        self.textarea.bind('<Control-f>', self.find)
        self.textarea.bind('<Control-F>', self.find)
        self.textarea.bind('<Control-A>', self.select)
        self.textarea.bind('<Control-a>', self.select)

        self.textarea.bind('<Control-N>', self.new)
        self.textarea.bind('<Control-n>', self.new)
        self.textarea.bind('<Control-O>', self.open)
        self.textarea.bind('<Control-o>', self.open)
        self.textarea.bind('<Control-S>', self.save)
        self.textarea.bind('<Control-s>', self.save)

        self.textarea.bind('<Any-KeyPress>', self.on_content_changed)
        self.textarea.tag_configure('active_line', background='ivory2')

        self.textarea.bind('<Button-3>', self.show_popupmenu)
        self.textarea.focus_set()

    def init_UI(self):
        self.frame = ttk.Frame(self)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.new_icon = tk.PhotoImage(file='__Final/_PORTFOLIO/_projects/Text Editor/icons/new.gif')
        self.open_icon = tk.PhotoImage(file='__Final/_PORTFOLIO/_projects/Text Editor/icons/open.gif')
        self.save_icon = tk.PhotoImage(file='__Final/_PORTFOLIO/_projects/Text Editor/icons/save.gif')
        self.cut_icon = tk.PhotoImage(file='__Final/_PORTFOLIO/_projects/Text Editor/icons/cut.gif')
        self.copy_icon = tk.PhotoImage(file='__Final/_PORTFOLIO/_projects/Text Editor/icons/copy.gif')
        self.paste_icon = tk.PhotoImage(file='__Final/_PORTFOLIO/_projects/Text Editor/icons/paste.gif')
        self.undo_icon = tk.PhotoImage(file='__Final/_PORTFOLIO/_projects/Text Editor/icons/undo.gif')
        self.redo_icon = tk.PhotoImage(file='__Final/_PORTFOLIO/_projects/Text Editor/icons/redo.gif')

        # -------------------------------------
        menubar = tk.Menu(self.frame)
        file = Menu(menubar, tearoff=0)
        file.add_command(label='New', accelerator='Ctrl+N', compound='left', image=self.new_icon, underline=0, command=self.new)
        file.add_command(label='Open', accelerator='Ctrl+O', compound='left', image=self.open_icon, underline=0, command=self.open)
        file.add_command(label='Save', accelerator='Ctrl+S', compound='left', image=self.save_icon, underline=0, command=self.save)
        file.add_command(label='Save as', accelerator='Shift+Ctrl+S', command=self.saveas)
        file.add_separator()
        file.add_command(label='Exit', accelerator='Alt+F4')
        menubar.add_cascade(label='File', menu=file)

        edit = Menu(menubar, tearoff=0)
        edit.add_command(label='Undo', accelerator='Ctrl+Z', compound='left', image=self.undo_icon, command=self.undo)
        edit.add_command(label='Redo', accelerator='Ctrl+Y', compound='left', image=self.redo_icon, command=self.redo)
        edit.add_separator()
        edit.add_command(label='Cut', accelerator='Ctrl+X', compound='left', image=self.cut_icon, command=self.cut)
        edit.add_command(label='Copy', accelerator='Ctrl+C', compound='left', image=self.copy_icon, command=self.copy)
        edit.add_command(label='Paste', accelerator='Ctrl+V', compound='left', image=self.paste_icon, command=self.paste)
        edit.add_separator()
        edit.add_command(label='Find', underline=0, accelerator='Ctrl+F', command=self.find)
        edit.add_separator()
        edit.add_command(label='Select All', underline=7, accelerator='Ctrl+A', command=self.select)
        menubar.add_cascade(label='Edit', menu=edit)

        view = Menu(menubar, tearoff=0)
        self.show_linebar_number = tk.IntVar()
        self.show_linebar_number.set(1)
        view.add_checkbutton(label='Show Line Number', variable=self.show_linebar_number, command=self.update_line_numbers)

        self.show_cursor_info = tk.IntVar()
        self.show_cursor_info.set(1)
        view.add_checkbutton(label='Show Cursor Location at Bottom', variable=self.show_cursor_info, command=self.show_statusbar)

        self.highlight = tk.BooleanVar()
        view.add_checkbutton(label='Highlight Current Line', onvalue=1, offvalue=0, variable=self.highlight, command=self.toggle_highlight)

        themes = Menu(menubar, tearoff=0)
        view.add_cascade(label='Themes', menu=themes)

        self.theme_choice = tk.StringVar()
        self.theme_choice.set('Default')

        for color in sorted(self.color_schemes):
            themes.add_radiobutton(label=color, variable=self.theme_choice, command=self.change_theme)

        menubar.add_cascade(label='View', menu=view)

        about = Menu(menubar, tearoff=0)
        about.add_command(label='About', command=self.mb_about)
        about.add_command(label='Help', command=self.mb_help)
        menubar.add_cascade(label='About',  menu=about)

        self.config(menu=menubar)

        # -------------------------------------
        toolbar = ttk.Frame(self.frame, height=25)
        toolbar.pack(expand=tk.NO, fill=tk.X)

        for icon in self.icons:
            toolbar_icon = tk.PhotoImage(file=f'__Final/_PORTFOLIO/_projects/Text Editor/icons/{icon}.gif')
            cmd = eval(f'self.{icon}')
            toolbar_button = ttk.Button(toolbar, image=toolbar_icon, command=cmd)
            toolbar_button.image = toolbar_icon
            toolbar_button.pack(side=tk.LEFT, pady=2, padx=(2, 0))

        self.linebar = tk.Text(self.frame, background='khaki', width=4, padx=3, takefocus=0,  border=0, state=tk.DISABLED, wrap=tk.NONE)
        self.linebar.pack(side=tk.LEFT,  fill=tk.Y)

        self.textarea = tk.Text(self.frame, wrap=tk.WORD, undo=1, borderwidth=0, highlightthickness=0)
        self.textarea.pack(expand=tk.YES, fill=tk.BOTH, anchor=tk.CENTER)

        self.scrollbar = ttk.Scrollbar(self.textarea)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar.config(command=self.on_scroll)

        self.textarea['yscrollcommand'] = self.on_textscroll
        self.linebar['yscrollcommand'] = self.on_textscroll

        # -------------------------------------
        self.statusbar = ttk.Frame(self, height=25)
        self.statusbar.pack(side=tk.TOP, expand=tk.NO, fill=tk.X, anchor=tk.SW)

        self.cursorinfo = ttk.Label(self.statusbar, text='Line: 1 | Column: 1')
        self.cursorinfo.pack(anchor=tk.SE)

        # -------------------------------------
        # set up the pop-up menu
        self.popupmenu = Menu(self.textarea, tearoff=0)
        for name in ('cut', 'copy', 'paste', 'undo', 'redo'):
            cmd = eval(f'self.{name}')
            self.popupmenu.add_command(label=name, compound='left', command=cmd)
        self.popupmenu.add_separator()
        self.popupmenu.add_command(label='Select All', underline=7, command=self.select)


    # EVENTS -------------------------
    def show_popupmenu(self, event):
        self.popupmenu.tk_popup(event.x_root, event.y_root)

    def show_statusbar(self):
        checked = self.show_cursor_info.get()
        if checked:
            self.statusbar.pack(side=tk.TOP, expand=tk.NO, fill=tk.X, anchor=tk.SW)
        else:
            self.statusbar.pack_forget()

    def update_cursor_info_bar(self, event=None):
        row, col = self.textarea.index(tk.INSERT).split('.')
        line_num, col_num = str(int(row)), str(int(col) + 1)  # col starts at 0

        infotext = f'Line: {line_num} | Column: {col_num}'
        self.cursorinfo.config(text=infotext)

    # change themes
    def change_theme(self, event=None):
        selected_theme = self.theme_choice.get()
        fg_bg_colors = self.color_schemes.get(selected_theme)

        foreground_color, background_color = fg_bg_colors.split('.')
        self.textarea.config(background=background_color, fg=foreground_color)

    def on_scroll(self, *args):
        """Scrolls both text widgets when the scrollbar is moved."""
        self.textarea.yview(*args)
        self.linebar.yview(*args)

    def on_textscroll(self, *args):
        """Moves the scrollbar and scrolls text widgets when the mousewheel is moved on a text widget"""
        self.scrollbar.set(*args)
        self.on_scroll('moveto', args[0])

    def highlight_line(self, interval=100):
        self.textarea.tag_remove('active_line', 1.0, tk.END)
        self.textarea.tag_add('active_line', 'insert linestart', 'insert lineend+1c')
        self.textarea.after(interval, self.toggle_highlight)

    def undo_highlight(self):
        self.textarea.tag_remove('active_line', 1.0, tk.END)

    def toggle_highlight(self, event=None):
        if self.highlight.get():
            self.highlight_line()
        else:
            self.undo_highlight()

    def get_line_numbers(self):
        output = ''
        if self.show_linebar_number.get():
            row, col = self.textarea.index(tk.END).split('.')
            for i in range(1, int(row)):
                output += f'{str(i)}\n'
        return output

    def update_line_numbers(self, event=None):
        line_numbers = self.get_line_numbers()
        self.linebar.config(state=tk.NORMAL)
        self.linebar.delete('1.0', tk.END)
        self.linebar.insert('1.0', line_numbers)
        self.linebar.see(tk.END)
        self.linebar.config(state=tk.DISABLED)

    def on_content_changed(self, event=None):
        self.update_line_numbers()
        self.update_cursor_info_bar()

    def mb_about(self, event=None):
        mb.showinfo('About', 'Message')

    def mb_help(self, event=None):
        mb.showinfo('Help', 'Message', icon='question')

    def mb_exit(self, event=None):
        if mb.askokcancel('Quit?', 'Really quit?'):
            self.destroy()

    def new(self, event=None):
        self.title('Untitled')
        self.filename = None
        self.textarea.delete(1.0, tk.END)
        self.on_content_changed()

    def open(self, event=None):
        name = fd.askopenfilename(
            defaultextension='.txt',
            filetypes=[('All Files', '*.*'), ('Text Documents', '*.txt')]
            )

        if name:
            self.filename = name
            self.title(f'{os.path.basename(self.filename)} - Untitled')
            self.textarea.delete(1.0, tk.END)

            with open(self.filename) as _file:
                self.textarea.insert(1.0, _file.read())

        self.on_content_changed()

    def __write(self, filename):
        try:
            content = self.textarea.get(1.0, tk.END)
            with open(filename, 'w') as the_file:
                the_file.write(content)

        except IOError:
           mb.showwarning('Save', 'Could not save the file.')

    def saveas(self, event=None):
        name = fd.asksaveasfilename(
            defaultextension='.txt',
            filetypes=[('All Files', '*.*'), ('Text Documents', '*.txt')]
            )

        if name:
            self.filename = name
            self.__write(self.filename)
            self.title(f'{os.path.basename(self.filename)} - Untitled')
        return 'break'


    def save(self, event=None):
        if not self.filename:
            self.saveas()
        else:
            self.__write(self.filename)
        return 'break'

    def find(self, event=None):
        self.searchbar = SearchTopLevel(self)
        self.searchbar.grab_set()
        return 'break'

    def select(self, event=None):
        self.textarea.tag_add(tk.SEL, '1.0', tk.END)
        return 'break'

    def cut(self):
        self.textarea.event_generate('<<Cut>>')
        self.on_content_changed()
        return 'break'

    def copy(self):
        self.textarea.event_generate('<<Copy>>')
        return 'break'

    def paste(self):
        self.textarea.event_generate('<<Paste>>')
        self.on_content_changed()
        return 'break'

    def undo(self):
        self.textarea.event_generate('<<Undo>>')
        self.on_content_changed()
        return 'break'

    def redo(self, event=None):
        self.textarea.event_generate('<<Redo>>')
        self.on_content_changed()
        return 'break'


#===========================
# Start GUI
#===========================

def main():
    app = App()
    app.mainloop()

if __name__ == '__main__':
    main()