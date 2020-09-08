
## File to generate JSON with department as root


from pymongo import MongoClient

#Connect to Mongo client on port number 27017
mongo = MongoClient('localhost', 27017)

#initialize mongodb collections to variables
project_db = mongo.MongoProject.project
department_db = mongo.MongoProject.department
department_data = mongo.MongoProject.department_data
employee_db = mongo.MongoProject.employee
workson_db = mongo.MongoProject.workson

#sort department collection based on department name
department_db = department_db.find().sort("Dname")


#method to return manager last name based on ssn value
def getManagerLastName(ssn):
    data = employee_db.find_one({'Ssn':ssn})
    return data['Lname']


#method to return manager first name based on ssn value
def getManagerFirstName(ssn):
    data = employee_db.find_one({'Ssn':ssn})
    return data['Name']




def main():
      
    #Since department is root iterate through every record in department collection
    for data in department_db:

        #get manager last name based on Mgr_ssn value
        lastName = getManagerLastName(data['Mgr_ssn'])

        #get manager first name based on Mgr_ssn value
        firstName = getManagerFirstName(data['Mgr_ssn'])

        employeeList = []

        #create employee nested object inside the main department object
        for empdata in employee_db.find({}):
            if(empdata['Dno'] == data['Dnumber']):
                empDict = {}
                empDict['EMP_LNAME'] = empdata['Lname']
                empDict['EMP_FNAME'] = empdata['Name']
                empDict['SALARY'] = empdata['Salary']

                #add each employee dict value to employeeList
                employeeList.append(empDict)

            
        #insert the newly formed JSON to mongodb collection department_data for each department record
        try:
            department_data.insert_one({
                'DNAME' : data['Dname'],
                'DNUMBER' : data['Dnumber'],
                'MGR_LNAME' : lastName,
                'MGR_FNAME' : firstName,
                'EMPLOYEES' : employeeList
            })

        except Exception as e:
            print(e)



if __name__ == '__main__':
    main() 
