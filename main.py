# Amaan Shah, CS 341, Spring 2022
# A console-based Python program that inputs commands from the user and outputs data from the CTA2 L daily ridership database

import sqlite3
import matplotlib.pyplot as figure


########################################################### 
#
# General Stats Functions
#

# num_Stations: Prints number of stations:
def num_Stations(dbCursor):
  dbCursor.execute("""select count(*) 
                        from stations;""")
  row = dbCursor.fetchone();
  print("  # of stations:", f"{row[0]:,}")


# num_Stops: Prints the number of stops:
def num_Stops(dbCursor):
  dbCursor.execute("""select count(*)
                        from stops;""")
  row = dbCursor.fetchone();
  print("  # of stops:", f"{row[0]:,}")


# num_Rides: Prints the number of ride entries:
def num_Rides(dbCursor):
  dbCursor.execute("""select count(*)
                        from ridership;""")
  row = dbCursor.fetchone();
  print("  # of ride entries:", f"{row[0]:,}")


# date_Range: Prints date range in format (earliest) - (recent) [YYYY-MM-DD]
def date_Range(dbCursor):
  dbCursor.execute("""select date(ride_date)
                        from ridership
                        order by ride_date asc
                        limit 1;""")
  early = dbCursor.fetchone();
  dbCursor.execute("""select date(ride_date)
                        from ridership
                        order by ride_date desc
                        limit 1;""")
  recent = dbCursor.fetchone();
  print("  date range:", early[0], "-", recent[0])


# total_Ridership: prints sum of total ridership and returns that value
def total_Ridership(dbCursor):
  dbCursor.execute("""select sum(num_riders)
                        from ridership;""")
  row = dbCursor.fetchone();
  print("  Total ridership:", f"{row[0]:,}")
  return row[0]


# weekday_Riders: prints weekday ridership and percentage of total ridership
def weekday_Riders(dbCursor, total_riders):
  dbCursor.execute("""select sum(num_riders)
                        from ridership
                        where type_of_day = 'W';""")
  weekday = dbCursor.fetchone();
  w_per = (weekday[0] / total_riders) * 100
  print("  Weekday ridership:", f"{weekday[0]:,}", "(" + "{:.2f}".format(w_per) + "%)")


# sat_Riders: print saturday ridership and percentage of total ridership
def sat_Riders(dbCursor, total_riders):
  dbCursor.execute("""select sum(num_riders)
                        from ridership
                        where type_of_day = 'A';""")
  sat = dbCursor.fetchone();
  s_per = (sat[0] / total_riders) * 100
  print("  Saturday ridership:", f"{sat[0]:,}", "(" + "{:.2f}".format(s_per) + "%)")


# hol_Riders: print sunday/holiday ridership and percentage of total ridership
def hol_Riders(dbCursor, total_riders):
  dbCursor.execute("""select sum(num_riders)
                        from ridership
                        where type_of_day = 'U';""")
  sh = dbCursor.fetchone();
  sh_per = (sh[0] / total_riders) * 100
  print("  Sunday/holiday ridership:", f"{sh[0]:,}", "(" + "{:.2f}".format(sh_per) + "%)")
  print()


# print_stats: Given a connection to the CTA database, executes various
# SQL queries to retrieve and output basic stats.
def print_stats(dbConn):
    dbCursor = dbConn.cursor()
    print("General stats:")
    
    # Call functions to print general data:
    num_Stations(dbCursor)
    num_Stops(dbCursor)
    num_Rides(dbCursor)
    date_Range(dbCursor)
    total_riders = total_Ridership(dbCursor)
    weekday_Riders(dbCursor, total_riders)
    sat_Riders(dbCursor, total_riders)
    hol_Riders(dbCursor, total_riders)
    
###########################################################  
#
# Command Functions:
#

# cmd1: Print station id and station name of stations that have names similar to
#       given user input. Order by station name asc. If no matches print error message.
def cmd1(dbCursor):
  print()
  name = input("Enter partial station name (wildcards _ and %): ")
  dbCursor.execute("""select station_id, station_name
                      from stations
                      where station_name like ?
                      order by station_name asc""", [name])
  rows = dbCursor.fetchall()
  
  if len(rows) == 0:
    print("**No stations found...")
  else:
    for row in rows:
      print(row[0], ":", row[1])
  
# cmd2: Output the ridership at each station, in ascending order by station name. Along
# with each value, output the percentage this value represents across the total L 
# ridership. 
def cmd2(dbCursor):
  print("** ridership all stations **")

  dbCursor.execute("select sum(num_riders) from ridership")
  row = dbCursor.fetchone()
  total_riders = row[0]

  dbCursor.execute("""select station_name, sum(num_riders)
                      from ridership join stations on (ridership.station_id = stations.station_id)
                      group by ridership.station_id
                      order by station_name asc;""")
  rows = dbCursor.fetchall()

  for row in rows:
    per = (row[1] / total_riders) * 100
    print(row[0], ":", f"{row[1]:,}", f"({per:.2f}%)")

# cmd3: Output the top-10 busiest stations in terms of ridership, in descending order by ridership.
# Along with each value, output the percentage this value represents across the total L ridership. 
def cmd3(dbCursor):
  print("** top-10 stations **")

  dbCursor.execute("select sum(num_riders) from ridership")
  row = dbCursor.fetchone()
  total_riders = row[0]

  dbCursor.execute("""select station_name, sum(num_riders) as total
                      from ridership join stations on (ridership.station_id = stations.station_id)
                      group by ridership.station_id
                      order by total desc limit 10;""")
  rows = dbCursor.fetchall()

  for row in rows:
    per = (row[1] / total_riders) * 100
    print(row[0], ":", f"{row[1]:,}", f"({per:.2f}%)")

# cmd4: Output the least-10 busiest stations in terms of ridership, in 
# ascending order by ridership
# Along with each value, output the percentage this value represents across the total L ridership.
def cmd4(dbCursor):
  print("** least-10 stations **")

  dbCursor.execute("select sum(num_riders) from ridership")
  row = dbCursor.fetchone()
  total_riders = row[0]

  dbCursor.execute("""select station_name, sum(num_riders) as total
                      from ridership join stations on (ridership.station_id = stations.station_id)
                      group by ridership.station_id
                      order by total asc limit 10;""")
  rows = dbCursor.fetchall()

  for row in rows:
    per = (row[1] / total_riders) * 100
    print(row[0], ":", f"{row[1]:,}", f"({per:.2f}%)")

# cmd5: Input a line color from the user and output all stop names that are part of that line, in ascending order. 
# If the line does not exist, print error statement
def cmd5(dbCursor):
  print()
  color = input("Enter a line color (e.g. Red or Yellow): ")
  dbCursor.execute("""select stop_name, direction, ada
                      from stops
                      join stopdetails on (stops.stop_id = stopdetails.stop_id)
                      join lines on (stopdetails.line_id = lines.line_id)
                      where color like ?
                      order by stop_name asc""", [color])
  rows = dbCursor.fetchall()

  if len(rows) == 0:
    print("**No such line...")
  else:
    for row in rows:
      name = row[0]
      direction = row[1]
      acc = row[2]
      word = ""

      if acc == 1:
        word = "yes"
      else:
        word = "no"
      
      print(name, ":", "direction =", direction, "(accessible?", word +")")


# cmd 6: Outputs total ridership by month, in ascending order by month. After the output, the user is given the
# option to plot the data
def cmd6(dbCursor, figure):
  print("** ridership by month **")
  dbCursor.execute("""select strftime("%m", ride_date) as month, sum(num_riders)
                      from ridership
                      group by month
                      order by month asc;""")
  rows = dbCursor.fetchall()
  for row in rows:
    print (row[0], ":", f"{row[1]:,}" )

  print()
  plot = input("Plot? (y/n) ")
  if plot == "y":
    x = []
    y = []

    for row in rows:
      x.append(row[0])
      y.append(row[1])
    
    figure.xlabel("month")
    figure.ylabel("number of riders (x * 10^8)")
    figure.title("monthly ridership")
    figure.plot(x,y)
    figure.show()
    
# cmd7: Outputs total ridership by year, in ascending order by year. After the output, the user is given the 
# option to plot the data
def cmd7(dbCursor, figure):
  print("** ridership by year **")
  dbCursor.execute("""select strftime("%Y", ride_date) as year, sum(num_riders)
                      from ridership
                      group by year
                      order by year asc;""")
  rows = dbCursor.fetchall()
  for row in rows:
    print (row[0], ":", f"{row[1]:,}" )

  print()
  plot = input("Plot? (y/n) ")
  if plot == "y":
    x = []
    y = []

    for row in rows:
      full = str(row[0])
      last_two = full[-2:]
      x.append(last_two)
      y.append(row[1])
    
    figure.xlabel("year")
    figure.ylabel("number of riders (x * 10^8)")
    figure.title("yearly ridership")
    figure.plot(x,y)
    figure.show()

# cmd8: Inputs a year and the names of two stations (full or partial names), and then outputs the daily 
# ridership at each station for that year. Only output the first 5 days and last 5 days of data for each 
# station. If user wants to plot, the function wil plot the results. 
#
def cmd8(dbCursor, figure):
  print()
  year = input("Year to compare against? ")
  print()

  stat1 = input("Enter station 1 (wildcards _ and %): ")
  dbCursor.execute("""select station_id, station_name
                      from stations
                      where station_name like ?
                      order by station_name asc""", [stat1])
  rows = dbCursor.fetchall()

  if len(rows) == 0:
    print("**No station found...")
    return
  elif len(rows) > 1:
    print("**Multiple stations found...")
    return
  
  stat1_id = rows[0][0]
  stat1_name = rows[0][1]
  print()

  stat2 = input("Enter station 2 (wildcards _ and %): ")
  dbCursor.execute("""select station_id, station_name
                      from stations
                      where station_name like ?
                      order by station_name asc""", [stat2])
  rows = dbCursor.fetchall()

  if len(rows) == 0:
    print("**No station found...")
    return
  elif len(rows) > 1:
    print("**Multiple stations found...")
    return
  
  stat2_id = rows[0][0]
  stat2_name = rows[0][1]

  
  print("Station 1:", stat1_id, stat1_name)
  dbCursor.execute("""select date(ride_date) as time, num_riders
                      from ridership
                      where station_id = ? AND strftime("%Y",ride_date) = ?
                      order by time asc;""", [stat1_id, year])
  first = dbCursor.fetchall()
  i = 0
  while i < 5:
    print(first[i][0], first[i][1])
    i += 1
  last = first[-5:]
  for row in last:
    print(row[0], row[1])

  print("Station 2:", stat2_id, stat2_name)
  dbCursor.execute("""select date(ride_date) as time, num_riders
                      from ridership
                      where station_id = ? AND strftime("%Y",ride_date) = ?
                      order by time asc;""", [stat2_id, year])
  second = dbCursor.fetchall()
  i = 0
  while i < 5:
    print(second[i][0], second[i][1])
    i += 1
  last = second[-5:]
  for row in last:
    print(row[0], row[1])

  print()
  plot = input("Plot? (y/n) ")
  if plot == "y":
    x = []
    y = []
    z = []
    
    day = 0

    for row in first:
      x.append(day)
      y.append(row[1])
      day += 1

    day = 0

    for row in second:
      z.append(row[1])
          
    figure.xlabel("day")
    figure.ylabel("number of riders")
    figure.title("riders each day of " + year)
    figure.plot(x, y)
    figure.plot(x, z)
    figure.legend([stat1_name, stat2_name])
    figure.show()

# cmd9: Input a line color from the user and output all station names that are part of that line, in 
# ascending order. If user wants to plot the data, plots on a map of Chicago using coordinates of stops
# apart of that color CTA line.
def cmd9(dbCursor, figure):
  print()
  color = input("Enter a line color (e.g. Red or Yellow): ")
  dbCursor.execute("""select distinct station_name, latitude, longitude
                      from stations
                      join stops on (stations.station_id = stops.station_id)
                      join stopdetails on (stops.stop_id = stopdetails.stop_id)
                      join lines on (stopdetails.line_id = lines.line_id)
                      where color like ?
                      order by station_name asc;""", [color])
  rows = dbCursor.fetchall()

  if len(rows) == 0:
    print("**No such line...")
  else:
    for row in rows:
      print(row[0], ":", "(" + str(row[1]) + ", " + str(row[2]) + ")")

    print()

    plot = input("Plot? (y/n) ")
    if plot == "y":
      x = [] #longitude
      y = [] #latitude

      image = figure.imread("chicago.png")
      xydims = [-87.9277, -87.5569, 41.7012, 42.0868]
      figure.imshow(image, extent=xydims)

      figure.title(color + " line")

      if color.lower() == "purple-express":
        color = "Purple"
      
      for row in rows:
        x.append(row[2])
        y.append(row[1])

      figure.plot(x, y, "o", c = color)
  
      for row in rows:
        figure.annotate(row[0], (row[2], row[1]))
      
      figure.xlim([-87.9277, -87.5569])
      figure.ylim([41.7012, 42.0868])
      figure.show()

########################################################### 
#
# Main
#
print('** Welcome to CTA L analysis app **')
print()

dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')

print_stats(dbConn)
dbCursor = dbConn.cursor()
while True:
  val = input("Please enter a command (1-9, x to exit): ")
  if val == "x":
    break
  elif val == "1":
    cmd1(dbCursor)
  elif val == "2":
    cmd2(dbCursor)
  elif val == "3":
    cmd3(dbCursor)
  elif val == "4":
    cmd4(dbCursor)
  elif val == "5":
    cmd5(dbCursor)
  elif val == "6":
    cmd6(dbCursor, figure)
  elif val == "7":
    cmd7(dbCursor, figure)
  elif val == "8":
    cmd8(dbCursor, figure)
  elif val == "9":
    cmd9(dbCursor, figure)
  else:
    print("**Error, unknown command, try again...")

  print()
  
#
# done
#
