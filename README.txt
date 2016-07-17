The docker image created after (remove sudo if on Mac OS X)
'$ sudo docker build -t hw1:latest .' 
and 
'$ sudo docker run -p 49160:8080 -d' 
works to all the asg1 specifications. The docker image works at http://localhost 

We initially tested out our docker image on Mac OS X, where the docker website specifies that a docker image's available ip address
is located at 192.168.99.100:port# on OSX and Windows systems, but otherwise on all other systems it should be located at localhost:port#. 

The testing commands worked perfectly fine on an ubuntu system.