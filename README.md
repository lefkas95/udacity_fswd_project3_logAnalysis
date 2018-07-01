# Log analysis tool

## Desription

This python program executes three SQL-queries against a postgresql database called news to answer the following questions:
* What are the most popular three articles of all time?
* Who are the most popular article authors of all time?
* On which days did more than 1% of requests lead to errors?

## Requirements

Please install the following programs (if not done before) in order to be able to use the log analysis tool:

* Vagrant - Deployment tool (https://www.vagrantup.com/)
* VirtualBox - A virtual maschine (https://www.virtualbox.org/)

## Run it

In order to run the program you will have to setup the database behind. Fortunately the given vagrant file creates the neccessary environment
and the `news` database. Go into the `vagrant` folder and execute the command `vagrant up`. Afterwards connect to the VM using `vagrant ssh`.

Now import the schema and data to the `news` database using a python script, which can be downloaded under 
`https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip`.
Run it like `psql -d news -f newsdata.sql`. Now the database is set up and filled with data.

To run the program call `python logAnalysis.py`

There must be an active postgresql database on the machine in order to work!
