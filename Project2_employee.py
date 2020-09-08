## File to generate JSON with employee as root


from pymongo import MongoClient

#Connect to Mongo client on port number 27017
mongo = MongoClient('localhost', 27017)

#initialize mongodb collections to variables
project_db = mongo.MongoProject.project
department_db = mongo.MongoProject.department
employee_data = mongo.MongoProject.employee_data
employee_db = mongo.MongoProject.employee
workson_db = mongo.MongoProject.works_on

#sort employee collection based on employee lastname
employee_db = employee_db.find().sort("Lname")


#method to return department name based on department number
def getDepartment(dept_no):
    dept = department_db.find_one({'Dnumber':dept_no})
    return dept['Dname']


#method to return project list based on employee SSN number
def getProjectList(employeeSSN):
    projectList = []
    for data in workson_db.find({'Essn':employeeSSN}):
        projectList.append(data['Pnum'])

    return projectList


def main():
  
    #Since employee is root iterate through every record in employee collection
    for data in employee_db:
        
        #get department name based on department number
        deptName = getDepartment(data['Dno'])

        #get project list based on employee SSN
        project_List = getProjectList(data['Ssn'])

        finalList = []

        #create project nested object inside the main employee object
        for projectNum in project_List:
            project_data = project_db.find_one({'Number':projectNum})
            hours_data = workson_db.find_one({'Pnum':projectNum, 'Essn':data['Ssn']})
            project_dict = {}
            project_dict['PNAME'] = project_data['Name']
            project_dict['PNUMBER'] = project_data['Number']
            project_dict['HOURS'] = hours_data['Hours']

            #add each project dict value to final list
            finalList.append(project_dict)


        #insert the newly formed JSON to mongodb collection employee_data for each employee record
        try:
            employee_data.insert_one({
                'EMP_LNAME' : data['Lname'],
                'EMP_FNAME' : data['Name'],
                'DNAME' : deptName,
                'PROJECTS' : finalList

            })

        except Exception as e:
            print(e)



if __name__ == '__main__':
    main() 
