from flask import Flask , render_template, request, make_response
app = Flask(__name__)

# @app.route('/',methods = ['POST', 'GET'])
@app.route('/assignment11.html',methods = ['POST', 'GET'])
def home():

    # Declaration
    userName = None
    userPass = None
    firstName = None
    lastName = None
    backgroundColor = None
    title = None
    imagePath = None

    logoutRequest = None
    editRequest = None
    createRequest = None
    emptyRequest = True
    userNameExist = False
    passwordMatch = False

    userName = request.args.get('user')
    userPass = request.args.get('pass')
    logoutRequest = request.args.get('logout')
    editRequest = request.args.get('edit')
    createRequest = request.args.get('create')


    # Check if logout-Request
    if logoutRequest != None :
        #Delete cookies
        if request.cookies.get('username') != None :
            resp = make_response(render_template('assignment11.html',logoutSucceed = True, userName = request.cookies.get('username')))
            resp.set_cookie('username', '', expires = 0)
            resp.set_cookie('password', '', expires = 0)
            return resp
        else:
            return render_template('assignment11.html')


    # Check if edit-Request
    if editRequest != None :
        #Get elements
        userName = request.cookies.get('username')
        userPass = request.cookies.get('password')
        firstName = request.args.get('fname')
        lastName = request.args.get('lname')
        backgroundColor = request.args.get('bkcolor')
        title = request.args.get('title')
        imagePath = request.args.get('image')
        
        oldLine = ""
        newLine = ""
        filedata = ""
        
        #Get oldline to replace
        with open('assignment11-account-info.txt') as file:
            for line in file:
                wordLists = line.split(';')
                if userName == wordLists[0]:
                    # ID found
                    userNameExist = True
                    if userPass == wordLists[1]:
                        # Password Match
                        passwordMatch = True
                        # get line to replace
                        oldLine = userName + ";" + userPass + ";" + wordLists[2] + ";" + wordLists[3] + ";" + wordLists[4] + ";" + wordLists[5] + ";" + wordLists[6]
                    break

        #Make new file data with replaced line
        with open('assignment11-account-info.txt') as file:
            filedata = file.read()
        newLine = userName + ";" + userPass + ";" + firstName + ";" + lastName + ";" + backgroundColor + ";" + title + ";" + imagePath + "\n"    
        newFileData = filedata.replace(oldLine,newLine)

        #write the new file
        with open('assignment11-account-info.txt','w') as file:
            file.write(newFileData)


        return render_template('assignment11.html',loginSucced = True, editSucceed = True, userName = userName, firstName = firstName, lastName = lastName, backgroundColor = backgroundColor, title = title, imagePath = imagePath)

    # Check if there is a Cookie 
    if request.cookies.get('username') :
        userName = request.cookies.get('username')
        userPass = request.cookies.get('password')

        # Get elements from txt file
        with open('assignment11-account-info.txt') as file:
            for line in file:
                wordLists = line.split(';')
                if userName == wordLists[0]:
                    # ID found
                    userNameExist = True
                    if userPass == wordLists[1]:
                        # Password Match
                        passwordMatch = True
                        # get the elements
                        firstName = wordLists[2]
                        lastName = wordLists[3]
                        backgroundColor = wordLists[4]
                        title = wordLists[5]
                        imagePath = wordLists[6]

                        print(backgroundColor)
                    break

        return render_template('assignment11.html',loginSucced = True, userName = userName, firstName = firstName, lastName = lastName, backgroundColor = backgroundColor, title = title, imagePath = imagePath)

    # Check if create-Request
    if createRequest != None :
        userName = request.args.get('user')
        userPass = request.args.get('pass')
        firstName = request.args.get('fname')
        lastName = request.args.get('lname')
        backgroundColor = "white"
        title = "Welcome to " + firstName + " " + lastName + "'s Assignment 11 web site!"
        imagePath = "https://upload.wikimedia.org/wikipedia/commons/thumb/9/94/Stick_Figure.svg/1200px-Stick_Figure.svg.png"

        # Form Error checking
        if userName == '':
            return render_template('assignment11.html',noNameForCreating = True)
        elif userPass == '':
            return render_template('assignment11.html',noPassForCreating = True)
        elif firstName == '':
            return render_template('assignment11.html',nofNameForCreating = True)
        elif lastName == '':
            return render_template('assignment11.html',nolNameForCreating = True)

        # Check if ID already Exists
        with open('assignment11-account-info.txt') as file:
            for line in file:
                wordLists = line.split(';')
                if userName == wordLists[0]:
                    # ID found
                    return render_template('assignment11.html',userNameExistForCreating = True, userName = userName)
                    
        # Add new info to text file
        with open('assignment11-account-info.txt','a') as file:
            newLine = userName + ";" + userPass + ";" + firstName + ";" + lastName + ";" + backgroundColor + ";" + title + ";" + imagePath 
            file.write('\n'+ newLine)


    # Check if Login & Initial request
    # Check if user Exists in info.txt
    if userName != None :
        emptyRequest = False
        with open('assignment11-account-info.txt') as file:
            for line in file:
                wordLists = line.split(';')
                if userName == wordLists[0]:
                    # ID found
                    userNameExist = True
                    if userPass == wordLists[1]:
                        # Password Match
                        passwordMatch = True
                        # get the elements
                        firstName = wordLists[2]
                        lastName = wordLists[3]
                        backgroundColor = wordLists[4]
                        title = wordLists[5]
                        imagePath = wordLists[6]

                    break

    if (userName == '' or userPass == '' ) :
        emptyRequest = True

    if emptyRequest == True :
        return render_template('assignment11.html')
    elif passwordMatch == True and userNameExist == True:
        print("login succeed!!!")

        #Create Cookies
        resp = make_response(render_template('assignment11.html',loginSucced = True, userName = userName, firstName = firstName, lastName = lastName, backgroundColor = backgroundColor, title = title, imagePath = imagePath))
        resp.set_cookie('username', wordLists[0])
        resp.set_cookie('password', wordLists[1])
        return resp

    elif passwordMatch == False and userNameExist == True:
        print("password wrong")
        return render_template('assignment11.html',passwordMiss = True)
    else :
        print("User does not exist")
        return render_template('assignment11.html',noUserExist = True) 




@app.route('/assignment11-account-info.txt',methods = ['POST', 'GET'])
def accountInfo():
    return render_template('assignment11-account-info.txt')


if __name__ == '__main__':
    app.debug = True
    app.run()

