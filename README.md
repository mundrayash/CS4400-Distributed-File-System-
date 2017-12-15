# CS4400-Distributed-File-System-
Student: Yash Mundra
Student No.: 16338461

A simple distributed file system coded in python 3.0. The system has features like a directory server and a locking server.

# Directory Server
The directory server keeps two local MongoDb databases. When the client makes a request, the directory server checks for the location of the file in file servers using the IP and port of the file server. The databases stores the location of the files and the machine in which it is present.

# Locking Server
It stores the database of files which are locked and unlocked. The client when perfoms a write operation, the locking server locks the file and the client is given full access to the file.

# Run
The system has bash scripts to run the system. The REST system uses Flask framework. The scripts should be run in the following order.
* Database - db_run.sh
* Directory Server - ds_run.sh
* Locking Server - ls_run.sh
* File Server - node_run.sh




