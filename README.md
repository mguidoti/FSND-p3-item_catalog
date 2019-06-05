## Item Catalog
> This is the fourth project of the [Full Stack Web Development Nanodegree](https://in.udacity.com/course/full-stack-web-developer-nanodegree--nd004/) program, from Udacity.



### Overview

This project's goal was to create an item catalog backed with a full CRUD application, allowing to edit, delete and create new places (e.g., restaurants) and items on their catalogs (e.g., dishes). We also had to provide: 

* an API endpoint retrieving the same information available on HTML as JSON (e.g., list of places and all information available for each place's catalog, as well as for all users in the database)

* an Oauth2 login system to protect the CRUD application from unauthenticated and unauthorized users



In addition, [Python PEP8 style guide](https://www.python.org/dev/peps/pep-0008/) was required.



### Chosen Theme

For this project, I choose to create an initial version of an app that would gather information on health facilities, including the list of accepted health insurance provider and a list of available treatment with their prices as well, for each facility. The goal is to have an easy-to-use application to retrieve the nearest, or cheapest, facility for a given condition. This type of information, especially prices, is often hidden - thus, this could be actually useful if it was a real app. 

However, for this initial version, only a simple list of health insurance providers names were included, and no locality functionality were added besides the same fake address for every facility. 

In order to fill the databases for this project, I chose the list of diseases from the [EA classic Theme Hospital](https://www.ea.com/news/theme-hospital-is-on-the-house). I hope you, evaluator, will have the same laughs that I did when building this project!



### Installation Requirements and Used Setup

To run this application, I use [VirtualBox](https://www.virtualbox.org/wiki/Downloads) and [vagrant](https://www.vagrantup.com/downloads.html). 

Then, I forked this provided [repository](https://github.com/udacity/OAuth2.0), cloned to my computer, and ran the `pg_config.sh` in order to finish the VM setup. 

Then, I had to create a developer's account and register my application in the two used Oauth2 providers, [Google](https://console.developers.google.com) and [Facebook](https://developers.facebook.com). Finally, I downloaded my `client_secrets.json`, and included in the root folder of my application. My personal `client_secrets.json` are not included in this repository for security reasons. Please, use yours to properly run this application.



### How to run

Assuming that you've the same environment described above: 

1. First, you need to initiate the database: `python initiate_database.py`

2. Then, you've to fill it with data: python `fill_database.py`

3. Next, you need to run the webserver (that will be serving on the port 5000): `python hospitals.py`

4. Finally, you must access the project on your browser: `http://localhost:5000`



### Database

The database is named `themehospitals.db`, which is created and filled when running the first and second command, respectively, from [#How to Run](#how-to-run). Every additional time this command is used, more hospitals and users are included in the database, until all 50 hospital names and users names stored in the `data_source.py` are used. One user can have more than one health facility, or none. Real users (e.g., you) will never be assigned as owner of a automatically created facility. The program avoids name repetition as well. 

After the database is created and filled, you'll receive a status message with the number of hospitals and users included in that interaction, and the average number of conditions included for the new hospitals. There is no way, other than manually, to add conditions to existent hospitals. 

If you delete the database and run this command again, a new database will be created, randomly filling its tables.

The database is composed by three tables, as follows: 

##### User

| Column  | Type    | Modifiers/Foreign Relationship |
| ------- | ------- | ------------------------------ |
| id      | integer | not null default               |
| name    | text    | not null                       |
| gender  | text    | not null                       |
| email   | text    | not null                       |
| type    | text    | not null                       |
| picture | text    |                                |


##### Hospital

| Column             | Type    | Modifiers/Foreign Relationship |
| ------------------ | ------- | ------------------------------ |
| id                 | integer | not null default               |
| name               | text    | not null                       |
| accepted_insurance | text    | not null                       |
| address            | text    | not null                       |
| phone              | text    | not null                       |
| user_id            | integer | ForeignKey(User.id)            |

##### Condition

| Column      | Type    | Modifiers/Foreign Relationship |
| ----------- | ------- | ------------------------------ |
| id          | integer | not nul default                |
| name        | text    | not null                       |
| cause       | text    | not nul                        |
| sympton     | text    | not null                       |
| cure        | text    | not null                       |
| type        | text    | not null                       |
| cost        | text    | not null                       |
| hospital_id | integer | ForeignKey(Hospital.id)        |
| user_id     | integer | ForeignKey(User.id)            |



### Data & Images

The header image is based on the [Theme Hospital](https://www.ea.com/news/theme-hospital-is-on-the-house) logotype, and the source image for that was found [here](<http://www.kabukis.com/wp-content/uploads/2015/01/theme-hospital-759x500.jpg>). The [profile images](https://www.clipartmax.com/middle/m2i8K9H7K9A0A0Z5_doctor-and-nurse-cartoon-doctor-and-nurse) for the fake users in the database were found on [clipartmax.com](http://www.clipartmax.com). The required editing was made using [Gimp](https://www.gimp.org/). 

The list of diseases was extracted from [here](https://strategywiki.org/wiki/Theme_Hospital/Diseases). The price range was completely invented as this information was not available, neither was part of the [game](https://www.ea.com/news/theme-hospital-is-on-the-house). 

A total of 50 hospital names were automatically generated using a [fantasy name generator](https://www.fantasynamegenerators.com
https://www.fantasynamegenerators.com/hospital-names.php). The people names also were created [with the same tool](https://www.fantasynamegenerators.com/english_names.php), completing the source list with 25 male and 25 female names. The health insurance names were created by me, [based on the top health insurance companies of the US](https://health.usnews.com/health-news/health-insurance/articles/2013/12/16/top-health-insurance-companies). 

All textual data used to create and fill the database is available in lists, dictionaries or lists of tuples in the `data_source.py`.



### Design

As layout/design wasn't a requirement in this project, the design used in this application was heavily based on the templates provided in the [forked repository](https://github.com/udacity/OAuth2.0/tree/master/templates), in order to focus on the development of the actual CRUD application. 

As this wasn't a requirement for this project, the design is not responsive.



### Routes/Pages

The following routes/pages are currently available in this application:

#### List of all Hospitals

| Description                        | Type   | Routes                                                            |
| -----------------------------------|--------| ------------------------------------------------------------------|
| Home page, list all Hospitals      | READ   | /<br>/hospital<br>/hospitals                                      |
| Login                              |        | /login                                                            |
| Hospital Page, list all Conditions | READ   | /hospital/<int: hospital_id><br>/hospital/<int:hospital_id>/treatments/<br>/hospital/<int:hospital_id>/conditions/                            |
| Add a new Hospital                 | CREATE | /hospital/new                                                     |
| Edit a Hospital                    | UPDATE | /hospital/<int: hospital_id>/edit                                 |
| Delete a Hospital                  | DELETE | /hospital/<int: hospital_id>/delete                               |
| Add a new Condition for a Hospital | CREATE | /hospital/<int: hospital_id>/condition/new                        |
| Edit a Condition for a Hospital    | UPDATE | /hospital/<int: hospital_id>/condition/<int: condition_id>/edit   |
| Delete a Condition for a Hospital  | DELETE | /hospital/<int: hospital_id>/condition/<int: condition_id>/delete |



### API Endpoints

Three API endpoints were added in this project:

| Description                                              | Routes                                                       |
| -------------------------------------------------------- | ------------------------------------------------------------ |
| Get all Hospitals                                        | /hospital/JSON<br>/hospitals/JSON                            |
| Get all Conditions for a given Hospital                  | /hospital/<int: hospital_id>/JSON;<br/>/hospital/<int: hospital_id>/conditions/JSON;<br>/hospital/<int: hospital_id>/treatments/JSON                  |
| Get all data for one Condition in one Hospital | /hospital/<int: hospital_id>/condition/<int: condition_id>/JSON |



### Oauth2

I'm using both [Google](https://developers.google.com/identity/protocols/OAuth2) and [Facebook](https://developers.facebook.com/docs/facebook-login/) Oauth2 authentication and authorization services. 



### Disclaimer

This is just a learning project, not planned to be released. No copyright infringement intended.



### Known Bugs

Five bugs currently exist in this application.

1. The green bar showing flash messages is bigger on a hospital page than on the homepage. Couldn't figured why. Sorry!
2. Sometimes when re-running the `python fill_database.py` command, it will cause error. The log from the error is available [here](https://github.com/mguidoti/FSND-p4-item_catalog/blob/master/bug_report/sql_bug.txt). I think it's probably something that keeps the `*.db` open, and thus, can't write new information on it? It's definitely a sqlite issue, not my application's issue.
3. I'm not checking if there are any values what so ever when creating hospitals or conditions, neither if the input values are of a given type. This means that you can create something completely blank or totally nonsense (e.g., cost = chihuahua). But why would you do that to me?
4. Sometimes, for some reason that I simply couldn't figure out, trying to disconnect will fail. I think it has something to do with me messing around with the server, causing problems with the login_session. Or some sort of expiration time for the tokens. Not sure. Sorry! But if you don't stay logged forever neither mess around with the server, should be all right.
5. According to this [question on stack overflow](https://stackoverflow.com/questions/44520959/how-to-get-gender-and-birthday-information-of-a-google-sign-in-user-using-people), the access to the gender information on Google accounts might be private and therefore, inaccessible. In order to avoid potential problems with this, I simply set the gender of real users (e.g., you) to 'Who cares?'. Not a bug, just explaining I guess?
