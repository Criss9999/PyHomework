from Database import *
import csv

class Chiulangii():
    def __init__(self):
        self.db = Database()  
     
#Executes a SQL query to fetch all access records from the fev_employees.access table.
    def dataSql(self):
        query = "SELECT * from fev_employees.access;"
        self.db.cursor.execute(query)
        results = self.db.cursor.fetchall() 
        self.db.connection.commit()
        return results
    
    def clearData(self):
        date = self.dataSql()
        day =''
        direction = []
        check_direction = []
        for row in range (len(date)):
            if day == '':
                day = (list(date[row])[1].split('-')[2].split('T')[0])
            else:
                if day <= (list(date[row])[1].split('-')[2].split('T')[0]):
                    day = (list(date[row])[1].split('-')[2].split('T')[0])
                    direction.append(list(date[row]))
                    if (direction[0][1].split('-')[2].split('T')[0]) < (date[row][1].split('-')[2].split('T')[0]):
                        direction.pop(0)
        day = ''
        for check in direction:
            for row in range(len(direction)):
                if day == '':
                    day = check[1].split('-')[0][2].split('T')[0]
                elif (check[1].split('-')[2].split('T')[0]) < day:
                    check_direction.append(check)
        if len (check_direction) == 0:
            return direction
        else:
            direction = list (set(check_direction))
            return direction
    
    def dictionary(self):
        sql_dict = []
        info = self.clearData()
        for row in info:
            data = {
                "user_id": row[0],
                "date":row[1],
                "gate_id":row[2],
                "direction":row[3]
            }
            sql_dict.append(data)
            # print (sql_dict)
        return sql_dict
    
#Processes the access records to calculate the amount of time each employee spent at work.
    def timePassBy(self):
        information = self.dictionary()
        data = {}
        time = []
        for entry in information:
            idPerson = entry ["user_id"]
            if idPerson not in data:
                data[idPerson] = []
            data[idPerson].append(entry)
        for user_id in data:
            for point in range(len(data[user_id])):
                hourIn = (data[user_id][point-1]["date"]).split('T')[1].split('.')[0]
                hourOut = (data[user_id][point]["date"]).split('T')[1].split('.')[0]
                direction = (data[user_id][point]["direction"])
                if direction == 'out':
                    workedHours = int(hourOut.split(":")[0]) - int(hourIn.split(":")[0])
                    workedMinutes = int(hourOut.split(":")[1]) - int(hourIn.split(":")[1])
                    content = {
                        "id": user_id,
                        "hours": workedHours,
                        "minutes":workedMinutes
                    }
                    time.append(content)
                    # print (time)
        return time
    
    def idUser(self,idd):
        cursor = self.db.connection.cursor()
        cursor.execute("SELECT first_name, last_name FROM access WHERE id = %s",{idd})
        i = cursor.fetchone()
        cursor.close()
        if i:
            name = i[0] + ''+i[1]
            # print (name)
            return name
        return None

    
    def userIdAndTime(self):
        workedHours = []
        time = {}
        for entry in self.timePassBy():
            id = entry['id']
            hours = entry['hours']
            minutes = entry['minutes']
            if minutes < 0:
                minutes += 60
                hours -= 1
            if id not in time:
                time[id] = {"hours": 0, "minutes": 0}  # Initialize a new entry for this 'id'
            time[id]["hours"] += hours
            time[id]["minutes"] += minutes
            if time[id]["minutes"] >= 60:
                time[id]["hours"] += time[id]["minutes"] // 60
                time[id]["minutes"] = time[id]["minutes"] % 60
        version = dict(time)
        lastVersion = []
        for id,time in version.items():
            workedHours.append(f"{time['hours']} hours{time['minutes']} minutes")
            transform = str(time['hours']) + "hours" + str(time['minutes']) + "minutes"
            entry = {
                "name":self.idUser(id),
                "workedHours": transform
            }
            lastVersion.append(entry)
            # print (lastVersion)
        return lastVersion

    # Create the txt and csv files into the backup_entries folder
    def createChiulangii (self):
        file = self.userIdAndTime()
        with open('TEMA_PY/backup_entries/chiulangii.txt','w') as file:
            for point in file:
                entry = ((file[point]["name"]) + '' + (file[point]["workedHours"]) + '\n')
                file.write(entry)
    # For this tipe of file we need to create a header 
        with open('TEMA_PY/backup_entries/chiulangii.csv','w') as file:
            writer = csv.writer(file)
            header = ['name','workedHours']
            writer.writerow(header)
            for element in file:
                row = [element["name"], element["workedHours"]]
                writer.writerow(row)
        return 'Both chiulangii.txt and chiulangii.csv files were created succesfully'
                
                
                    
                
          

