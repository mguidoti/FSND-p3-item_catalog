"""
Data source used to populate the database.
"""

conditions = {
    'Broken wind': {
        'Cause': 'Using a gymnasium treadmill after a meal',
        'Sympton': 'Upsetting the people directly behind the patient',
        'Cure': 'A heavy mixture of special watery atoms is drunk '
                'rapidly in the Pharmacy',
        'Type': 'Pharmacy',
        'Cost_Min': 15.00,
        'Cost_Max': 25.00
    },

    'Chronic Nosehair': {
        'Cause': 'Sniffing disdainfully at those worse off than the'
                 'patient',
        'Sympton': 'Nosebeard a badger could make a nest in',
        'Cure': 'A disgusting hair-removal potion is'
                 'taken orally, prepared by a Nurse in the Pharmacy',
        'Type': 'Pharmacy',
        'Cost_Min': 35.00,
        'Cost_Max': 50.00
    },

    'Corrugated Ankles': {
        'Cause': 'Driving over traffic calming measures in road',
        'Sympton': 'Footwear does not fit snugly',
        'Cure': 'A slightly toxic blend of herbs and spices is drunk'
                'to straighten out the ankles',
        'Type': 'Pharmacy',
        'Cost_Min': 15.00,
        'Cost_Max': 20.00
    },

    'Discrete Itching': {
        'Cause': 'Tiny insects with sharp teeth',
        'Sympton': 'Scratching, leading to body-part inflammation',
        'Cure': 'Patient drinks a pharmaceutical gluey syrup to'
                'prevent the skin from itching',
        'Type': 'Pharmacy',
        'Cost_Min': 35.00,
        'Cost_Max': 60.00
    },

    'Gastric Ejections': {
        'Cause': 'Spicy Mexican or Indian food',
        'Sympton': 'Half-digested food is emitted from the patient in'
                   'random clusters',
        'Cure': 'Drinking a special binding solution prevents anything'
                'being ejected',
        'Type': 'Pharmacy',
        'Cost_Min': 50.00,
        'Cost_Max': 75.00
    },

    'Gut Rot': {
        'Cause': 'Mrs. O''Malley''s Good Time Whisky Cough Mixture',
        'Sympton': 'No cough but no stomach-wall lining either',
        'Cure': 'A Nurse can administer a selection of dissolved'
                'chemicals to coat the tum',
        'Type': 'Pharmacy',
        'Cost_Min': 35.00,
        'Cost_Max': 75.00
    },

    'Heaped Piles': {
        'Cause': 'Standing around by water coolers',
        'Sympton': 'Patient feels like he/she is sitting on a bag of'
                   'marbles',
        'Cure': 'A pleasant, yet powerfully acidic drink dissolves the'
                'piles from the inside',
        'Type': 'Pharmacy',
        'Cost_Min': 50.00,
        'Cost_Max': 85.00
    },

    'Invisibility': {
        'Cause': 'Being bitten by a radioactive (and invisible) ant',
        'Sympton': 'Patients suffer no discomfort. Indeed, many use'
                   'the condition to play practical jokes on their'
                   'families',
        'Cure': 'A colourful liquid drunk in the Pharmacy soon'
                'restores the patient to full observability',
        'Type': 'Pharmacy',
        'Cost_Min': 85.00,
        'Cost_Max': 125.00
    },

    'Sleeping Illness': {
        'Cause': 'Overactive sleep gland in the roof of the mouth',
        'Sympton': 'Overwhelming desire to crash out everywhere',
        'Cure': 'A high dosage of powerful stimulant is administered'
                'by a Nurse',
        'Type': 'Pharmacy',
        'Cost_Min': 40.00,
        'Cost_Max': 65.00
    },

    'The Squits': {
        'Cause': 'Eating pizza found under the cooker',
        'Sympton': 'Ugh. Surely you can guess',
        'Cure': 'A glutinous mix of stringy pharmaceutical chemicals'
                'solidify the patients innards',
        'Type': 'Pharmacy',
        'Cost_Min': 55.00,
        'Cost_Max': 70.00
    },

    'Transparency': {
        'Cause': 'Licking the yogurt from the foil tops of opened pots',
        'Sympton': 'Flesh is rendered see-through and horrible',
        'Cure': 'A Pharmacy drink of specially cooled and coloured'
                'water cures this disease',
        'Type': 'Pharmacy',
        'Cost_Min': 15.00,
        'Cost_Max': 45.00
    },

    'Uncommon Cold': {
        'Cause': 'Small particles of snot in the air',
        'Sympton': 'Runny nose, sneezing and discoloured lungs',
        'Cure': 'A big swig of uncommon cough medicine made from'
                'special ingredients in the Pharmacy will cure this',
        'Type': 'Pharmacy',
        'Cost_Min': 45.00,
        'Cost_Max': 65.00
    },

    '3rd Degree Sideburns': {
        'Cause': 'Wistful longing for the 1970''s',
        'Sympton': 'Big hair, flares, platforms and glitter make-up',
        'Cure': 'The Psychiatry staff must, using up-to-date'
                'techniques, convince the patient that these hairy'
                'accoutrements are rubbish',
        'Type': 'Psychiatric',
        'Cost_Min': 150.00,
        'Cost_Max': 175.00
    },

    'Fake Blood': {
        'Cause': 'Patient usually subject of practical joke',
        'Sympton': 'Red fluid in veins which evaporates on contact'
                   'with clothing',
        'Cure': 'Psychiatric calming is the only way to deal with this'
                'problem',
        'Type': 'Psychiatric',
        'Cost_Min': 215.00,
        'Cost_Max': 250.00
    },

    'Infectious Laughter': {
        'Cause': 'Classic situation comedy',
        'Sympton': 'Helpless chortling and repetition of unfunny'
                   'catchphrases',
        'Cure': 'A qualified Psychiatrist must remind the patient how'
                'serious this condition is',
        'Type': 'Psychiatric',
        'Cost_Min': 150.00,
        'Cost_Max': 225.00
    },

    'King Complex': {
        'Cause': 'The spirit of the King entering the patient''s'
                 'mind and taking over',
        'Sympton': 'Donning of colourful suede footwear and eating'
                   'cheeseburgers',
        'Cure': 'A Psychiatrist tells the patient how ridiculous he or'
                'she looks',
        'Type': 'Psychiatric',
        'Cost_Min': 125.00,
        'Cost_Max': 250.00
    },

    'Sweaty Palms': {
        'Cause': 'Fear of job interviews',
        'Sympton': 'Handshakes with patient are like grabbing a'
                   'recently submerged sponge',
        'Cure': 'A Psychiatrist must talk the patient out of this'
                'made-up disease',
        'Type': 'Psychiatric',
        'Cost_Min': 145.00,
        'Cost_Max': 185.00
    },

    'TV Personalities': {
        'Cause': 'Daytime television',
        'Sympton': 'Delusions of being able to present a cookery show',
        'Cure': 'A trained Psychiatrist must convince the patient to'
                'sell their TV and buy a radio',
        'Type': 'Psychiatric',
        'Cost_Min': 150.00,
        'Cost_Max': 350.00
    },

    'Alien DNA': {
        'Cause': 'Face huggers equipped with intelligent alien blood',
        'Sympton': 'Gradual alien metamorphosis and desire to destroy'
                   'our cities',
        'Cure': 'The DNA is mechanically removed, cleaned of alien'
                'elements and replaced quickly',
        'Type': 'Clinics',
        'Cost_Min': 250.00,
        'Cost_Max': 300.00
    },

    'Baldness': {
        'Cause': 'Telling lies and making up stories to be popular',
        'Sympton': 'Shiny-headedness and embarrassment',
        'Cure': 'Hair is seamlessly melded onto the patient''s head'
                'using a painful machine',
        'Type': 'Clinics',
        'Cost_Min': 150.00,
        'Cost_Max': 250.00
    },

    'Bloaty Head': {
        'Cause': 'Sniffing cheese and drinking unpurified rainwater',
        'Sympton': 'Very uncomfortable for the sufferer',
        'Cure': 'The swollen head is popped, then reinflated to the'
                'correct PSI using a clever machine',
        'Type': 'Clinics',
        'Cost_Min': 85.00,
        'Cost_Max': 150.00
    },

    'Fractured Bones': {
        'Cause': 'Falling off high things onto concrete',
        'Sympton': 'Loud crack and inability to use afflicted limbs',
        'Cure': 'The cast is set then removed using a laser-driven'
                'removing machine',
        'Type': 'Clinics',
        'Cost_Min': 75.00,
        'Cost_Max': 100.00
    },

    'Hairyitis': {
        'Cause': 'Prolonged exposure to the moon',
        'Sympton': 'Sufferers experience enhanced sense of smell',
        'Cure': 'An electrolysis machine removes the hair and seals up'
                'the pores',
        'Type': 'Clinics',
        'Cost_Min': 150.00,
        'Cost_Max': 200.00
    },

    'Jellyitis': {
        'Cause': 'Gelatin-rich diet and too much exercise',
        'Sympton': 'Excessive wobbliness and falling down a lot',
        'Cure': 'The patient is immersed in the Jelly Vat in a special'
                'room for a bit',
        'Type': 'Clinics',
        'Cost_Min': 150.00,
        'Cost_Max': 215.00
    },

    'Serious Radiation': {
        'Cause': 'Mistaking plutonium isotopes for chewing gum',
        'Sympton': 'Patients with this condition feel very, very'
                   'unwell',
        'Cure': 'The patient must be placed in a Decontamination'
                'Shower and cleansed properly',
        'Type': 'Clinics',
        'Cost_Min': 350.00,
        'Cost_Max': 425.00
    },

    'Slack Tongue': {
        'Cause': 'Chronic overdiscussion of soap operas',
        'Sympton': 'Tongue swells to five times its original length',
        'Cure': 'The tongue is placed in the Slicer Machine, and'
                'removed quickly, efficiently and painfully',
        'Type': 'Clinics',
        'Cost_Min': 125.00,
        'Cost_Max': 175.00
    },

    'Broken Heart': {
        'Cause': 'Someone richer, younger and thinner than the patient',
        'Sympton': 'Weeping and RSI caused by hours of tearing up'
                   'holiday photos',
        'Cure': 'Two Surgeons open the chest and gently mend the heart'
                'whilst holding their breath',
        'Type': 'Surgical',
        'Cost_Min': 1500.00,
        'Cost_Max': 2500.00
    },

    'Golf Stones': {
        'Cause': 'Exposure to poison gas inside golf-balls',
        'Sympton': 'Delirium and advanced shame',
        'Cure': 'These must be removed by an operation requiring two'
                'Surgeons',
        'Type': 'Surgical',
        'Cost_Min': 800.00,
        'Cost_Max': 1125.00
    },

    'Iron Lungs': {
        'Cause': 'Inner-city smog mixed with kebab remains',
        'Sympton': 'Ability to breathe fire and shout loudly'
                   'underwater',
        'Cure': 'Two Surgeons operate to remove the cast solid lungs'
                'in the Theatre',
        'Type': 'Surgical',
        'Cost_Min': 1750.00,
        'Cost_Max': 2250.00
    },

    'Kidney Beans': {
        'Cause': 'Crunching up ice cubes in drinks',
        'Sympton': 'Pain and frequent trips to the toilet',
        'Cure': 'Two Surgeons must remove the beans without touching'
                'the sides of the kidney',
        'Type': 'Surgical',
        'Cost_Min': 1500.00,
        'Cost_Max': 2000.00
    },

    'Ruptured Nodules': {
        'Cause': 'Bungee jumping in cold weather',
        'Sympton': 'Inability to sit down in comfort',
        'Cure': 'Two qualified Surgeons must remove the nodules using'
                'steady hands',
        'Type': 'Surgical',
        'Cost_Min': 1250.00,
        'Cost_Max': 1750.00
    },

    'Spare Ribs': {
        'Cause': 'Sitting on cold stone floors',
        'Sympton': 'Unpleasant feeling of chestiness',
        'Cure': 'These must be taken out by two Surgeons, and given to'
                'the patient in a doggy bag',
        'Type': 'Surgical',
        'Cost_Min': 3500.00,
        'Cost_Max': 4000.00
    },

    'Unexpected Swelling': {
        'Cause': 'Anything unexpected',
        'Sympton': 'Swelling',
        'Cure': 'The swelling can only be reduced by lancing during an'
                'operation requiring two Surgeons',
        'Type':
        'Surgical',
        'Cost_Min': 1500.00,
        'Cost_Max': 3500.00
    }
}

hospital_names = [
    'Green Country Community Hospital',
    'Overlook Clinic'
    'Spring River Medical Clinic',
    'Wildflower Medical Center',
    'Crossroads Medical Center',
    'Maple Valley General Hospital',
    'Grand View Clinic',
    'Swan River Medical Center',
    'Silver Pine Hospital Center',
    'Diamond Grove Hospital',
    'Grand Valley General Hospital',
    'Horizon Hospital',
    'Grand Willow Medical Clinic',
    'Hope Haven Medical Center',
    'Union Clinic',
    'Lilypad Hospital',
    'Great River Hospital',
    'Paradise Valley Hospital Center',
    'Silver Oak Medical Clinic',
    'Marine General Hospital',
    'Flowerhill Hospital Center',
    'Rose Gardens Clinic',
    'Big Heart Clinic',
    'Forest View Medical Center',
    'Bellevue Hospital',
    'Hillsdale Medical Center',
    'Clearview Medical Center',
    'Hopevale Clinic',
    'Grand Garden Clinic',
    'White Willow Medical Clinic',
    'Hyacinth Community Hospital',
    'Greengrass Medical Center',
    'Stillwater General Hospital',
    'Summer Springs Community Hospital',
    'Union Health Clinic',
    'Fairview General Hospital',
    'New Horizons Hospital',
    'Summerstone Medical Clinic',
    'Cherry Blossom Hospital Center',
    'Grand Meadow Clinic',
    'White Blossom Community Hospital',
    'Silver Birch Hospital',
    'Silver Boulder Clinic',
    'Silver Wing Medical Center',
    'Tulip Community Hospital',
    'Petunia Community Hospital',
    'Grand University Community Hospital',
    'White River General Hospital',
    'Silverstone Hospital Center',
    'Silverspring Hospital Center',
    'Ruby Valley Clinic'
]

people_names = [
    ('Naomi Bell', 'F'),
    ('Rebecca West', 'F'),
    ('Sophia Hopkins', 'F'),
    ('Charlotte Mitchell', 'F'),
    ('Esme Wood', 'F'),
    ('Perla Dillon', 'F'),
    ('Jessie Hewitt', 'F'),
    ('Eliana Martin', 'F'),
    ('Yesenia Spears', 'F'),
    ('Chloe Thornton', 'F'),
    ('Julia Butler', 'F'),
    ('Sara Cole', 'F'),
    ('Alicia Brooks', 'F'),
    ('Bella Lawson', 'F'),
    ('Zoe Palmer', 'F'),
    ('Lorelai Woods', 'F'),
    ('Sharon Carter', 'F'),
    ('Aliyah White', 'F'),
    ('Gabriella Jackson', 'F'),
    ('Layla Williams', 'F'),
    ('Azalea Collier', 'F'),
    ('Eleanor Hawkins', 'F'),
    ('Heidi Mason', 'F'),
    ('Nicole Wallace', 'F'),
    ('Demi Martin', 'F'),
    ('Joel Reynolds', 'M'),
    ('Edward Smith', 'M'),
    ('Callum James', 'M'),
    ('Isaac Parry', 'M'),
    ('Jay Lawrence', 'M'),
    ('Beckett Long', 'M'),
    ('Deacon Paul', 'M'),
    ('Remy Beach', 'M'),
    ('Thiago Patel', 'M'),
    ('Reagan Tanner', 'M'),
    ('Ewan Chapman', 'M'),
    ('Jayden Morris', 'M'),
    ('Oscar Lewis', 'M'),
    ('Ollie Hughes', 'M'),
    ('Brandon Rees', 'M'),
    ('Samuel Galloway', 'M'),
    ('Raylan Lynn', 'M'),
    ('Milo Daugherty', 'M'),
    ('Konner Moody', 'M'),
    ('Deandre Dickerson', 'M'),
    ('Harrison Brown', 'M'),
    ('Cameron Ellis', 'M'),
    ('Arthur Hudson', 'M'),
    ('Rhys Gill', 'M'),
    ('Edward Walsh', 'M')
]

health_insurance_co_names = [
    "UnitedCare Group",
    "Bhrama Foundation Group",
    "Nicepoint Inc. Group",
    "Athena Group",
    "Animalia Group",
    "HPCP Group",
    "Cigana Health Group",
    "Lowmark Group",
    "Red Shield of California Group",
    "Independence Red Cross Group",
]
