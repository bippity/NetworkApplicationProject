# How to run this
* Assuming Mininet and x11/xming is already setup via the guides/tutorials
* Connect to Mininet VM via SSH(putty)

1) Setup the Mininet topology.
    ```sudo python startMininet.py```
    
2) Should now be inside Mininet CLI, open xterm for all 3 hosts.
    ```mininet> xterm h1 h2 h3```
    
3) Open up the corresponding programs for each host.
    * h1 = Controller, h2 = Server, h3 = Renderer
    
    ```
    python controller.py
    python server.py
    python renderer.py
    ```
