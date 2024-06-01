# Sideproject-as-Quiz-vol2


#Parses ultra.ge's laptop section using "While True" loop to avoid problems with paging. Also, it avoids
#getting detected from anti-DDOS plugin by randomizing its iterating time and whole information gets
#simultaneously saved into ".csv",".txt" and ".sqlite" files.

#Code brings 3 kinds of information : Laptop's title, price and link to its image.
#Also, code is optimized to handle some advanced occasions, for instance some products
#on "Ultra.ge" are currently on sale, so it checks if product is on sale inside HTML, and brings
#most recent, (current) price.
