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
def multi_direction_change(start, first_direction,lengths):
    final_res=[start]
    longest_run=[]
    beginning=start
    current_direction=first_direction
    for length in lengths:
        if(current_direction=="up"):
            res= ascending(beginning,length)
            current_direction="down"
         
        else:
            res= descending(beginning,length)
            current_direction="up"

        if len(longest_run)==0: longest_run=res
        else:
            if len(res)>len(longest_run):
                longest_run=res

        final_res.extend(res[1:])

        beginning=res[-1]
    return final_res, longest_run

#small test
# test_lengths=[2,5,3,2]
# # test_upsAnddowns=["down","up","down","up"] #expect: [3,2,3,4,5,6,5,4,5]

# print(multi_direction_change(3,"down",test_lengths)) 
