# TouchNet Discovery
 A simple discovery protocol for TouchDesigner

## Overview
The TouchNet Discovery module has two modes: Client and Server. The terminology is admittedly somewhat inappropriate, but stems from the fact that this tox is an offshoot from a larger project that uses a Client-Server architecture, and, as such, there are some important differences between the two modes.

As of version 1, it is fairly bare bones, and would require some attention to fit a particular use-case. My hope is that in time people will find their own applications, and an API can be built out to address those use-cases.

### Getting Started
Navigate to the **/Build** folder in the package and drag and drop the component in a TouchDesigner network. If on a strictly peer network (no servers) fill in an **`Alias`** for your instance to go by, hit **`Initialize`** (just for good measure) and then **`Enable`**. You shoudl be ready to go. Read below for an explanation of Server/Client modes and other parameters.

### Client Mode
This is the default mode of the module. An **`Alias`** must be assigned, then the user should initialize and enable the module using the provided custom parameters. At that point, the module will begin sending a discovery announcment message at regular intervals on a multicast address. Clients and servers both listen for and respond to these messages.

### Server Mode
In server mode, the module does not send out a discovery announcement, it only listens and responds. If the **`Search Forever`** parameter is disabled on the Client, it will stop sending announcements as soon as it hears a response from the Server.

How the information provided to each instance is used is entirely up to the user. It is also the responsibility of the user to monitor the connection between multiple clients.

## Custom Parameters
**`Alias`**: This is simple, user-assigned name given to a TouchDesigner instance.  

**`Mode`**: See above for a short explanation of the two selectable modes.  

**`Initialize`**: Destroys all data relating to discovered peers.  

**`Enable`**: Enables network listening and announcements.  

**`Manual Send`**: Forces a discovery announcement outside of the module's regular period.  

**`Search Forever`**: When enabled, the Client will continue sending discovery announcements after receiving a response from the Server. Disabling this can help reduce multicast traffic. Clients will always respond to their peers' discovery announcements, so even with this switched off, they will still all find each other.

**`Timeout`**: [Not implemented] The amount of time for which the Client will send announcement messages without hearing any responses.  

**`Local Address`**: The IP address of the host machine.  

**`Discovery Port`**: The port that the Client will listen on for discovery responses. It is recommended to change this **only** when there are two clients on the same machine, this ensures that each client has its own connection to the server or its peers. 

**`TouchNet`**: [For future use]  

## Outputs
The DAT output is a table containing all connected peers and basic information about the machine/project.

## Network Protocol
### Overview
The client joints multicast group 239.255.22.22:9099 and sends a Discovery Announcement packet every 2 seconds. When a server sees that packet it sends a discovery response.

Discovery Announcment Packet Definition:  

	{
		"type":"1",
		"hostname":<name of host machine>,
		"ip":<ip address of host machine>,
		"projectName":<name of the TD project file>
	}

Discovery Response Packet Definition:  

	{
		"type":"2",
		"ip":<ip address of responder>,
		"port":<touchnet port>
	}
