import argparse
import logging
import re
import sys
import time


###########
# Logging #
###########

# Set up logging, to a file with the current timestamp.
logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    filename='splits_happen-' + time.strftime('%Y_%m_%d_%H_%M' + '.log'),
                    level=logging.INFO)


####################
# Argument Parsing #
####################

# Argument parsing: Declare a positional argument, input is the bowling score.
parser = argparse.ArgumentParser()
parser.add_argument("score", help="Enter your full bowling score.")
args = parser.parse_args()


# Validates that all characters are digits, "/", "-" or "X".
# Does not validate length, or a host of other cases.
if re.match('^[0-9X/\-]+$', args.score) is None:
    logging.error('Invalid characters entered: %s  Please use digits or the following characters "/-X"', args.score)
    sys.exit()
else:
    logging.info('Valid characters, %s was entered.', args.score)


#############
# Functions #
#############


# Converts all of the special characters into numbers in a new list.
# These will be easier to work with. X = 10, - = 0. We will keep the spare "/" in for now.
# If there were more, we should create a lookup table instead of elifs.

def cleaninput(dirtyscore):

    # expand if the rules of bowling change
    lookupDict={"X": 10, "-": 0, "/": "/"}
    cleanscore = []

    # replaces entries with dictionary
    try:
        for entry in dirtyscore:
            if entry in lookupDict:
                cleanscore.append(lookupDict.get(entry))
            # Move all of the characters to ints
            elif entry.isdigit():
                cleanscore.append(int(entry))
        return cleanscore

    except Exception:
        logging.error("Error in cleanscore function: ", exc_info=True)



# Adds the score up, based on roll/strike/regular score
# Order of checking matters.
# Scoring backwards or breaking this up into frames might have been easier.
def sumtotalscore(sanitized_score):
    totaled = 0
    try:
        for roll in range(len(sanitized_score)):
            # Check to see if the strike is in the last few rolls, otherwise, we get an out of index error
            if len(sanitized_score) - 3 <= roll:
                if sanitized_score[roll] is "/":
                    totaled += (10 - sanitized_score[roll + 1])
                else:
                    totaled += (sanitized_score[roll])

            # Calculate spare
            elif sanitized_score[roll] is "/":
                # Tricky, make sure you subtract the previous roll from 10, then add the next roll
                totaled += (10 - sanitized_score[roll - 1] + sanitized_score[roll + 1])

            # Calculate Strike!
            # Add the strike, and the next two frames, but check for a spare.
            elif int(sanitized_score[roll]) is 10:
                totaled += sanitized_score[roll]
                totaled += sanitized_score[roll+1]
                if sanitized_score[roll + 2] == '/':
                    totaled += (10 - sanitized_score[roll + 1])
                else:
                    totaled += sanitized_score[roll + 2]

            # Add numbers 0-9 directly to the total
            elif 0 <= int(sanitized_score[roll]) <= 9:
                totaled += sanitized_score[roll]

        return totaled
    except Exception:
        logging.error("Error in sumtotalscore function: ", exc_info=True)

################
# Main Program #
################

if __name__ == "__main__":
    try:
        # Calls function to clean bowling score
        converted_score = cleaninput(args.score)
        logging.info('Score after conversion, %s was entered.', converted_score)

        # Calls function to total the sanitized score
        total_score = sumtotalscore(converted_score)
        print('Total score was: ', total_score)
        logging.info('Total score is: %s ', total_score)

    except Exception:
        logging.error("Error in main loop: ", exc_info=True)
