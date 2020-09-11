import time
import argparse
from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER1
from pyfingerprint.pyfingerprint import FINGERPRINT_CHARBUFFER2

def enroll():
    f = PyFingerprint('COM6', 57600, 0xFFFFFFFF, 0x00000000)

    print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

    print('Waiting for finger...')

    while ( f.readImage() == False ):
        pass

    f.convertImage(FINGERPRINT_CHARBUFFER1)

    result = f.searchTemplate()
    positionNumber = result[0]

    if ( positionNumber >= 0 ):
        print('Template already exists at position #' + str(positionNumber))
        exit(0)

    print('Remove finger...')
    time.sleep(2)

    print('Waiting for same finger again...')

    while ( f.readImage() == False ):
        pass

    f.convertImage(FINGERPRINT_CHARBUFFER2)

    if ( f.compareCharacteristics() == 0 ):
        raise Exception('Fingers do not match')

    print("Nhập thông tin:")
    StudenID = input("StudentID: ")
    Name = input("Name: ")
    Class = input("Class: ")
    School = input("School: ")
    Faculty = input("Faculty: ")
    Room = input("Room: ")
    Phone = input("Phone: ")
    Email = input("Email: ")

    f.createTemplate()

    file = open('profiles/' + str(positionNumber) + '.txt', 'w', encoding='UTF8')
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

    positionNumber = f.storeTemplate()
    print('Finger enrolled successfully!')
    print('New template position #' + str(positionNumber))

def search():
    f = PyFingerprint('COM6', 57600, 0xFFFFFFFF, 0x00000000)

    print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

    print('Waiting for finger...')

    while ( f.readImage() == False ):
        pass

    f.convertImage(FINGERPRINT_CHARBUFFER1)
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

def check():
    f = PyFingerprint('COM6', 57600, 0xFFFFFFFF, 0x00000000)

    print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

    page = input('Please enter the index page (0, 1, 2, 3) you want to see: ')
    page = int(page)

    tableIndex = f.getTemplateIndex(page)

    for i in range(0, len(tableIndex)):
        print('Template at position #' + str(i) + ' is used: ' + str(tableIndex[i]))

def delete():
    f = PyFingerprint('COM6', 57600, 0xFFFFFFFF, 0x00000000)

    print('Currently used templates: ' + str(f.getTemplateCount()) +'/'+ str(f.getStorageCapacity()))

    positionNumber = input('Please enter the template position you want to delete: ')
    positionNumber = int(positionNumber)

    if ( f.deleteTemplate(positionNumber) == True ):
        print('Template deleted!')

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--method", required = True,
        help = "path to input method: 0 - Check , 1 - Enroll , 2 - Search , 3 - Delete")
    args = vars(ap.parse_args())

    if(args["method"] == "0"):
        check()
    if(args["method"] == "1"):
        enroll()
    elif(args["method"] == "2"):
        search()
    if(args["method"] == "3"):
          delete()
    else:
        print("""
            path to input method:
            \n0: Check  - Shows the template index table\n1: Enroll - Enrolls new finger\n2: Search - Search for a finger\n3: Delete - Deletes a finger from sensor")



if __name__ == "__main__":
    try:
        main()
    except:
        raise