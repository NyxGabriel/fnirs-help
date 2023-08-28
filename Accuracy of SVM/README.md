#  About 
 This code checks the accuracy of the MCPA analysis done with an SVM trained in TurboSatori. 
The only way that works is if you have copied it exactly! (last line included the output the SVM training from turbosatori) and given it *_4Script.txt* file ending
 #  HOW TO USE
The program will ask how many subjects results you want to analyze. If you are only looking at 1 subject you can just give it one file or many files to analyze.  
IF you are looking to analyze multiple subjects' data it will do it automatically for all 4Script txt files in the directory you provide. Please provide the mother directory to all of your subjects' folders. 
 Or give the path to multiple subjects' data and the number of subjects and let it run automatically 
### Details: 
 As an input it takes the copied output from TurboSatori (TS).  TS outputs it in an internal GUI module; from there the user should copy the output and save it into a txt file with the relevant title
 we suggest using the subject number, the type of signal used, the number of trials used and adding an _4Script
 Example: S02_Results_(D)_Simulated_real_time_4Script 
 **!!!!!!!!ADDING the 4Script in the title is obligatory because that is how this scripts selects the correct file!!!!!!!!!!**


#  How it works
 Goes to the given path of the text file you are trying to compute the accuracy from OR goes through the directory you have given in order to find the file and automatically do the computation for all subjects.
Compute the classification accuracy by checking the predicted 2 (as opposed to 1 - no task) 
is next to the lowest value computed 
then computes average classification accuracy
then outputs to a new file with the same name but without the 4script part (oxy,deoxy, or both), all participants
