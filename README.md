# Data Pre-processing with Python
A python script to pre-process large amount of system data generated on linux server to detect whether the system was attacked or not. 

Introduction

Description of Australian Defence Force Academy-Linux Dataset (ADFA-LD) :
1. The dataset was generated on Linux local server running on Ubuntu 11.04, oﬀering a variety of functions such as ﬁle sharing, database, remote access and web server.
2. Six types of attacks occur in ADFA-LD including two brute force password guessing attempts on the open ports enabled by FTP and SSH respectively, an unauthorised attempt to create a new user with root privileges through encoding a malicious payload into a normal executable, the uploads of Java and Linux executable Meterpreter payloads for the remote compromise of a target host, and the compromise and privilege escalation using C100 webshell. These types are termed as Hydra-FTP, Hydra-SSH, Adduser, Java-Meterpreter, Meterpreter and Webshell respectively.
3. 833 and 4373 normal traces are generated for training and validation respectively, over a period during which no attacks occur against the host and legitimate application activities ranging from web browsing to document writing are operated as usual.

Task Steps
Following steps have been performed to do the task :
1. We split the Attack data for each category into 70% training data and 30% test data. For that, ﬁrst 7 folders have been used for training data and last 3 for test data. For Normal data , ﬁles in ”Training Data Master” folder have been used for training data and ﬁles in ”Validation Data Master” have been used as test data.
2. For each type of attack. the python script ﬁrst combines all the training data ﬁles into one list, then the frequency all the unique n-grams have been found for them as well as for Normal training data ﬁles. Concatenating entire training ﬁle for a particular class of attack and then running the script on the concatenated ﬁle instead of running it individually on each ﬁle saves time.
3. For ﬁnding n-grams , a list of all possible values of n is maintained. For general case, we have included only one element i.e. n = 3, the list can be extending just by adding other elements like 5 or 7. And the same program will work because the whole process iterates over all elements of n.
2
4. For calculating the frequencies of all n-grams, the ngrams freq function ﬁrst takes three consecutive elements of the list (of concatenated training data ﬁles) and makes it a string. In this was, the whole list is iterated and such strings are compared to get the frequency of ngrams.The function returns a dictionary of n-grams frequencies. This also saves our time comparing 3 elements individually.Similarly, the script ﬁnds the unique n-grams frequency for Normal ﬁles.
5. For all the category of attacks and the Normal, top 30% most frequent n-grams are selected. For that, the whole n-gram frequency dictionary is sorted and then top 30% have been picked. These n-grams are used as the features to create the dataset.
6. Now, the training dataset is created. File train.csv is created. The frequencies of n-grams which are in features list are found from each and every ﬁles which are in training data individually. A row is added in the train.csv ﬁle corresponding to each ﬁle. Corresponding label has been added for each data.
7. Now, for creating the test dataset, ﬁrst test.csv ﬁle is created in similar way.And same thing is done on each of the ﬁles individually. And one row is added for each ﬁle processed.
