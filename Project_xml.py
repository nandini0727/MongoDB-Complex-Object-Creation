
## File to generate XML with project as root

from pymongo import MongoClient
import xml.etree.ElementTree as ET

#Connect to Mongo client on port number 27017
mongo = MongoClient('localhost', 27017)

#Create root of XML document
root = ET.Element("PROJECTS")

#initialize mongodb collections to variables
project_db = mongo.MongoProject.project
department_db = mongo.MongoProject.department
employee_db = mongo.MongoProject.employee
workson_db = mongo.MongoProject.workson


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

        #create a project subelement attached to the root for every project record
        projectEle = ET.SubElement(root,"PROJECT")
    
        #get department name based on department number
        deptName = getDepartment(data['Dnum'])

        #get employee ssn list based on project number
        ssn_list = getEmployeesSSNList(data['Number'])

        #add all required subelements data to project element
        ET.SubElement(projectEle, "PNAME").text = data['Name']
        ET.SubElement(projectEle, "PNUMBER").text = str(data['Number'])
        ET.SubElement(projectEle, "DNAME").text = deptName


        #create employee nested element inside the main project element
        for ssn in ssn_list:

            #create a employee sublement attached to project element for every matched employee record
            empEle = ET.SubElement(projectEle,"EMPLOYEE")

            employee_data = employee_db.find_one({'Ssn':ssn})
            hours_data = workson_db.find_one({'Essn':ssn, 'Pnum':data['Number']})
           
            #add all required subelements data to employee element
            ET.SubElement(empEle, 'EMP_LNAME').text = employee_data['Lname']
            ET.SubElement(empEle, 'EMP_FNAME').text = employee_data['Name']
            ET.SubElement(empEle, 'HOURS').text = str(hours_data['Hours'])


    tree = ET.ElementTree(root)

    #write the final tree to xml file
    tree.write('Project2_project.xml')

if __name__ == '__main__':
    main() 



    
