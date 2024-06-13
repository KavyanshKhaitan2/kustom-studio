import typing
import time
import datetime
from typing import Any

batteryLevel = 100 # in %

# Function to parse a KWGT formula
def parse(formula: str) -> Any:
    if formula.count('$') % 2 != 0:
        # Invalid formula.
        return "Invalid formula!"

    
    # Split formula into parts separated by '$'
    parts = formula.split('$')
    returnVal = ""
    for i, _part in enumerate(parts):
        if i%2 == 0:
            returnVal += _part
            continue
        
        func_name = _part.split('(')[0]
        part = ''.join(_part.split('(')[1:]).removesuffix(')')
        
        args: list[str] = part.split(",")
        args = [i.removeprefix('"').removesuffix('"') for i in args]
        
        print(args, flush=True)
        if func_name == 'bi':
            returnVal += str(bi(args[0]))
            continue
        if func_name == 'df':
            returnVal += str(df(*args))
            continue
        returnVal += _part
        
    return returnVal

def bi(type: str, date: int | float | None = None):
    """
    Date will NOT be implemented!
    """
    if type == 'level':
        return batteryLevel
    
    if type == 'charging':
        return time.time() % 2


def df(_format: str, _date: int | str | None = None):
    """
    FIXME: Custom date to be implemented!
    FIXME: Ref. List needs to be changed
    """
    if _date is None:
        date = time.time()
    else: raise NotImplementedError
    
    ref_list = [
        ['W', 'hh:mm'], # Time as text
        
        ['a' , '%p'], # AM/PM
        ['A' , '%p'], # AM/PM
        
        ['EEEE', '%A'], # WEEKDAY
        ['EEE' , '%a'],
        ['EE'  , '%a'],
        ['E'   , '%a'],
        ['e'   , '%w'],
        

        ['hh', '%I'], # HOUR
        ['h' , '%l'],

        ['MMMM', '%B'], # MONTH
        ['MMM' , '%b'],
        ['MM'  , '%e'],
        ['M'   , '%e'],
        ['o'   , '30'],

        ['mm', '%M'], # MINUTE
        ['m' , '%M'],

        ['ss', '%S'], # SECONDS
        ['s' , '%S'],
        

        ['kk', '%I'], # HOUR OF DAY
        ['k' , '%l'],
        ['H' , '%H'],
        
        ['dd', '%d'], # DAY/MONTH
        ['d' , '%e'],
        


        ['DDDD', '%j'], # DAY/YEAR
        ['DDD' , '%j'],
        ['DD'  , '%j'],
        ['D'   , '%j'],
        
        ['zzzz', '%Z'], # TIME ZONE INDICATOR
        ['zzz' , '%Z'],
        ['zz'  , '%Z'],
        ['z'   , '%Z'],
        
        ['S', 'Special EPOCH time'], # SPECIAL EPOCH TIME
    ]
    
    format = _format
    for ref, repl in ref_list:
        replacement = repl
        if ref == 'S':
            replacement = str(time.time())
        format = format.replace(ref, replacement)
        
    dt = datetime.datetime.now()
    return dt.strftime(format)