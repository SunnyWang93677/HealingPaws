### <center>Requirements Analysis</center>

####  1. Purpose of the project
​    The database need to be developed for the pet hospital management software. Based on the principle of easy to use and convenience, the customized database system can be divided into three categories: user information management, Q&A information management and surgery information management. These three categories also respectively have the query, management and other functions.

#### 2. Description of project
​    The new system will allow customers to make appointments for their pets online, and allow employees of Healing Paws to organize, prioritize, and keep track of appointments. Healing Paws has three locations: Beijing, Shanghai and Chengdu.
​    It can relieve the staff of the clinic from the heavy work, greatly reduce the workload, reduce the human error in the work, improve the management efficiency of the clinic operation, so as to improve the management level and business level of the clinic.

#### 3. The specific requirements
  ##### 1) user information management
​    Users are divided into customers and employees. Customers will register and log in to use the software, and employee information will be entered into the system. Employees and customers can set their own basic user information, such as setting passwords, names, phone numbers and so on.
  ##### 2) Q&A information management
​    Customers can use the client to ask questions, and employees can use the employee side to answer those questions.
  ##### 3) Surgery information management
​    Employees can use the software to organize, sort and track pets. Customers can check their pet's information and the operation status. For instance, surgery date confirmed, surgery complete, pet ready for release, etc. 

#### 4. E-R diagram

#### Appendix(Entity analysis):
The employee-side and client-side of the software mainly include 7 types of entities.
1. Entity: XXX Healing Paws Veterinary Hospital;
   Attributes: name, location, ID, principal, contact number.
2. Entity: customer;
   Attributes: name, ID, password, e-mail address, phone number, pet name, pet ID.
3. Entity: employee;
   Attributes: name, ID, password, e-mail address, phone number, hospital.
4. Entity: pet;
   Attributes: pet type(dog or cat), name, ID, injury, surgery ID, hospital.
5. Entity: surgery;
   Attributes: ID, injury, surgery type, surgery date, surgery complete, release date, hospital.
6. Entity: order information;
   Attributes: ID, pet name, customer name, phone number, order date.
7. Entity: Q&A information:
   Attributes: question, answer, customer name, employee name, customer ID, employee ID.
