Environment:
* Mininet 2.2.2 - Ubuntu 14.04 LTS - 32 bit
* Python3 (3.4.3)

* Look at this if no host-only adapter selected (https://askubuntu.com/questions/198452/no-host-only-adapter-selected)
------------

* Run the program with "sudo python3 programName"
* Decode messages to UTF-8 before comparing (https://stackoverflow.com/questions/6269765/what-does-the-b-character-do-in-front-of-a-string-literal)
    
    EX: b'hello' is a Bytes literal, convert to "hello" using .decode("utf-8")
    ```
    b = b'hello'
    print(b.decode("utf-8"))
    ```

* The OS buffers bytes at the socket in its own tcp IP stack -> make sure to clear buffer out when restarting
* Should be running each program (Controller/Renderer/Server) in a separate mininet host. So 3 instances of Mininet.

* Each program needs a socket. But only the Renderer/Server need to listen to messages that might be received.
The Controller only needs a socket to send messages.

* Follow this guide to setup GUI/OpenFlow/xTerm - https://github.com/mininet/openflow-tutorial/wiki


Mininet Reminders/Tips
--------------
* Topology setup command:
    ``` sudo mn --topo single,3 --mac```
* Always cleanup Mininet using 
    ``` sudo mn -c ```
* Default switch (s1) runs in root network -> same thing as regular terminal/host
* You should be running commands from a SSH terminal (Putty[windows]/Terminal[Mac]), not directly in Mininet VM.
* "xterm h1 h2", not "h1 h2 xterm"

General Successful Flow
--------------
1) Controller requests a list of files from Server
2) Controller tells Renderer to request a file from Server
3) Server sends file to Renderer
4) Renderer displays the file (it does not send data back to Controller)
 ** Controller does not render anything, it just controls the Renderer and requests a list of files from Server
5) Controller tells Renderer to close file.
6) User tells Controller to exit...which tells everything else to stop?
