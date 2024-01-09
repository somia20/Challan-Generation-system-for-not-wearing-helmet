Challan Generation System for Not Wearing Helmet

This project is a Flask-based web application designed to manage and generate traffic violation challans for individuals caught not wearing helmets while riding motorcycles. 

The system provides an efficient way to record violations, issue challans, and maintain a digital record of the violation. Additionally, the system sends SMS and email notifications to the admin when a violation is recorded.

![without challan](https://github.com/somia20/Challan-Generation-system-for-not-wearing-helmet/assets/108867754/1cf37774-557f-4037-aa4b-86185b2a8e3e)


![helmet detected](https://github.com/somia20/Challan-Generation-system-for-not-wearing-helmet/assets/108867754/21d42cfa-ee5f-43de-b1a3-092ed7e7d85e)





Features - 

User Registration: Individuals can register their details, including name, contact information, and vehicle details.

Helmet Detection: The system utilizes helmet detection technology to determine whether a helmet is worn or not.

Violation Recording: The system allows for the recording of instances when individuals are not wearing helmets, capturing details such as the date, time, and a photo for documentation.

Challan Generation: If a helmet is not detected, the system automatically generates a challan with relevant details such as the offender's name, vehicle information, violation date, and a fine amount. If a helmet is detected, a message is sent indicating that no challan is generated.

Notification to Admin: The system sends SMS and email notifications to the admin when a violation is recorded, providing details of the incident.

Data Storage: Violation records are stored in a SQLite database for future reference and analysis.


