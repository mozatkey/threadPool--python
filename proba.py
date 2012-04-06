import sys


def proba(r_node_num, f_node_num, tries_num, counter):
    sum = 1.0
    if tries_num != 1:
        for i in range(tries_num+1):
            #print i, sum
            sum *= f_node_num/float(r_node_num)
    else:
        sum = f_node_num/float(r_node_num)
    print counter * sum

if __name__ == "__main__":
    proba(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    #print (sys.argv[1], sys.argv[2], sys.argv[3])
