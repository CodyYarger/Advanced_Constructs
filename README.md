
# Lesson 9

# Introduction

Your functional rewrite of the application has proved to be very successful, and defect rates have dropped as testing is now easier. But the real test of that is now comping, as you have requirements to add new functionality to the application.

You have received many requests to add images to the application. Users want to be able to add their latest pictures, and have these stored for later use.

Obviously, you will continue to use a functional approach for development. And since you are now making more use of a database you will write a context manager to oversee your database connections.

Filing and retrieving images is quite complex, and you will introduce logging so that you can observe any issues that may have occurred when the program is running.

# What to do

1. Be sure to use unit tests as you develop your code!

1. Start with your completed solution to lesson 8. Replace your database connection logic with a connection manager. You will need to write the connection manager to work with DataSet, and then change your code so that it uses your new connection manager.

1. You will create a new table in the database called Picture. This table will store a unique id for each picture, will have a foreign key back to the Users table, and a character field called *tags*. *tags* is a string that contains one or more tags that start with the # symbol and contain a short descriptive name for the image. Each tag is separated by a space. So an example of the #tag field will look like this:

    #house #family #andy_miles

Note that tags can only contain upper and lower case letters and underscore. No spaces (since that separates tags!).

* Here are the details of the *Picture* table:
    * picture_id (Primary Key).
    * user_id (Foreign Key from the *Users* table).
    * #tags (limited to 100 characters).

1. For this exercise we will assume that the images themselves are all png files (ie they end in .png). The file name for the picture will be the picture_id from the database, which should be a zero padded string that is incremented by one for each picture (for example 0000000001.png, 0000000002.png). 0000000001 etc will be the picture id in the database.

2. THe images need to be stored in a specific structure on disk. Each user will have a directory in which their images are stored. The name of that directory will be the value of the user_id field from the users table. Then, the images are stored in that directory for the specific user as follows:

    the #tags for the image must first be sorted. Then, each tag in sequence represents a directory level for that user. So, for example, if the tag string is #car #sports then the image would be stored in the following directory:

    user_id_value\car\sports (or user_id_value/car/sports on Mac or linux) where user_id_value is replaced by the corresponding key from the database.

3. Note that images may have to be stored in new or existing directories depending on the tag values, and that images can be stored at any level (so in the above example you could later add an image to the car directory).

4. **Also note that for this assignment you will not need to store the images themselves. You will just be storing the image file names.**

5. Create a decorator that you can use to add logging where it is needed in your code.

6. Add logging to your code to help you to investigate any issues that may occur when the program runs.

7. Write a function to list all of a users images. The function, called ```list_user_images``` will take a user_id as a parameter, and will return a list of tuples. Each tuple will contain the user_id, the full path to the image file, and the image file name. For example:
    ("1234", "00001\car\sports", "00004.png")

    ```list_user_images``` must use recursion to navigate through the image directory structure.

8. Write a further function to compare list_user_images with what is stored in your image database table. This new function, called ```reconcile_images```, will list any images record on disk that are not in the database, and any in the database that are not on disk. Use unit tests to prove that this functionality works.

9. Don't forget to add an option in ```menu.py``` to add images and list all user images (note you do not need to deal with deleting or amending images).

# Submission

The following files need to be submitted:

* *main.py*.
* *menu.py*.
* *user_status.py*.
* *users.py*.
* *test_unit.py*.
* *list_user_images.py*.

Any other files required by your implementation of this assignment.

# Other requirements

* Your code needs to be able to create the image directories and populate them with the names of image files. Note that you will not be storing any real image files; just their names.
* For testing, if your test database does not run from memory, you will need to add code to delete the .db file that is created after every test run.

# How will your code be evaluated?

* The instructor will delete any .db files and image directories included in the submission. This is to make sure your code can create and initialize a database file from scratch.
* The instructor will run *menu.py* and load sample CSV files into your SQL database. A SQL database inspector will be use to look at the table structure of your database, verify that the correct fields have been set as primary keys in each table, as well as that *UserID* has been set as foreign key in the *Status* table.
* The instructor will interact with your database using the user interface in *menu.py* and try to add and report upn images, checking that this is also reflecting in the database file and the images directory structure.
* The instructor will also try common error conditions: specifying invalid tags and tag structures. Your code should not crash due to these errors and please, no bare exceptions (most database errors will be *IntegrityError* exceptions).
* The instructor will look at your code and verify that all operations are being performed directly in the SQL database.

As usual, your code will need to be linted and score 10/10 on pylint.

# Tips

1. Develop each feature one at a time. Use unit testing to help!

2. Start with the context manager.

3. Consider adding the logging decorator next, as it it may help you to develop the functionality.

4. Then add tags to the database. The enable the tag functionality in the program.

5. Next, write the tags to disk.

6. Now write the reporting functionality

7. Amend menu.py

