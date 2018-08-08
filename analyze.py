# most recent visited 18,950,264 pages in 155,988 seconds
from time import time,sleep
import operator

f=open('surf_report-concurrent.tsv','r')
linked_to_ct={} # number of times a link is linked to
linked_from_ct={} # number of places a link links to
# linked_to_list={} # list of links that link to this link
# linked_from_list={} # list of links this link links to

line_idx=0
for line in f:
    line_idx+=1
    if line_idx%20000==0: print("\rLine index: %d"%line_idx,end="\r")
    items=line.strip().split("\t")
    if len(items)==2:
        if items[0] in linked_from_ct:   linked_from_ct[items[0]]+=1
        else:                            linked_from_ct[items[0]]=1
        if items[1] in linked_to_ct:     linked_to_ct[items[1]]+=1
        else:                            linked_to_ct[items[1]]=1
        # if items[1] in linked_to_list:   linked_to_list[items[1]]+=", "+items[0]
        # else:                            linked_to_list[items[1]]=items[0]
        # if items[0] in linked_from_list: linked_from_list[items[0]]+=", "+items[1]
        # else:                            linked_from_list[items[0]]=items[1]

print("\nSorting...")
dest_sorted=sorted(linked_to_ct.items(), reverse=True,key=lambda kv: kv[1])
src_sorted=sorted(linked_from_ct.items(), reverse=True,key=lambda kv: kv[1])

print("Writing results to file...")
dest_f=open("linked_to-count.tsv","w")
for l0,l1 in dest_sorted:
    dest_f.write("%s\t%d\n"%(l0,l1))
src_f=open("linked_from-count.tsv","w")
for l0,l1 in src_sorted:
    src_f.write("%s\t%d\n"%(l0,l1))
# dest_f_list=open("linked_to-list.tsv","w")
# for l0,l1 in linked_to_list:
#     dest_f_list.write("%s\t%s\n"%(l0,l1))
# src_f_list=open("linked_from-list.tsv","w")
# for l0,l1 in linked_from_list:
#     src_f_list.write("%s\t%s\n"%(l0,l1))

print("Closing files...")
f.close()
src_f.close()
dest_f.close()
# dest_f_list.close()
# src_f_list.close()

print("Done!")