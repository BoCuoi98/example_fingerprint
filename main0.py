import time
import hashlib
import argparse
from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER2

## Enrolls new finger
##

def enroll():
    ## Tries to initialize the sensor
    f = PyFingerprint('COM6', 57600, 0xFFFFFFFF, 0x00000000)

    ## Gets some sensor information
    print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

    print('Waiting for finger...')

    ## Wait that finger is read
    while ( f.readImage() == False ):
        pass

    ## Converts read image to characteristics and stores it in charbuffer 1
    f.convertImage(FINGERPRINT_CHARBUFFER1)

    ## Checks if finger is already enrolled
    result = f.searchTemplate()
    positionNumber = result[0]

    if ( positionNumber >= 0 ):
        print('Template already exists at position #' + str(positionNumber))
        exit(0)

    print('Remove finger...')
    time.sleep(2)

    print('Waiting for same finger again...')

    ## Wait that finger is read again
    while ( f.readImage() == False ):
        pass

    ## Converts read image to characteristics and stores it in charbuffer 2
    f.convertImage(FINGERPRINT_CHARBUFFER2)

    ## Compares the charbuffers
    if ( f.compareCharacteristics() == 0 ):
        raise Exception('Fingers do not match')

    ## 
    print("Nhập thông tin:")
    StudenID = input("StudentID: ")
    Name = input("Name: ")
    Class = input("Class: ")
    School = input("School: ")
    Faculty = input("Faculty: ")
    Room = input("Room: ")
    Phone = input("Phone: ")
    Email = input("Email: ")

    file = open('profiles/2.txt', 'w', encoding='UTF8')
    file.writelines(
        "StudentID: " + StudenID +
        "\nName: " + Name +
        "\nClass: " + Class +
        "\nSchool: " + School +
        "\nFaculty: " + Faculty +
        "\nRoom: " + Room +
        "\nPhone: " + Phone +
        "\nEmail: " + Email
    )
    file.close()

    ## Creates a template
    f.createTemplate()

    ## Saves template at new position number
    positionNumber = f.storeTemplate()
    print('Finger enrolled successfully!')
    print('New template position #' + str(positionNumber))

def search():
    ## Tries to initialize the sensor
    f = PyFingerprint('COM6', 57600, 0xFFFFFFFF, 0x00000000)

    ## Gets some sensor information
    print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

    ## Tries to search the finger and calculate hash
    print('Waiting for finger...')

    ## Wait that finger is read
    while ( f.readImage() == False ):
        pass

    ## Converts read image to characteristics and stores it in charbuffer 1
    f.convertImage(FINGERPRINT_CHARBUFFER1)

    ## Searchs template
    result = f.searchTemplate()

    positionNumber = result[0]
    accuracyScore = result[1]

    if ( positionNumber == -1 ):
        print('No match found!')
        exit(0)
    else:
        print('Found template at position #' + str(positionNumber))
        print('The accuracy score is: ' + str(accuracyScore))

        f = open('profiles/' + str(positionNumber) + '.txt', 'r', encoding='UTF8')
        for line in f:
            print(line, end='')
        f.close()




# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--method", required = True,
    help = "path to input method: enroll or search")
args = vars(ap.parse_args())

# check the method to be executed with the image: create or search
if(args["method"] == "enroll"):
    enroll()

elif(args["method"] == "search"):
    search()
            
else:
    print("method does not match: enroll or search")