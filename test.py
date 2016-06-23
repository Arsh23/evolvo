#thickest
# y = [ (x,phones[x]['Dimensions']['Width']) for x in phones.keys() ]
# z = sorted(y, key=lambda x: x[1],reverse=True)

#thinest
# y = [ (x,phones[x]['Dimensions']['Width']) for x in phones.keys() ]
# z = [ x for x in sorted(y, key=lambda x: x[1]) if x[1] != -1 ]

#smallest area
# y = [ (x,phones[x]['Dimensions']['Height']*phones[x]['Dimensions']['Length']) for x in phones.keys() ]
# z = [ x for x in sorted(y, key=lambda x: x[1]) if x[1] != 1 ]

#largest area
# y = [ (x,phones[x]['Dimensions']['Height']*phones[x]['Dimensions']['Length']) for x in phones.keys() ]
# z = sorted(y, key=lambda x: x[1],reverse=True)


#heaviest
# y = [ (x,phones[x]['Weight']) for x in phones.keys() ]
# z = sorted(y, key=lambda x: x[1],reverse=True)

#lightest
# y = [ (x,phones[x]['Weight']) for x in phones.keys() ]
# z = [ x for x in sorted(y, key=lambda x: x[1]) if x != -1 ]
