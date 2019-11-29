Environment:
* Mininet 2.2.2 - Ubuntu 14.04 LTS - 32 bit
* Python3 (3.4.3)
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
