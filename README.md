# Udacity catalog

The catalog project is a simple database project completed for Udacity's full-stack nanodegree program program. The project demostrates usage of CRUD techniques to talk to a database while implementing useful features with Flask

## Documentation



After ensuring you have both Vagrant and virtual box installed. Please follow the instructions below to run the project

1. Download or clone files
1. Navigate to tournament project folder cd /vagrant
1. Once inside of the vagrant folder run ```$ vagrant up ``` command in your terminal
1. After step 3 has been installed successfully. run ```$ vagrant ssh ``` inside of your terminal 
1. While you are in your vagrant env. Look for the directory catalog and cd into it
1. Execute the following command ```$  python database_setup.py && python database_items.py && python project.py ```
1. Open your browser and insert the following url: http://localhost:5333/