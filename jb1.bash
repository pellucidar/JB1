#!/bin/bash

DATE_TIME_START=`date +%F_T_%H-%M-%S`
JB1_LOG_FILE="jb1_$DATE_TIME_START.log"

echo "jb1 Started " $DATE_TIME_START
echo "jb1 Started " $DATE_TIME_START > $JB1_LOG_FILE

pwd >> $JB1_LOG_FILE

python3 jb1.py -v pipeline_problem_data.ms &>> $JB1_LOG_FILE

ERROR_TEST=`grep "ERROR" $JB1_LOG_FILE`
echo "Error Test Contents : " $ERROR_TEST

# For demo purposes only :
#ERROR_TEST="DEMO"
echo "Error Test Contents : " $ERROR_TEST

ERROR_TEST_LENGTH=${#ERROR_TEST}
echo "Error Test Length : " $ERROR_TEST_LENGTH

if [ $ERROR_TEST_LENGTH -eq 0 ]; then
    echo "NO ERRORS"
else
    echo "ERROR DETECTED"
    echo $ERROR_TEST
    ./ds9 jb1_output_basic.fits &
    ./ds9 jb1_output_cleaned.fits &   
fi
   
DATE_TIME_FINISH=`date +%F_T_%H-%M-%S`
echo "jb1 Completed " $DATE_TIME_FINISH
echo "jb1 Completed " $DATE_TIME_FINISH >> $JB1_LOG_FILE

exit 0
