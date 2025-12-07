Hello there, welcome to the Home Buyer Helper installation guide!
~~~~~~~~~~~~
So you want to use Home Buyer Helper program to start house hunting and planning?
You're in luck, here's the simple plan...

1.) A file in this directory named "requirements.txt" is provided which lists all the version numbers,
    and library names that this project is depended on. Install those in order to run the program.

2.) Alright, so lets get that database setup. Home Buyer Helper expects a PostgreSQL server to connect to.
    The following are the information on how the server needs to be created.
    Any modification to the following will require matching changes to the variables within DatabaseInteraction.py
   
    -Name = "HomeBuyer"
    -User = "postgres"
    -Pass = "password"
    -Host = "127.0.0.1" --> Change to your own if you wish to host.
    -Port = "5432"      --> Default local port, change if you are hosting.

    The tables and connection are automatically created and held if no existsing database is detected.
    So simply, run the program after you have started a PostgresSQL server.

3.) Start home hunting!