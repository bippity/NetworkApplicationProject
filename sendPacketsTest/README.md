Simple repo to test sending a message

1. Setup the Single switch topology
    ```sudo python singleSwitchTopo.py```
2. Pull up the xterms for both hosts
    ```xterm h1 h2```
3. Run the client/server program on each host
    ```
       python server.py //run this first
       python client.py
    ```
    
* Server should receive the message that client sends
and then send it back to client.
