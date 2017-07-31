import glob
import math
from collections import Counter
import csv


# returns a dictionary of n-grams frequency for any list
def ngrams_freq(listname, n):
    counts = dict()
    # make n-grams as string iteratively
    grams = [' '.join(listname[i:i+n]) for i in range(len(listname)-n)]
    for gram in grams:
        if gram not in counts:
            counts[gram] = 1
        else:
            counts[gram] += 1
    return counts


# returns the values of features for any list
def feature_freq(listname,n,features):
	counts = dict()
	# make n-grams as string iteratively
	grams = [' '.join(listname[i:i+n]) for i in range(len(listname)-n)]
	for gram in grams:
		counts[gram] = 0
	for gram in grams:
		if gram in features:
			counts[gram] += 1
	return counts


# values of n for finding n-grams
n_values = [3, 5, 7]

# Base address for attack data files
add = "ADFA-LD/ADFA-LD/Attack_Data_Master/"
# list of attacks
attack = ['Adduser','Hydra_FTP','Hydra_SSH','Java_Meterpreter','Meterpreter','Web_Shell']

# initializing dictionary for n-grams from all files
traindict = {}


print("Generating Training Data ..................................")
for term in attack:
	print("	Training data from " + term)
	globals()['%s_list' % term] = []
	in_address = add+term
	k = 1
	# finding list of data from all files
	for i in range (1,8):
		read_files = glob.glob(in_address+"_"+str(i)+"/*.txt")
		for f in read_files:
			with open(f, "r") as infile:
				globals()['%s_list_array' % term+str(k)] = infile.read().split()
				globals()['%s_list' % term].extend(globals()['%s_list_array' % term+str(k)])
				k += 1
	# number of lists for distinct files
	globals()['%s_size' % term] = k-1
	# combined list of all files
	listname = globals()['%s_list' % term]
	# finding n-grams and extracting top 30%
	for n in n_values:
		print("		Extracting top 30% "+str(n)+"-grams from "+term+".......................")
		dictname = ngrams_freq(listname,n)
		top = math.ceil(0.3*len(dictname))
		dictname = Counter(dictname)
		for k, v in dictname.most_common(top):
			traindict.update({k : v})

# finding training data for Normal file
print("	Training data from Normal")
Normal_list = []
in_address = "ADFA-LD/ADFA-LD/Training_Data_Master/"
k = 1
read_files = glob.glob(in_address+"/*.txt")
for f in read_files:
	with open(f, "r") as infile:
		globals()['Normal%s_list_array' % str(k)] = infile.read().split()
		Normal_list.extend(globals()['Normal%s_list_array' % str(k)])
		k += 1

# number of lists for distinct files
Normal_list_size = k-1
# combined list of all files
listname = Normal_list
# finding n-grams and extracting top 30%
for n in n_values:
	print("		Extracting top 30% "+str(n)+"-grams from Normal........................")
	dictname = ngrams_freq(listname,n)
	top = math.ceil(0.3*len(dictname))
	dictname = Counter(dictname)
	for k, v in dictname.most_common(top):
		traindict.update({k : v})


# Creating feature list
features = []
features.append('Label')
for k,v in traindict.items():
	features.append(k)
print("\n			Features created by taking top 30% frequent n-grams for all types..........\n")


# Writing training data to file
print("\nWriting Training data in training file..................................\n")
with open('train.csv','w') as csvfile:
	# writing features as header 
	writer = csv.DictWriter(csvfile, fieldnames = features, extrasaction='ignore')
	writer.writeheader();

	# Calculating values of each feature for each file
	for term in attack:
		print("	Writing for "+term)
		for k in range (1,globals()['%s_size' % term]+1):
			listname = globals()['%s_list_array' % term+str(k)]
			feature_count = {}
			for n in n_values:
				print("		Calculating "+str(n)+"-gram feature frequency for files in "+term)
				feature_count.update(feature_freq(listname,n,features))
			feature_count.update({'Label' : term})
			for f in features:
				if f not in feature_count:
					feature_count.update({f : 0})
			writer.writerow(feature_count)

	# Calculating values of each feature for each file
	print("	Writing for Normal")
	for k in range (1,Normal_list_size+1):
		listname = globals()['Normal%s_list_array' % str(k)]
		feature_count = {}
		for n in n_values:
			print("		Calculating "+str(n)+"-gram feature frequency for files in Normal")
			feature_count.update(feature_freq(listname,n,features))
		feature_count.update({'Label' : 'Normal'})
		for f in features:
			if f not in feature_count:
				feature_count.update({f : 0})
		writer.writerow(feature_count)

print("\ntrain.csv created..............................................\n")
	

print("Generating Test Data ..................................")
for term in attack:
	print("	Test data from " + term)
	globals()['%s_test_list' % term] = []
	in_address = add+term
	k = 1
	# finding list of data from all files
	for i in range (8,11):
		read_files = glob.glob(in_address+"_"+str(i)+"/*.txt")
		for f in read_files:
			with open(f, "r") as infile:
				globals()['%s_test_list_array' % term+str(k)] = infile.read().split()
				globals()['%s_test_list' % term].extend(globals()['%s_test_list_array' % term+str(k)])
				k += 1
	# number of lists for distinct files
	globals()['%s_test_size' % term] = k-1
	
	
print("	Test data from Normal")
Normal_test_list = []
in_address = "ADFA-LD/ADFA-LD/Validation_Data_Master/"
k = 1
read_files = glob.glob(in_address+"/*.txt")
# finding list of data from all files
for f in read_files:
	with open(f, "r") as infile:
		globals()['Normal%s_test_list_array' % str(k)] = infile.read().split()
		Normal_test_list.extend(globals()['Normal%s_test_list_array' % str(k)])
		k += 1
# number of lists for distinct files
Normal_test_list_size = k-1



# Writing test data to file
print("\nWriting Test data in test file..................................\n")
with open('test.csv','w') as csvfile:
	features.remove('Label')
	writer = csv.DictWriter(csvfile, fieldnames = features, extrasaction='ignore')
	writer.writeheader();

	# Calculating values of each feature for each file
	for term in attack:
		print("	Writing for "+term)
		for k in range (1,globals()['%s_test_size' % term]+1):
			listname = globals()['%s_test_list_array' % term+str(k)]
			feature_count = {}
			for n in n_values:
				print("		Calculating "+str(n)+"-gram feature frequency for files in "+term)
				feature_count.update(feature_freq(listname,n,features))
			for f in features:
				if f not in feature_count:
					feature_count.update({f : 0})
			writer.writerow(feature_count)

	# Calculating values of each feature for each file
	print("	Writing for Normal")
	for k in range (1,Normal_test_list_size+1):
		listname = globals()['Normal%s_test_list_array' % str(k)]
		feature_count = {}
		for n in n_values:
			print("		Calculating "+str(n)+"-gram feature frequency for files in Normal")
			feature_count.update(feature_freq(listname,n,features))
		for f in features:
			if f not in feature_count:
				feature_count.update({f : 0})
		writer.writerow(feature_count)

print("\ntest.csv created..............................................\n")

print("Done")




