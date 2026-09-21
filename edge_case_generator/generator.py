def ascending(start,length):
    resArr=[start]
    for i in range(1,length):
        resArr.append(start+i)

    return resArr


def descending(start,length):
    resArr=[start]
    for i in range(1,length):
        resArr.append(start-i)

    return resArr


def direction_change(start,first_length, sencond_length, peak_direction):
    if(peak_direction=="up"):
        resStart=ascending(start,first_length)
        resEnd=descending(resStart[first_length-1], sencond_length)
        
    else:
        resStart=descending(start,first_length)
        resEnd=ascending(resStart[first_length-1], sencond_length)
                 
    resStart.extend(resEnd[1:])
    return resStart

#up down up down
#im thinking we pass a list of the valleys and peaks -- ["up","down","up","down"]
#and a list of lengths [2,5,4,3]
# def multi_direction_change()


