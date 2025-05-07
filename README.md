# CS32-final-project
Final Project for  CS 32

A peer to peer messaging app like whatsapp made by Evelyn Gathara and Kwame Boateng.
This app provides a gui that can be used to send messages between two friends on the same network.

Instructions to Run.
1. Ensure that both computers are on the same network
2. Run the server.py located in the network folder on one computer.
3. Then run main.py on that same computer
4. Before you run main.py on the second computer, change the "SERVER IP" in client.py to the ip address of your first compluter(The one currently running server.py)
5. When the interface is opened, click on the "Profile" button to choose a new user name. You will have to close and reopen the app to save these changes.i.e close the interface and rerun main.py
6. Click on the "Add Friend/Connect" button and type in the field, the respective username of the other client
7. A message box should open. Type in your messages and hit enter to send

Note:
The two computers should be on the same network. You should also allow python.exe through the firewall on you computer. Finally, the scripts should be run on a local IDE because tkinter did not run on the cloud codespaces when we tested it.



External Contributors

We used generative AI to help debug parts of our code, especially the sections of the user interface that weren’t working properly with the other parts of the project.

We found these sources to be greatly helpful when dealing with multithreading, tkinter, json and databases
https://realpython.com/intro-to-python-threading/
https://www.freecodecamp.org/news/work-with-sqlite-in-python-handbook/
https://www.geeksforgeeks.org/python-tkinter-tutorial/?ref=outindfooter
https://www.geeksforgeeks.org/read-json-file-using-python/

