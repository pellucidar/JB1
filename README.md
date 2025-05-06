# This README is for software JB1
Last updated : 2025-05-06

The software consists of :

1. README - This file.

2. jb1_virtual_env.source

A text file to be run at the local Unix/Linux prompt to set up
   
the relevant Python development/run environment to run the software.

3. jb1.bash

A ".bash" shell script for running the relevant software.

Ensure that this has "execute" authority. (Type at the prompt : $ chmod u+x jb1.bash) 

4. jb1.py

A Python (Python3) program for actually processing the relevant data.

This assumes that the following Python module libraries are available :

sys     

os      

argparse 

datetime 

inspect  

importlib 

casacore 

ducc0 

numpy 

math 

scipy 

matplotlib 

astropy 


To run the software :

1. At the prompt type : $ source jb1_virtual_env.source

This will set up the relevant Python environment.

2. Help text for the main processing program can be viewed by typing at the prompt :
  
$ python3 jb1.py -h

The help text is :

usage: 

jb1.py [-h] [-s SPEC_NAME] [-o OUTPUT_FILE_NAME] [-d OUTPUT_DIRECTORY] [-it NUM_ITERATIONS] 

[-r RESOLUTION [30-300]] [-lpm] [-v] [-t] input_table_name

Jodrell Bank Demo Program Number 1

positional arguments:

  input_table_name      Input table name

options:
  -h, --help            show this help message and exit
  
  -s SPEC_NAME, --spec_name SPEC_NAME
                        Spec name (DEFAULT=SPECTRAL_WINDOW)
  
  -o OUTPUT_FILE_NAME, --output_file_name OUTPUT_FILE_NAME
                        Output directory (DEFAULT=jb1_output.png)
  
  -d OUTPUT_DIRECTORY, --output_directory OUTPUT_DIRECTORY
                        Output directory (DEFAULT=CURRENT)
  
  -it NUM_ITERATIONS, --num_iterations NUM_ITERATIONS
                        Output directory (DEFAULT=600)
  
  -r RESOLUTION [30-300], --resolution RESOLUTION [30-300]
  
  Resolution of output graphics file in DPI (DEFAULT=100dpi, RANGE=30-300dpi)
  
  -lpm, --list_python_modules
                        List Python Modules imported to this program (DEFAULT=NO)
  
  -v, --verbose         Display processing messages to STDOUT (DEFAULT=NO)
  
  -t, --test_mode       Run program in test mode (DEFAULT=NO)


3. To actually run the software to process data type at the prompt : $ ./jb1.bash

4. This will do the following :

Set up a log file with name : jb1_YYYY-MM-DD_T_HH-MM-SS.log

5. Run the main processing program :

$ python3 jb1.py -v pipeline_problem_data.ms >> $JB1_LOG_FILE

This is run in "verbose" ("-v") mode and all output is sent to the log file.

For example purposes "jb1.py" is run with dataset "pipeline_problem_data.ms".

Any relevant dataset(s) may be used.

For example purposes "jb1.py" is run with the default option "SPEC_NAME" "SPECTRAL_WINDOW".

(Any other relevant name may be used with the "-s" "--spec_name" command line argument.)

If other and/or multiple data sets are required to be processed then the "jb1.bash" script
can be modified to read (a)(lists of) file name(s) from (a) relevant director(y)(ies)
and if necessary called multiple times. (EG. Loop on list of file names.)

For the case of multiple calls with different input files the command line arguments :

-o --output_file_name

-d --output_directory

can be used to re-name/re-direct multiple output files, one file per call of "jb1.py". 


6. "jb1.py" produces 4 output files per call with default names : 

jb1_output_basic.png
jb1_output_basic.fits
jb1_output_cleaned.png
jb1_output_cleaned.fits

Default output is to the working directory.

The ".png" files are (A4 paper) sized images of the "basic" (uncleaned)
and "cleaned" images made from the input data.

These may be printed out if a hard copy is needed.

The FITS files are the same output in FITS format.

Cleaning is with a basic "Hogbom" algorithm.

7. Errors in processing are found by "grep" searches of the log file for the word "ERROR".

If no errors are found the following rubric is produced at the prompt :

Error Test Contents : 

Error Test Contents : 

Error Test Length :  0

NO ERRORS

8. For demonstration purposes ONLY the "jb1.bash" script includes the lines :

"# For demo purposes only :"

"#ERROR_TEST="DEMO""

These may be "uncommented" (IE. Remove "#") to generate a (test) "error condition"
demonstrating what happens if an error condition is detected.

9. Currently the "$JB1_LOG_FILE" is searched for the word "ERROR" which is contained in all errors.

However each different potential error reported by "jb1.py" has a different text
hence the "grep" search term may be customized to search for specific errors.

EG. "ERROR : Unable to generate psf".

10. If an error condition is found then the "DS9" FITS file viewer is invoked
for both the "basic" (uncleaned) and "cleaned" images allowing closer examination.

(It is assumed that DS9 is installed on the relevant processing system.
Any other file viewer(s) could be used instead.

The limiting factor is the ability to display FITS and/or ".png" type files.)

12. In its current configuration the "jb1.bash" script ONLY reports error conditions.

It does not decide what to do with any given (set of) error(s).

That decision is to be taken by the relevant operator(s).



Installation Considerations
---------------------------

The "JB1" software is written to be used with maximum configurability.

"jb1.py" may be run "stand alone" at a Unix/Linux command line prompt.

It may also be included as callable module (library) within another Python program.
(Use standard Python "import".)

Either of "jb1.py" or "jb1.bash" may also be included in other scripts 
which could be any (combination) of shell script (bash, csh/tsh, ksh, zsh, etc.) and/or PERL.

For a situation with a large volume of data and/or multiple machines available for processing
it is recommended that (a) script(s) be written which can run multiple invocations of
"jb1.py" on multiple machines at the same time. 

A control script can pass command line arguments either directly or by further levels of script to multiple different invocations
of "jb1.py" on multiple machines allowing simultaneous processing of large quantities of data
in parallel. The multiple machines could be any combination of physical and/or virtual.
