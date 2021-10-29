import numpy as np

#000 - A
#001 - B
#010 - C
#011 - D
#100 - E
#101 - F
#110 - G
#111 - A ov8

#00 - Quarter
#01 - Quarter
#10 - Half
#11 - Whole

def get_random_chrome(rule_size, num_rules):
    """ Generates a random chromosome of 1s and 0s
For a full chromosome, it should be 320 bits (10 bit per rule, 32 rules). """
    length = rule_size * num_rules
    chrome = np.random.randint(2,size=length)
    return chrome
    
