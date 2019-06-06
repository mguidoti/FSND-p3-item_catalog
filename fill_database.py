"""
Fills the database radomly.

Can be re-used until all hospitals and people's names have been used.
"""

from __future__ import division
import random

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from initiate_database import Base, User, Hospital, Condition
import data_source as source


# Initiates an engine for the databases
engine = create_engine('sqlite:///themehospitals.db')

# Bind the engine to the metadata of the Base class to access the
# declaratives in a DBSession instance
Base.metadata.create_all(engine)

# Start the stage for all acts and conversations with the referred database
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Pick a random even number from 8 to 12 to be the number of hospitals
number_of_hospitals = random.randrange(8, 12, 2)

# Create counters to keep gender equity
number_of_males = 0
number_of_females = 0

# Status counter to be printed at the end
user_counter = 0

# Create users considering gender equity
while (number_of_males + number_of_females) < number_of_hospitals:

    # Pick a random person from the source, saving name and gender
    choice = random.choice(list(source.people_names))
    user_name = choice[0]
    gender = choice[1]

    users_in_db = session.query(User).all()

    if len(users_in_db) < len(source.people_names):

        # Check if the randomly picked person already exists in the
        # database. If it's the case, it will count as one more added
        # users without adding it to enforce hospital ownership
        # repetition.
        try:
            user = session.query(User).filter_by(name=user_name).one()
            if gender == 'F':
                number_of_females += 1
            else:
                number_of_males += 1
            # If the user already exists, don't create a second entry
            continue

        except:
            # Set dummy e-mail and the "most likely to be right"
            # profile picture
            email = str(user_name) + '@udacityfake.com'

            if gender == 'F':
                picture = '/static/clipart67092-female_doc.png'
                number_of_females += 1
            else:
                picture = '/static/clipart67092-male_doc.png'
                number_of_males += 1

            # Adds new user
            new_user = User(name=user_name, email=email,
                            gender=gender, type='fake',
                            picture=picture)

            session.add(new_user)
            session.commit()

            user_counter += 1

    else:
        print("All users in the source database already added.")
        break


# Add all users and their IDs into a dictionary for easier access
added_users = session.query(User).filter_by(type='fake').all()
dict_of_added_users = {}

for each_user in added_users:
    dict_of_added_users.update({each_user.name: each_user.id})


# Create hospitals avoiding repetition of names

# Create an empty list to hold the added hospitals for easier access
hospitals = []

while len(hospitals) < number_of_hospitals:

    # First, get all already added hospitals, which might be > 0 - in
    # case of re-running the script
    hospitals_added = session.query(Hospital).all()

    # Base case to avoid the while loop quicker if all 50 names in the
    # source were already added
    if len(hospitals_added) < 50:

        # Pick a random name
        hospital_name = random.choice(source.hospital_names)

        # Check if it's already added or not
        try:
            hospital = session.query(Hospital).filter_by(
                       name=hospital_name).one()
            continue
        except:

            # Create a random number as the number of insurance
            # companies for a given hospital and creates the string
            # that will be composed with insurance company names
            insurance_range = random.randint(0, 6)
            accepted_insurance = ''

            # Compose to the accepted_insurance string
            while insurance_range > 0:
                if accepted_insurance == '':
                    accepted_insurance += random.choice(
                        source.health_insurance_co_names)
                    insurance_range -= 1
                else:
                    accepted_insurance += ', ' + random.choice(
                        source.health_insurance_co_names)
                    insurance_range -= 1

            # Pick a random user from the dict_of_added_users
            user_name = random.choice(list(dict_of_added_users))
            user_id = dict_of_added_users[user_name]

            # Add new hospital
            new_hospital = Hospital(name=hospital_name,
                                    accepted_insurance=accepted_insurance,
                                    address="302 Doesn't Exist St., Not"
                                            "Even Bother, 99999",
                                    phone='900DONTCALL',
                                    user_id=user_id)

            session.add(new_hospital)
            session.commit()

            # Add the new hospital to the list of hospitals for easier
            # access
            hospitals += [hospital_name]

    else:
        print("All hospitals in the source database already added.")
        break

# Add all hospitals and their user_IDs into a dictionary for easy access
allHospitals = session.query(Hospital).all()
arrayOfHospitals = {}

for each in allHospitals:
    arrayOfHospitals.update({each.name: each.user_id})


# Add a random number of conditions to each added hospital in this
# session
# Status counter to be printed at the end
totalOfConditions = 0

for hospital_name in hospitals:
    hospital = session.query(Hospital).filter_by(
                name=hospital_name).one()

    conditionRange = random.randint(10, 15)

    # Check if the given hospital already have any condition included
    addedConditions = session.query(Condition).filter_by(
                        hospital_id=hospital.id).all()

    if len(addedConditions) == 0:

        while conditionRange > 0:
            condition_name = random.choice(list(source.conditions))

            # Check if the randomly picked condition already exists
            # for the given hospital, to avoid duplicates
            condition_exists = session.query(Condition).filter_by(
                                hospital_id=hospital.id,
                                name=condition_name).all()

            if len(condition_exists) == 0:

                # Calculate a random price with floating number and two
                # decimals.
                cost_min = source.conditions[condition_name]['Cost_Min']
                cost_max = source.conditions[condition_name]['Cost_Max']
                cost = round(random.uniform(cost_min, cost_max), 2)

                newCondition = Condition(name=condition_name,
                                         cause=source.conditions
                                         [condition_name]
                                         ['Cause'],
                                         sympton=source.conditions
                                         [condition_name]
                                         ['Sympton'],
                                         cure=source.conditions
                                         [condition_name]
                                         ['Cure'],
                                         type=source.conditions
                                         [condition_name]
                                         ['Type'],
                                         cost=cost,
                                         hospital_id=hospital.id,
                                         user_id=hospital.user_id)

                session.add(newCondition)
                session.commit()

                totalOfConditions += 1
                conditionRange -= 1

            else:
                continue


# Print status message reporting number of users, hospitals and the
# average number of conditions added to the database
if len(hospitals) == 0:
    print("A total of %s users were succesfully created!" %
          (str(user_counter)))
else:
    average_of_added_conditions = totalOfConditions/(len(hospitals))
    print("A total of %s users, %s hospitals, with an average of %s "
          "conditions were succesfully "
          "created!" % (str(user_counter), str(len(hospitals)),
                        average_of_added_conditions))
