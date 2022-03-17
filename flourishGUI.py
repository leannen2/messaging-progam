# a5.py
#
# ICS 32
#
# v0.4
#
# The following module provides a graphical user interface shell for the DSP journaling program.

import pathlib
import time
from Contact import Contact
import ds_messenger as ds_msg
import ds_protocol as dsp
from NaClProfile import MessengerProfile
from Profile import Post
from turtle import bgcolor
from tkinter import ttk, filedialog, messagebox, simpledialog
import tkinter as tk
from logging import root
HOST = '168.235.86.101'
PORT = 3021

# import ds_client


"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the body portion of the root frame.
"""


class Body(tk.Frame):
    def __init__(self, root, select_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._select_callback = select_callback

        # list of contacts loaded from the dsu file
        self.contacts = []
        self.current_recipient = None
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Body instance
        self._draw()

    """
    Update the entry_editor with the full post entry when the corresponding node in the posts_tree
    is selected.
    """

    def node_select(self, event):
        index = int(self.posts_tree.selection()[0])
        entry = self.contacts[index].msg_log
        self.current_recipient = index
        print('current recipient', self.contacts[self.current_recipient].name)
        self.set_text_entry(entry)

    def node_index_select(self):
        """
        Returns contact that is selected from the tree
        """
        index = int(self.posts_tree.selection()[0])
        return self.contacts[index]

    """
    Returns the text that is currently displayed in the entry_editor widget.
    """

    def get_text_entry(self) -> str:
        return self.msgentry_editor.get('1.0', 'end').rstrip()

    """
    Sets the text to be displayed in the entry_editor widget.
    NOTE: This method is useful for clearing the widget, just pass an empty string.
    """

    def set_text_entry(self, text: str):
        self.msg_text.delete(0.0, 'end')
        self.msg_text.insert(0.0, text)

    def set_bot_text_entry(self, text: str):
        self.msgentry_editor.delete(0.0, 'end')
        self.msgentry_editor.insert(0.0, text)

    """
    Populates the self._posts attribute with posts from the active DSU file.
    """

    def set_contacts(self, contacts: list):
        self.contacts = contacts
        for id, contact in enumerate(self.contacts):
            self._insert_post_tree(id, contact)

    def update_contacts(self, contacts: list):
        self.contacts = contacts

    """
    Inserts a single contact to the post_tree widget.
    """

    def insert_contact(self, contact: Contact):
        self._posts.append(contact)
        id = len(self._posts) - 1  # adjust id for 0-base of treeview widget
        self._insert_post_tree(id, contact)

    """
    Resets all UI widgets to their default state. Useful for when clearing the UI is neccessary such
    as when a new DSU file is loaded, for example.
    """

    def reset_ui(self):
        self.set_text_entry("")
        self.msg_text.configure(state=tk.NORMAL)
        self._posts = []
        for item in self.posts_tree.get_children():
            self.posts_tree.delete(item)

    """
    Inserts a post entry into the posts_tree widget.
    """

    def _insert_post_tree(self, id, contact: dict):
        entry = contact.name
        # Since we don't have a title, we will use the first 24 characters of a
        # post entry as the identifier in the post_tree widget.
        if len(entry) > 25:
            entry = entry[:24] + "..."

        self.posts_tree.insert('', id, id, text=entry)

    '''def _add_contact(self, id, contact_name):
        self.posts_tree.insert('', id, id, text=contact_name)
        self.contacts.append(contact_name)'''

    """
    Call only once upon initialization to add widgets to the frame
    """

    def night_mode_on(self):
        pass

    def night_mode_off(self):
        pass

    def _draw(self):
        posts_frame = tk.Frame(master=self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT)
        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)

        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP,
                             expand=True, padx=5, pady=5)
        # main frame
        entry_frame = tk.Frame(master=self, bg="")
        entry_frame.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
        #
        messages_frame = tk.Frame(master=entry_frame, bg="red")
        messages_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        scroll_frame = tk.Frame(master=entry_frame, bg="blue", width=10)
        scroll_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        self.msg_text = tk.Text(messages_frame, width=0)

        self.msg_text.configure(state='disabled')
        self.msg_text.pack(fill=tk.BOTH, side=tk.LEFT,
                           expand=True, padx=0, pady=0)

        msg_scrollbar = tk.Scrollbar(
            master=scroll_frame, command=self.msg_text.yview)
        self.msg_text['yscrollcommand'] = msg_scrollbar.set
        msg_scrollbar.pack(
            fill=tk.Y, side=tk.LEFT, expand=False, padx=0, pady=0)

        entry_frame = tk.Frame(master=self, bg="blue")
        entry_frame.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=True)

        self.msgentry_editor = tk.Text(
            entry_frame, width=0)
        self.msgentry_editor.pack(
            fill=tk.BOTH, side=tk.BOTTOM, expand=True)
        # this sets the entry but takes over the Send button


"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the footer portion of the root frame.
"""


class Footer(tk.Frame):
    def __init__(self, root, save_callback=None, online_callback=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._save_callback = save_callback
        self._online_callback = online_callback
        # IntVar is a variable class that provides access to special variables
        # for Tkinter widgets. is_online is used to hold the state of the chk_button widget.
        # The value assigned to is_online when the chk_button widget is changed by the user
        # can be retrieved using he get() function:
        # chk_value = self.is_online.get()
        self.is_online = tk.IntVar()
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the Footer instance
        self._draw()

    """
    Calls the callback function specified in the online_callback class attribute, if
    available, when the chk_button widget has been clicked.
    """

    def online_click(self):
        if self._online_callback is not None:
            self._online_callback(self.is_online.get())

    """
    Calls the callback function specified in the save_callback class attribute, if
    available, when the save_button has been clicked.
    """

    def save_click(self):
        if self._save_callback is not None:
            self._save_callback()

    """
    Updates the text that is displayed in the footer_label widget
    """

    def set_status(self, message):
        self.footer_label.configure(text=message)

    """
    Call only once upon initialization to add widgets to the frame
    """

    def _draw(self):
        save_button = tk.Button(master=self, text="Send", width=20, fg="blue")
        save_button.configure(command=self.save_click)
        save_button.pack(fill=tk.BOTH, side=tk.RIGHT, padx=5, pady=5)

        '''self.chk_button = tk.Checkbutton(
            master=self, text="Online", variable=self.is_online)
        self.chk_button.configure(command=self.online_click)
        self.chk_button.pack(fill=tk.BOTH, side=tk.RIGHT)'''

        self.footer_label = tk.Label(master=self, text="Ready.")
        self.footer_label.pack(fill=tk.BOTH, side=tk.LEFT, padx=5)


"""
A subclass of tk.Frame that is responsible for drawing all of the widgets
in the main portion of the root frame. Also manages all method calls for
the NaClProfile class.
"""


class MainApp(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self._is_online = False
        self._profile_filename = pathlib.Path().resolve() / 'messages.dsu'
        # Initialize a new NaClProfile and assign it to a class attribute.
        self._current_profile = MessengerProfile()
        # self._current_profile.load_profile(self._profile_filename)
        # self.open_profile()
        self.profileloaded = False
        # After all initialization is complete, call the _draw method to pack the widgets
        # into the root frame
        self._draw()

    """
    Creates a new DSU file when the 'New' menu item is clicked.
    """

    def new_profile(self):
        try:
            filename = tk.filedialog.asksaveasfile(
                filetypes=[('Distributed Social Profile', '*.dsu')])
            self._profile_filename = filename.name
            self._current_profile = MessengerProfile()
            self._current_profile.dsuserver = '168.235.86.101'
            self._current_profile.username = 'iJustGotDivorced'
            self._current_profile.password = 'KanyeYE'
            self._current_profile.save_profile(self._profile_filename)
            self.body.reset_ui()
            print(self._current_profile.keypair)
        except:
            print('error')

    """
    Opens an existing DSU file when the 'Open' menu item is clicked and loads the profile
    data into the UI.
    """

    def open_profile(self):
        # try:
        # filename = tk.filedialog.askopenfile(
        #     filetypes=[('Distributed Social Profile', '*.dsu')])
        # self._profile_filename = filename.name
        self._current_profile = MessengerProfile()
        self._current_profile.load_profile(self._profile_filename)
        self.profileloaded = True
        print(self._current_profile.username)
        self.body.reset_ui()
        self.body.set_contacts(self._current_profile.get_contact_objs())
        # except:
        #     print("Error")

    """
    Closes the program when the 'Close' menu item is clicked.
    """

    def close(self):
        self.root.destroy()

    """
    Saves the text currently in the entry_editor widget to the active DSU file.
    """

    def save_profile(self):
        # contact = Contact(self.body.node_index_select().name, self.body.get_text_entry())
        # self.body.insert_contact(contact)
        recipient = self.body.node_index_select().name
        msg = self.body.get_text_entry()

        dir_msg = ds_msg.DirectMessage(
            recipient, msg, time.time(), self._current_profile.username)
        self._current_profile.add_sent_msg(dir_msg)
        self._current_profile.save_profile(self._profile_filename)
        self.body.update_contacts(self._current_profile.get_contact_objs())

        self.body.set_bot_text_entry("")
        dsm = ds_msg.DirectMessenger(
            HOST, self._current_profile.username, self._current_profile.password)
        dsm.send(message=msg, recipient=recipient)
        # self.body.reset_ui()
        # self.body.set_contacts(self._current_profile.get_contact_objs())
        # self.body.set_text_entry(self.body.current_recipient.msg_log)
        # index = int(self.body.posts_tree.selection()[0])

        # print('index, ', index_of_recipient)
        # print('contacts', self.body.contacts)
        index_of_recipient = self.body.current_recipient
        entry = self.body.contacts[index_of_recipient].msg_log

        self.body.msg_text.delete(0.0, 'end')

        self.body.msg_text.insert(0.0, entry)
        # self.body.node_select()

    """
    Publishes to the server if online widget is checked
    """

    # def publish(self, post: Post):
    #     host = '168.235.86.101'
    #     port = 3021
    #     usr = self._current_profile.username
    #     pwd = self._current_profile.password
    #     entry = post['entry']
    #     ds_client.send(host, port, usr, pwd, entry)

    """
    A callback function for responding to changes to the online chk_button.
    """

    def online_changed(self, value: bool):
        if value == 1:
            self._is_online = True
        else:
            self._is_online = False

    def add_contact(self):
        # response = messagebox.askokcancel(
        # 'Add Username', "Enter username of recipient you wish to add")

        # if response == 1:
        # print('yes')

        contact_name = simpledialog.askstring(
            'Add Contact', 'What is the username of your new contact?')
        id = len(self.body.contacts)
        self._add_contact(id, contact_name)

    def _add_contact(self, id, contact_name):
        self.body.posts_tree.insert('', id, id, text=contact_name)
        new_contact = Contact(contact_name, '')
        self.body.contacts.append(new_contact)
        self._current_profile.add_contact_profile(contact_name)
        self._current_profile.save_profile(self._profile_filename)

        #messagebox.showinfo('Hello!', 'Hi, {}'.format(name))

    def new_messages(self):
        if self.profileloaded == True:
            # user = ds_msg.DirectMessenger(
            #     '168.235.86.101', 'iJustGotDivorced', 'KanyeYE')
            # x = user.retrieve_new()
            # self._current_profile.add_retrieved_msg()
            # print(self._current_profile.retrieved_msg)
            # messages = dsp.extract_messages(x)
            # for dic in messages:
            #     if len(dic) > 0:
            #         self.body.set_text_entry(dic['message'])
            dsm = ds_msg.DirectMessenger(
                HOST, self._current_profile.username, self._current_profile.password)

            # retrieved = dsm.retrieve_new()
            # if len(retrieved) > 0:
            # print('before:', self._current_profile.retrieved_msg)
            new = self._current_profile.add_retrieved_msg()
            self._current_profile.save_profile(self._profile_filename)
            if new:
                self.body.update_contacts(
                    self._current_profile.get_contact_objs())
                index_of_recipient = self.body.current_recipient
                entry = self.body.contacts[index_of_recipient].msg_log

                self.body.msg_text.delete(0.0, 'end')
                self.body.msg_text.insert(0.0, entry)
                print('new msg!')
            else:
                print('no new msg')
            # print('after:', self._current_profile.retrieved_msg)

        self.root.after(2000, self.new_messages)

    def night_mode_on(self):
        self.body.msg_text.configure(bg='black', fg='white')
        self.body.msgentry_editor.configure(bg='black', fg='white')
        style = ttk.Style()
        # style.theme_use('clam')
        style.configure("Treeview", background='black', fieldbackground='black',
                        foreground='white')

    def night_mode_off(self):
        self.body.msg_text.configure(bg='white', fg='black')
        self.body.msgentry_editor.configure(bg='white', fg='black')
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background='white', fieldbackground='white',
                        foreground='black')

    """
    Call only once, upon initialization to add widgets to root frame
    """

    def _draw(self):
        # Build a menu and add it to the root frame.
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_file = tk.Menu(menu_bar)
        menu_setting = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu=menu_file, label='File')
        menu_bar.add_cascade(menu=menu_setting, label='Settings')
        menu_setting.add_command(label='Add Contact', command=self.add_contact)
        menu_setting.add_command(
            label='Night Mode On', command=self.night_mode_on)
        menu_setting.add_command(
            label='Night Mode Off', command=self.night_mode_off)
        menu_file.add_command(label='New', command=self.new_profile)
        menu_file.add_command(label='Open...', command=self.open_profile)
        menu_file.add_command(label='Close', command=self.close)
        # NOTE: Additional menu items can be added by following the conventions here.
        # The only top level menu item is a 'cascading menu', that presents a small menu of
        # command items when clicked. But there are others. A single button or checkbox, for example,
        # could also be added to the menu bar.

        # The Body and Footer classes must be initialized and packed into the root window.
        self.body = Body(self.root, self._current_profile)
        self.body.pack(fill=tk.BOTH, side=tk.TOP, expand=True)

        self.footer = Footer(
            self.root, save_callback=self.save_profile, online_callback=self.online_changed)
        self.footer.pack(fill=tk.BOTH, side=tk.BOTTOM)


if __name__ == "__main__":
    # All Tkinter programs start with a root window. We will name ours 'main'.
    main = tk.Tk()

    # 'title' assigns a text value to the Title Bar area of a window.
    main.title("ICS 32 Distributed Social Messenger")

    # This is just an arbitrary starting point. You can change the value around to see how
    # the starting size of the window changes. I just thought this looked good for our UI.
    main.geometry("850x670")

    # adding this option removes some legacy behavior with menus that modern OSes don't support.
    # If you're curious, feel free to comment out and see how the menu changes.
    main.option_add('*tearOff', False)

    # Initialize the MainApp class, which is the starting point for the widgets used in the program.
    # All of the classes that we use, subclass Tk.Frame, since our root frame is main, we initialize
    # the class with it.
    app = MainApp(main)
    # When update is called, we finalize the states of all widgets that have been configured within the root frame.
    # Here, Update ensures that we get an accurate width and height reading based on the types of widgets
    # we have used.
    # minsize prevents the root window from resizing too small. Feel free to comment it out and see how
    # the resizing behavior of the window changes.
    main.update()
    main.minsize(main.winfo_width(), main.winfo_height())
    # And finally, start up the event loop for the program (more on this in lecture).
    main.after(2000, app.new_messages)
    main.mainloop()
