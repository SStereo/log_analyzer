Log File Analyzer
=================
This Project was created by SStereo in the context of the Udacity Full Stack Web Developer Nanodegree. It analyzes a given database of page views on articles written by authors. This program runs SQL queries against a given PostgreSQL database and shows the most popular articles, authors and shows the day when the webserver produced more than 1% of error codes. This program creates all necessary views in the database for the queries to run.

INSTALL & RUN
--------------------
1. Install Virtual Box (https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
2. Install Vagrant (https://www.vagrantup.com/downloads.html)
3. Download the VM configuration that includes the database (https://github.com/udacity/fullstack-nanodegree-vm)
4. Download the database dump from https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
5. Unzip the database dump after downloading. The file inside is called newsdata.sql. Put this file into the vagrant directory, which is shared with your virtual machine.
6. Copy the file "log_analyzer.py" into the vagrant directory
7. Turn on your virtual machine using "vagrant up" from the command line
8. log into your virtual machine using "vagrant ssh" from the command line
9. Change the folder to \vagrant
10. Upload the database dump by using the command "psql -d news -f newsdata.sql"
11. In the terminal run "python log_analyzer.py"

CONTACT
-------
You can contact me on GitHub under SStereo.

