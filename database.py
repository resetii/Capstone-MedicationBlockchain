import sqlite3

conn = sqlite3.connect('MedicalBlockChain.db')

# Create a cursor
x = conn.cursor()


# Create a Table
#x.execute("""CREATE TABLE nodes (
	#indexx int,
	#type text,
	#created_on text,
	#verified_by text,
	#quantity text,
	#block_hash text,
	#previous_hash text
#)""")

# Adds to the database
x.execute("INSERT INTO nodes VALUES ('55435', 'Aiden', 'Mon Apr 12 20:07:58 2021', 'Ellis', '5', '66435', '99837')")


#Query the database
x.execute("SELECT * FROM nodes")
items = x.fetchall()

#print('hi')

for item in items:
	print(str(item[0]) + " " + item[1] + " " + item[2] + " " + item[3] + " " + item[4] + " " + item[5] + " " + item[6])


# Commit our command
conn.commit()

# Close our connection
conn.close()