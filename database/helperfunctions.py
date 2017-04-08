'''
Created on 1 jan. 2017

@author: Adrian
'''
from datetime import datetime, date


# For summing up e.g., the price in a booking
def listSum(NumberList):
    '''
    Adds numbers in a list.
    '''
    total = 0
    for number in NumberList:
        total += number
        
    return total

def named_month(month_number):
    """
    Return the name of the month, given the number.
    """
    return date(1900, month_number, 1).strftime("%B")

