## File to generate XML with employee as root

from pymongo import MongoClient
import xml.etree.ElementTree as ET

#Connect to Mongo client on port number 27017
mongo = MongoClient('localhost', 27017)

#Create root of XML document
root = ET.Element("EMPLOYEES")

#initialize mongodb collections to variables
project_db = mongo.MongoProject.project
department_db = mongo.MongoProject.department
employee_db = mongo.MongoProject.employee
workson_db = mongo.MongoProject.workson

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

        #create a employee subelement attached to the root for every employee record
        employeeEle = ET.SubElement(root,"EMPLOYEE")
        
        #get department name based on department number
        deptName = getDepartment(data['Dno'])

        #add all required subelements data to employee element
        ET.SubElement(employeeEle, "EMP_LNAME").text = data['Lname']
        ET.SubElement(employeeEle, "EMP_FNAME").text = data['Name']
        ET.SubElement(employeeEle, "DNAME").text = deptName

        #get project list based on employee SSN
        project_List = getProjectList(data['Ssn'])

        #create project nested element inside the main employee element
        for projectNum in project_List:

            #create a project sublement attached to employee element for every matched project record
            projectEle = ET.SubElement(employeeEle,"PROJECT")

            project_data = project_db.find_one({'Number':projectNum})
            hours_data = workson_db.find_one({'Pnum':projectNum, 'Essn':data['Ssn']})

            #add all required subelements data to project element
            ET.SubElement(projectEle, 'PNAME').text = project_data['Name']
            ET.SubElement(projectEle, 'PNUMBER').text = str(project_data['Number'])
            ET.SubElement(projectEle, 'HOURS').text = str(hours_data['Hours'])

    tree = ET.ElementTree(root)

    #write the final tree to xml file
    tree.write('Project2_employee.xml')


if __name__ == '__main__':
    main() 


    
