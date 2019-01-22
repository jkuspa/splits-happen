# Basic unit test for the sumtotalscore function
# Run with the command 'python3.7 test_splits_happen.py'

def test_sumtotalscore():
    assert sumtotalscore([10,10,10,10,10,10,10,10,10,10,10,10]) == 300, "Should be 300"
    assert sumtotalscore([9, 0, 9, 0, 9, 0, 9, 0, 9, 0, 9, 0, 9, 0, 9, 0, 9, 0, 9, 0]) == 90, "Should be 90"
    assert sumtotalscore([5, '/', 5, '/', 5, '/', 5, '/', 5, '/', 5, '/', 5, '/', 5, '/', 5, '/', 5, '/', 5]) == 150, "Should be 150"
    assert sumtotalscore([10, 7, '/', 9, 0, 10, 0, 8, 8, '/', 0, 6, 10, 10, 10, 8, 1]) == 167, "Should be 167"

def sumtotalscore(sanitized_score):
    totaled = 0

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

if __name__ == "__main__":
    test_sumtotalscore()
    print("Everything passed")