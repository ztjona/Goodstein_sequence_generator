# -*- coding: utf-8 -*-
'''
Python 3.8.6
[MSC v.1916 64 bit (AMD64)]
17 / 11 / 2020
@author: z_tjona
Cuando escribí este código, solo dios y yo sabíamos como funcionaba. Ahora solo lo sabe dios.
"I find that I don't understand things unless I try to program them."
-Donald E. Knuth
'''

''' Goodstein Sequence calculator

################################################### '''

#%%


def toBaseNotation(number, base):
    ''' returns a representation of the number in the given base.
    This representation is a vector with its ith element being the ith power of the base.

    Examples:
    305 in base 10 would be represented as: 5*1 + 0*10 + 3*100
        toBaseNotation(number=305, base=10)
        [5, 0, 3]
    
    35 in base 2 would be represented as: 1 + 1*2^1 + 2^5
        toBaseNotation(number=35, base=2)
        [1, 1, 0, 0, 0, 1]

    Note: it assumes the input number is in base 10.
    ############################################### '''
    result = []
    while number >= base:
        result.append(number % base)
        number //= base

    result.append(number)
    return result

#%%


def toBaseNotation_pairs(number, base):
    ''' returns a representation of the number in the given base.
    This representation is a vector of tuples with every tuple being [digit, exponent].
    When digit is equal to zero it is omitted.

    Examples:
    305 in base 10 would be represented as: 5*1 + 0*10 + 3*100
        toBaseNotation_pairs(number=305, base=10)
        [[5, 0], [3, 2]]
    
    35 in base 2 would be represented as: 1 + 2 + 2^5
        toBaseNotation(number=35, base=2)
        [[1, 0], [1, 1], [1, 5]]

    Note: it assumes the input number is in base 10.
    ############################################### '''
    result = []
    idx = 0
    while number >= base:
        digit = number % base
        if digit > 0:
            result.append([digit, idx])
        number //= base
        idx += 1

    result.append([number, idx])
    return result

#%%


def toHereditaryBaseNotation(number, base):
    ''' returns a representation of a number in Hereditary Base notation.
    This representation is modification of toBaseNotation_pairs.

    Example:
    35 in base 2 would be represented as: 1 + 2 + 2^5
        toBaseNotation(number=35, base=2)
        [[1, 0], [1, 1], [1, 5]]
        But the 5 is bigger or equal than 2, so it must be changed.
        5 in base 2 is: 1 + 2^2
        Then---
        [[1, 0], [1, 1], [1, [[1, 0], [1, 2]] ]]
        But again, 2 is bigger or equal than 2 so it must be changed:
        2 in base 2 is: 2^1
        Then---
        35 = 1 + 2 + 2^(1 + 2^(2^1))
        [[1, 0], [1, 1], [1, [[1, 0], [1, [[1, 1] ] ]] ]]

    
    266 in base 2 is: 2 + 2^3 + 2^8
    3 in base 2 is: 2 + 1
    8 in base 2 is: 2^3
    Placing everything together is:
    266 = 2+ 2^(2 + 1)+ 2^(2^(2 + 1))
        toHereditaryBaseNotation(number=266, base=2)
        [[1, 1], [1, [[1, 0], [1, 1]]], [1, [[1, [[1, 0], [1, 1]]]]]]
    ############################################### '''

    numberExpanded_in_base = toBaseNotation_pairs(number, base)

    # loop to Hereditaryate!
    for idx, x in enumerate(numberExpanded_in_base):
        exponent = x[1]
        if exponent >= base:
            valExpanded_in_base = toHereditaryBaseNotation(exponent, base)
            numberExpanded_in_base[idx][1] = valExpanded_in_base

    return numberExpanded_in_base


def toIntegerfromHereditary(number_as_hereditary, base):
    ''' Returns the integer number (base 10) from its Hereditary Representation.

    Example:
    toIntegerfromHereditary([[1, 1], [1, [[1, 0], [1, 1]]], [1, [[1, [[1, 0], [1, 1]]]]]], base=2)
    266

    View example of toHereditaryBaseNotation
    ############################################### '''
    num = 0
    for digit, exponent in number_as_hereditary:

        if isinstance(exponent, list):
            exponentValue = toIntegerfromHereditary(exponent, base)
        else:
            exponentValue = exponent
        num += digit * (base**exponentValue)
    return num


#%%
def genGoodsteinSequence(number, initialBase=2):
    ''' Generator that returns the next element of the Goodstein sequence.
    ############################################### '''
    base = initialBase
    representation = toHereditaryBaseNotation(number, base)
    nextVal = number
    while nextVal > 0:
        base += 1
        nextVal = toIntegerfromHereditary(representation, base) - 1
        representation = toHereditaryBaseNotation(nextVal, base)
        yield nextVal


def main():
    ''' Gets the first 100 elements of the Goodstein sequence beggining with 4.
    ############################################### '''
    number = 4
    gen = genGoodsteinSequence(number)
    print(number)
    for _ in range(100):
        print(next(gen))
    return


if __name__ == "__main__":
    main()
