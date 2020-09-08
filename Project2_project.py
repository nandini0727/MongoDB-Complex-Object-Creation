## File to generate JSON with project as root


from pymongo import MongoClient

#Connect to Mongo client on port number 27017
mongo = MongoClient('localhost', 27017)

#initialize mongodb collections to variables
project_db = mongo.MongoProject.project
department_db = mongo.MongoProject.department
project_data = mongo.MongoProject.project_data
employee_db = mongo.MongoProject.employee
workson_db = mongo.MongoProject.works_on

#sort project collection based on Name
project_db = project_db.find().sort("Name")


#method to return department name based on department number
def getDepartment(dept_no):
    dept = department_db.find_one({'Dnumber':dept_no})
    return dept['Dname']


#method to return employee ssn list based on project number
def getEmployeesSSNList(projectNum):
    ssnList = []
    for data in workson_db.find({'Pnum':projectNum}):
        ssnList.append(data['Essn'])

    return ssnList


def main():
  
    #Since project is root iterate through every record in project collection
    for data in project_db:
    
        #get department name based on department number
        deptName = getDepartment(data['Dnum'])

        #get employee ssn list based on project number
        ssn_list = getEmployeesSSNList(data['Number'])

        employees_List = []

        #create employee nested object inside the main project object
        for ssn in ssn_list:
            employee_data = employee_db.find_one({'Ssn':ssn})
            hours_data = workson_db.find_one({'Essn':ssn, 'Pnum':data['Number']})
            employee_dict = {}
            employee_dict['EMP_LNAME'] = employee_data['Lname']
            employee_dict['EMP_FNAME'] = employee_data['Name']
            employee_dict['HOURS'] = hours_data['Hours']

            #add each employee dict value to final list
            employees_List.append(employee_dict)

        #insert the newly formed JSON to mongodb collection project_data for each project record
        try:
            project_data.insert_one({
                'PNAME' : data['Name'],
                'PNUMBER': data['Number'],
                'DNAME': deptName,
                'EMPLOYEES':employees_List

            })

        except Exception as e:
            print(e)



if __name__ == '__main__':
    main() 
