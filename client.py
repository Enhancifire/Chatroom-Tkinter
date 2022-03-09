import socket
import sys
import threading

import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = '127.0.0.1'
PORT = 2077

class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        msg = tkinter.Tk()
        msg.withdraw()

        self.nickname = simpledialog.askstring("Nickname", "Please choose a nickname", parent = msg)

        self.gui_done = False
        self.running = True

        self.gui_thread = threading.Thread(target=self.gui_loop)
        self.receive_thread = threading.Thread(target=self.receive)

        # self.gui_thread.daemon = True
        # self.receive_thread.daemon = True

        self.gui_thread.start()
        self.receive_thread.start()

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.configure(bg = "lightgray")

        self.chat_label = tkinter.Label(self.win, text="Chat:", bg="lightgray")
        self.chat_label.configure(font=("Arial", 12))

        self.chat_label.pack(padx = 20, pady = 5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
        self.text_area.pack(padx = 20, pady = 5)
        self.text_area.config(state = 'disabled')

        self.msg_label = tkinter.Label(self.win, text="Message:", bg="lightgray")
        self.msg_label.configure(font=("Arial", 12))

        self.msg_label.pack(padx = 20, pady = 5)

        self.input_area = tkinter.Text(self.win, height = 3)
        self.input_area.pack(padx = 20, pady = 5)

        self.send_button = tkinter.Button(self.win, text = "Send", command = self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx = 20, pady = 5)

        self.gui_done = True

        self.win.protocol("WM_DELETE_WINDOW", self.stop)
        self.win.mainloop()

    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)

    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')


    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == 'NICK':
                    self.sock.send(self.nickname.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state = 'normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state = 'disabled')

            except ConnectionAbortedError:
                self.sock.close()
                break

            except SystemExit:
                self.sock.close()
                print("Exit by system")

            except KeyboardInterrupt:
                print("Stopped manually")
                self.sock.close()

            except:
                print("Error")
                self.sock.close()
                sys.exit(0)



client = Client(host= HOST, port= PORT)
