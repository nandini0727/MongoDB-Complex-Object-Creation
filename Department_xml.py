## File to generate XML with department as root


from pymongo import MongoClient
import xml.etree.ElementTree as ET

#Connect to Mongo client on port number 27017
mongo = MongoClient('localhost', 27017)

#Create root of XML document
root = ET.Element("DEPARTMENTS")

#initialize mongodb collections to variables
project_db = mongo.MongoProject.project
department_db = mongo.MongoProject.department
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

        #create a department subelement attached to the root for every department record
        departmentEle = ET.SubElement(root,"DEPARTMENT")

        #get manager last name based on Mgr_ssn value
        lastName = getManagerLastName(data['Mgr_ssn'])

        #get manager first name based on Mgr_ssn value
        firstName = getManagerFirstName(data['Mgr_ssn'])

        #add all required subelements data to department element
        ET.SubElement(departmentEle, "DNAME").text = data['Dname']
        ET.SubElement(departmentEle, "DNUMBER").text = str(data['Dnumber'])
        ET.SubElement(departmentEle, "MGR_LNAME").text = lastName
        ET.SubElement(departmentEle, "MGR_FNAME").text = firstName


        #create employee nested element inside the main department element
        for empdata in employee_db.find({}):
            if(empdata['Dno'] == data['Dnumber']):

                #create a employee sublement attached to department element for every matched employee record
                empEle = ET.SubElement(departmentEle,"EMPLOYEE")

                #add all required subelements data to employee element
                ET.SubElement(empEle, 'EMP_LNAME').text = empdata['Lname']
                ET.SubElement(empEle, 'EMP_FNAME').text = empdata['Name']
                ET.SubElement(empEle, 'SALARY').text = str(empdata['Salary'])

    tree = ET.ElementTree(root)

    #write the final tree to xml file
    tree.write('Project2_department.xml')


if __name__ == '__main__':
    main() 
    
