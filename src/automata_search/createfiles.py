import utils

print("creating 1MB file")
utils.generate_test_file("small_text.txt",1)

print ("creating 10MB file")
utils.generate_test_file("large_text.txt",10)

print("done creating files")