# COMP 4102 Final Project
-----------

|||||
|:---|:---|:---|:---|
|Name|Jiahe Geng | Yuhua Chen | Jiacheng Tang|
|Student ID|101056037|101035484|101038546|
|E-mail|jiahegeng@cmail.carleton.ca|yuhuachen@cmail.carleton.ca|jiachengtang@cmail.carleton.ca|

###Notice:
Befor you execute `.py`, please 
make sure that the file path in the code is correct
and the environment is correct. 

###Library:
|||
|:---|:---|
|numpy|1.18.1
|opencv-python|3.4.2.16
|opencv-contrib-python|3.4.2.16
|imutils|0.5.3
|lazy-object-proxy|1.4.3
|PyMySQL|0.9.3


### Files:
* `campusCard_recognition.py` files is the main program, cannot run with Pycharm (can work on console or Terminal)
* `student_info_student` file is database
* `card 1 - card4` example image for testing

### Instruction:
- Background:
To install MySQL and MySQL Workbench, you could watch the following video:
For Windows 10: https://www.youtube.com/watch?v=WuBcTJnIuzo
For Mac OS X: https://www.youtube.com/watch?v=UcpHkYfWarM
i.e. when you install the MySQL please set the Password to "12345678" 
(then you can skip "Connect database" part)

- Import the "student_info" database:
Please ensure that MySQL and MySQL Workbench is installed.
1. Open MySQL Workbench
2. Find "MySQL Connections", and point local instance.
3. Choose "Administration"(besides "Schemas"), and point "Data Import/Restore".
4. Choose "Import from Dump Project Folder", and type in the path of "database" file holder. (which include in our project file)
5. Point "Start Import" (In the lower-left corner)
6. Choose "Schemas", check all of your schemas, if you can see the "student_info", you import successfully. 

- Import PyMySQL library:
Since the system is written by Python, you need to import PyMySQL. (i.e. PyMySQL is a library used to connect to the MySQL server in the Python 3.x version)
Before using PyMySQL, we need to ensure that PyMySQL is installed.
	$ pip3 install PyMySQL

- Connect database:
1. Open the campusCard_recognition.py.
2. Find all "pymysql.connect". (CTRL+F)		i.e. the system use pymysql.connect() to establish a connection to our MySQL database
3. Set up the arguments. pymysql.connect() accepts several arguments:
	1. host – Host where the database server is located. (use "localhost" for here)
	2. user – Username to log in as. (use "root" for here)
	3. password – Password to use. (password for your database)
	4. database – Database to use, None to not use a particular one. (use "student_info" for here)
	5. port – MySQL port to use, default is usually OK. (default: 3306)

- Lanuch the main program:
1. Make sure you have install required libraries
2. Use command "python3 campusCard_recognition.py" to launch the program
    1. For detect student by using computer's front camera, press the button "Turn on your camera", and place the student card in the GREEN rectangle. PRESS "q" to take the photo
    (Due to resolution of front camera, the performance of recognition using front camera have lower accuracy and might require take photos for several times)
    2. For detect student by using local image, press the button "Upload". Try to upload the image that take from phone's camera which has higher resolution or use attached example images.
    3. To close the result image, do not click red cross in the top left, press any keystroke to close that window. 
