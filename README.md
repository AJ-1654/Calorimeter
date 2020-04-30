# Calorimeter #
A full stack web application that helps you track your dietary habits and calorie intake. Calorimeter allows users to estimate the calories
in any food item image with just one click. To estimate the calories, Calorimeter uses a food classification and calorie estimation model 
built by fine tuning Inception V3 pre trained network on 30 classes of FOOD-101 dataset. The following functionalities have been provided 
 
* Measure the calories in any food item image uploaded by a user. This feature helps users assess their dietary habits and encourages them to eat healthy
* Allow registered users to set fitness goals that they aim to achieve in a given timespan.
* Based on this aim, a calorie budget is assigned to the user to restrict his calorie intake.
* All meals (breakfast, lunch and dinner) of the user are then tracked. User uploads the food item image for each meal and the calorie measurement model used in Calorimeter estimates the calories in the food item consumed.
* The “View” tab under the “Current Goal” section keeps a record of all meals consumed by the user since the beginning of his fitness track. This helps the users keep a track of their progress and provide them incentive to further restrict their calorie intake to achieve their fitness goal.

## Installation Requirements ##
- Flask (1.1.2)
- flask-sqlalchemy
- flask-wtforms
- flask-login
- TensorFlow (1.15.1)
- Keras (2.3.1)
- NumPy (1.18.2)
- Matplotlib (3.1.3)
- OpenCV

## How To Run ##

* Activate the environment having all packages needed installed using the command: “conda activate my_env” (in Anaconda prompt)
* Move in the directory, using the cd command, into the “Calorimeter” folder
* Run the command: “python run.py”
* Copy the URL and paste it in your favourite browser window.
