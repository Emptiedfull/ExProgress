from conversion import convert
import timeit,atexit,asyncio
import numpy as np
from ai import mass,log_map



def mapping(con):
    suffix = ""
    
    res = []
    
    if int(con) == 0:
        months = con*12
        
        if int(months) == 0:
            days = con*365
            
            if int(days) == 0:
                hours = days*24
                suffix = " hours"
                res.append(hours)
            else:
                suffix = " days"
                res.append(days)
        else:
            suffix = " months"
            res.append(months)
    else:
        res.append(con)
        suffix=" years"
  
    return [str(int(res[0])) + suffix + " ago",con]

def mapping_alt(con):
   
    years = int(con)
    months = int((con - years) * 12)
    days = int((con - years - months / 12) * 365)
    hours = int(days * 24)
    return [f'{years} years {months} months {days} days {hours} hours',con]


if __name__ == "__main__":

    # p_values = np.random.rand(10)
    p_values = np.random.rand(100)
    results = [mapping_alt(convert(p)) for p in p_values]
    asyncio.run(mass(results))

    print(results)
    atexit.register(log_map)

