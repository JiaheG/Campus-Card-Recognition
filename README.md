# COMP 4102 Final Project
-----------

|||||
|:---|:---|:---|:---|
|Name|Jiahe Geng | Yuhua Chen | Jiacheng Tang|
|Student ID|101056037|101035484|101038546|
|E-mail|jiahegeng@cmail.carleton.ca|yuhuachen@cmail.carleton.ca|jiachengtang@cmail.carleton.ca|

### Summary:
The project will be focusing on solving the campus card recognition problem with the preposition camera of the personal computer device. And the recognition includes locating the campus card, recognizing the student number, the student name and the university on the card. After obtaining the information from the campus card, the program would try to match the student number and student name from different databases.

### Background:
As mentioned above, the goal of this project is to build a the project taht is a student information management system, which could scan and extract the information on the student card and compare it with the information in the database to quickly find the student information. The system will also display all the student information (i.e. first name, last name, department, total credit, etc.). What is more, the user could delete, update or add student information to the database. For the challenges of the project, even though the system is implemented by using some pre-existing functions in OpenCV and MySQL, but it still has to be able to recognize the object with a different and complicated environment and handle some problems with the picture such as glare in the photo or wrong direction of the photo. 

### The Challenge:
We will solve our problem by using just a few pre-existing functions in OpenCV. And we hope to practice the topics we have learned in class, such as image filtering, edge detection and so on. The program needs to be able to have the authority to the user’s camera and has the ability to recognise the object with a different and complicated environment. The program should also able to handle some problem with the picture such as glare in the photo or wrong direction of the photo. 
Given the goal, this project can be broken down into five problems. First, is the image capture. Next, is locating the card’s edges regardless of perspective. Also, locating the student number. Then, the application needs to recognize the digits of the student number. Finally, using the database to manipulate the student information.

### Goals and Deliverables:
#### I. Plan to achieve
The goal of the project is to build software that turns on the camera of the device,
take a picture of a student card, and capture the student information from the taken
image.
The software should also connect to a student information database and verify the
student information with the database. If the verification is successful, our program
will display the detailed information of this student. If the verification is
unsuccessful, Our program will display some suggestions. For example, ask the user
if he wants to add the information to the database, or correct the information of this
student.
#### II. Hope to achieve
If there is enough time, we could build a more complex ID recognition software that
can recognize different types of documents, such as a driver's license (or passport).
The software can distinguish the type of the document and use different interfaces
to process each of them.

### Schedule：
|||||
|:---|:---|:---|:---|
| |Jiahe Geng | Yuhua Chen | Jiacheng Tang|
|2.1 - 2.9|Research & learn OpenCV|Research & learn OpenCV|Research & learn OpenCV|
|2.10 - 2.16(Make the plan)|Draw a use case diagram|Draw a use case diagram|UI design|
|2.17 - 2.23 (reading week)start image information detection part|edge detection|Smooth the image|Positioning the card in the image|
|2.24 - 3.1|Positioning the card number|Positioning the card number|Positioning the card number|
|3.2 - 3.8 Finish image information detection part|Identify the number in the card & testing|dentify the number in the card & testing|dentify the number in the card & testing|
|3.9 - 3.15(Database Design)|Design SQL Database|Process the information on the card using Database|testing|
|3.16 - 3.29(Finish UI part)|Display the information on the card|Connect UI part with image information detection part|Connect UI part with Database part|
|3.30 - 4.10|testing|testing|testing|



### Notice:
Befor you execute `.py`, please 
make sure that the file path in the code is correct
and the environment is correct. 

### Library:
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
