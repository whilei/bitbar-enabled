#!/bin/bash

# echo "One"
# echo "Two"
# echo "Three"
# echo "---"
# echo "Four"
# echo "Five"
# echo "Six"


#################### 

# SPARK="/usr/local/Cellar/spark/1.0.1/bin/spark"

# if [ ! -f "${SPARK}" ]; then
#     echo "Install spark utility please."
#     exit 1
# fi




# IDLE=`top -F -R -l3 | grep "CPU usage" | tail -1 | \
#       egrep -o '[0-9]{0,3}\.[0-9]{0,2}% idle' | sed 's/% idle//'`

# CURRENT=$(printf "%.0f" $(echo 100 - $IDLE | bc))

# # Let's put/keep last 6 values (= one minute) in HISTORY_FILE
# HISTORY_FILE="${HOME}/.cpu.history"
# touch "${HISTORY_FILE}"
# PREVIOUS=`tail -5 "${HISTORY_FILE}"`
# echo "$PREVIOUS" > "${HISTORY_FILE}"
# echo $CURRENT >> "${HISTORY_FILE}"

# # Spark outputs unicode characters so let's make sure we can handle
# # them correctly.
# LC_ALL=en_US.UTF-8

# # Spark uses maximum input value to define scale so let's make sure
# # that input contains at least one 100(%). Strip it afterwards.
# CHART=`( echo 100 ; cat ${HISTORY_FILE} ) | ${SPARK}`
# echo ${CHART:1}






# CHART=`(echo 2 3 4 5 ) | ${SPARK}`

# echo ${CHART}