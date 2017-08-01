import zipfile
import os
import sys
import shutil
import re

print("\ntest_checker.py is now running\n")
# print("arguments are : ", sys.argv)

try:
    # if not sys.argv[1]:
    #     print('You did not enter the target test name')
    #
    # if not sys.argv[2]:
    #     print('You did not enter the target zip file name')
    #
    # if not sys.argv[3]:
    #     print('You did not enter the target output file name')

    if not sys.argv[1] or not sys.argv[2]:
        print("Missing arguments, exiting now")
        quit()

except IndexError:
    print("Missing arguments, exiting now")
    quit()

print('Target test name: ', sys.argv[1])
print('Target archive name: ', sys.argv[2])

try:
    output_file = sys.argv[3]
except IndexError:
    print("Output file not specified, defaulting to output.txt");
    output_file = "output.txt"

print('Target output file name: ', output_file)

if os.path.isdir("archive") == True:
    shutil.rmtree("archive")
    print('Deleting old folder and extracting again into the folder')

if not os.path.isfile(sys.argv[2]):
    print("File", sys.argv[2] , " does not exist")
    quit()

try:
    zip_ref = zipfile.ZipFile(sys.argv[2], "r");
    zip_ref.extractall("archive");
    zip_ref.close();
except zipfile.BadZipFile:
    print("File", sys.argv[2], " is not a zip file, exiting now!")
    quit()

if sys.argv[1] == "check_all":
    sys.argv[1] = '[A-Za-z0-9]+'

#Regex for locating test names in the files
test_name = 'test_'+ sys.argv[1] + '_[A-Za-z0-9]*'
#test_name = 'test_'+ sys.argv[1] + '_.*'
#test_python_[A-Za-z0-9]*

print('Regex for test: ', test_name)

tests = {}

#Goes through all the files extracted from the archive/zip file and goes through their contents to see if there are any matches for the regex
with open(output_file, "w") as a:
    for path, subdirs, files in os.walk(os.path.abspath('archive')):
        for filename in files:
            #print("Path: ", path)
            #print("Filename: ", filename)
            f = os.path.join(path, filename)

            #Going through the lines of each file to look for matches
            testo = open(f, "r")
            try:
                for inner_line in testo:
                    if  re.search(test_name, inner_line.lower()):

                        start = re.search(test_name, inner_line.lower()).start()
                        end = re.search(test_name, inner_line.lower()).end()

                        # print("printing re.search ", test_name, inner_line.lower(), " is ", re.search(test_name, inner_line.lower()).span())
                        # print(str(inner_line)[start:end])
                        extracted_test_name = str(inner_line)[start:end]

                        #Checks to see if the testname is already in the dictionary/hashmap
                        if not extracted_test_name in tests:
                            # print("Adding ", extracted_test_name , " to the hashmap\n");
                            tests[extracted_test_name] = 1

            except UnicodeDecodeError:
                print("UnicodeDecodeError! Ignoring line!")

            testo.close()

    # print("Contents of hashmap/dictionary is: \n")
    for hash_test_names in tests:
        # print(hash_test_names)
        a.write(hash_test_names + "\n")

print("\ntest_checker.py has finished running\n")





