import cv2
import numpy as np
import copy
import tkinter as tk
from tkinter import filedialog
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
from tkinter import messagebox
import pymysql

global stuNum
global info

def idRecognition():
    ref = cv2.imread("reference.png")
    ref = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
    ref = cv2.threshold(ref, 10, 255, cv2.THRESH_BINARY_INV)[1]

    # find contours
    # sort them from left to right, and initialize a dictionary to map digit name
    refCnts = cv2.findContours(ref.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    refCnts = imutils.grab_contours(refCnts)
    refCnts = contours.sort_contours(refCnts, method="left-to-right")[0]
    digits = {}

    # loop over the reference contours
    for (i, element) in enumerate(refCnts):
        # compute the bounding box for the digit, extract it, and resize it to a fixed size
        (x, y, w, h) = cv2.boundingRect(element)
        roi = ref[y:y + h, x:x + w]
        roi = cv2.resize(roi, (57, 88))
        digits[i] = roi
        # update the digits dictionary

    # initialize a rectangular and square structuring kernel
    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 3))
    sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

    # load the input image, resize it, and convert it to grayscale
    image = cv2.imread("dst.jpg")
    # image = img
    image = imutils.resize(image, width=600)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_num = gray[340:372, 75:240]

    # apply a tophat (whitehat) morphological operator to find light regions against a dark background
    tophat = cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, rectKernel)

    # compute the gradient of the tophat image, then scal the rest
    gradX = cv2.Sobel(tophat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    gradX_num = gradX[340:372, 75:240]

    gradX_num = np.absolute(gradX_num)
    (minVal, maxVal) = (np.min(gradX_num), np.max(gradX_num))
    gradX_num = (255 * ((gradX_num - minVal) / (maxVal - minVal)))
    gradX_num = gradX_num.astype("uint8")

    # apply a closing operation using the rectangular kernel
    gradX_num = cv2.morphologyEx(gradX_num, cv2.MORPH_CLOSE, rectKernel)
    thresh = cv2.threshold(gradX_num, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, sqKernel)

    # find contours in the thresholded image, then initialize the
    # list of digit locations
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    (x, y, w, h) = cv2.boundingRect(cnts[0])

    output = []

    groupOutput = []

    # extract digits from the grayscale image, then apply thresholding to segment the digits from the background

    kernel = np.ones((2, 2), np.uint8)
    gray_num = cv2.erode(gray_num, kernel, iterations=1)
    group = cv2.threshold(gray_num, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # detect the contours of each individual digit in the group,  then sort the digit contours from left to right
    digitCnts = cv2.findContours(group.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    digitCnts = imutils.grab_contours(digitCnts)
    digitCnts = contours.sort_contours(digitCnts, method="left-to-right")[0]

    for c in digitCnts:
        # compute the bounding box of the individual digit, extract
        # the digit, and resize it
        (x, y, w, h) = cv2.boundingRect(c)
        if ((w * h) > 700 or (w * h) < 50):
            continue
        roi = group[y:y + h, x:x + w]
        roi = cv2.resize(roi, (57, 88))

        # initialize a list of template matching scores
        scores = []

        # loop over the reference digit name and digit ROI
        for (digit, digitROI) in digits.items():
            # apply correlation-based template matching, take the score, and update the scores list
            result = cv2.matchTemplate(roi, digitROI, cv2.TM_CCOEFF_NORMED)
            (_, score, _, _) = cv2.minMaxLoc(result)
            scores.append(score)

        # the classification for the digit will be the reference digit name with the *largest* template matching score

        groupOutput.append(str(np.argmax(scores)))

    # draw the digit classifications around the group
    cv2.rectangle(image, (75, 343), (225, 371), (0, 0, 255), 2)
    cv2.putText(image, "".join(groupOutput), (236, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 0, 255), 2)

    # update the output digits list
    output.extend(groupOutput)
    if(len(output)!=9):
        print("Failed to recognize the student number, please try again!")
        messagebox.showwarning('Recognition Failed', 'Failed to recognize the student number, please try again!')
        return
    stuNum = output
    print("out",output)
    print("stuNum", stuNum)
    gettable(stuNum)
    cv2.imshow("test", image)
    p = cv2.waitKey(0)
    cv2.destroyAllWindows()

    # display the output credit card information to the screen
    print("Credit Card #: {}".format("".join(output)))
    return output


def imageCapture():
    cap = cv2.VideoCapture(0)
    cap.set(3,1080)
    cap.set(4,640)
    cap.set(1, 10.0)

    x=80
    y=50
    w=1000
    h=600

    while(1):
        ret,frame = cap.read()
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
        cv2.startWindowThread()
        cv2.imshow("capture",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            saveImg = frame[y+1:y+h,x+1:x+w]
            cv2.imwrite("Img.jpg", saveImg)
            break

    cap.release()
    #cv2.destroyAllWindows()
    featureMatching(saveImg)
    # cv2.destroyAllWindows()




'''
-------------------------------------------
transform based on Reference 
----------------------------------------------
'''


def featureMatching(cardImage):
    ref = cv2.imread('ref3.png')
    ref_gray = cv2.cvtColor(ref, cv2.COLOR_BGR2GRAY)
    card = copy.copy(cardImage)

    card_gray = cv2.cvtColor(card, cv2.COLOR_BGR2GRAY)
    ref2 = cv2.imread('ref2.png')
    ref2_gray = cv2.cvtColor(ref2, cv2.COLOR_BGR2GRAY)
    surf = cv2.xfeatures2d.SURF_create(400)
    kp1, des1 = surf.detectAndCompute(card, None)
    kp2, des2 = surf.detectAndCompute(ref, None)
    #kp3, des3 = surf.detectAndCompute(ref2, None)

    # matching images by using FLANN
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)
    match = cv2.FlannBasedMatcher(index_params, search_params)
    matches = match.knnMatch(des1, des2, k=2)
    # matches2 = match.knnMatch(des1,des3,k=2)

    # filter through all the matches to obtain the best ones  (card and ref1 )
    good = []
    for m, n in matches:
        if m.distance < 0.6 * n.distance:
            good.append(m)
    # stiching, established a homography and warp perspective
    src_pts = np.array([kp1[m.queryIdx].pt for m in good])
    dst_pts = np.array([kp2[m.trainIdx].pt for m in good])
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    h, w = card_gray.shape
    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
    dst = cv2.perspectiveTransform(pts, M)
    dst = cv2.warpPerspective(card, M, (ref.shape[1], ref.shape[0]))
    cv2.startWindowThread()
    #cv2.imshow("dst", dst)
    cv2.imwrite("dst.jpg", dst)
    # cv2.waitKey()
    # cv2.destroyAllWindows()
    idRecognition()


def selectFile():
    filename = filedialog.askopenfilename(title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    card = cv2.imread(filename)
    featureMatching(card)

def gettable(output):
    conn = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="jasper980906",
        database="student_info",

        charset="utf8"
    )
    cursor = conn.cursor()
    ret = cursor.execute("SELECT * FROM student")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    output = "".join(output)
    print("results",results)
    for row in results:
        if(row[0] == output):
            print("row", row[0])
            print("output", output)
            sid = row[0]
            fname = row[1]
            lname = row[2]
            dept_name = row[3]
            tot_cred = row[4]
    messagebox.showinfo('Student Info', 'Student id:%s\nFirst name:%s\nLast Name: %s'
                                        '\nDepartment Name: %s\nTotal Credit: %s\n' % (
                        sid, fname, lname, dept_name, tot_cred))

def add():
    def add_to_database():
        sid = new_id.get()
        fname = new_fname.get()
        lname = new_lname.get()
        dept_name = new_dept.get()
        tot_cred = new_tot_crd.get()

        conn = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="jasper980906",
            database="student_info",

            charset="utf8"
        )
        cursor = conn.cursor()
        ret = cursor.execute("SELECT * FROM student")
        results = cursor.fetchall()
        for row in results:
            if (row[0] == sid):
                messagebox.showinfo('warning', 'Student exist')
                cursor.close()
                conn.close()
                window_adding.destroy()
                return

        insert_sql = "INSERT INTO student (id, firstname, lastname, dept_name, tot_cred) VALUES ('%s','%s','%s','%s','%s');"% (sid, fname, lname, dept_name, tot_cred)
        cursor.execute(insert_sql)
        conn.commit()
        messagebox.showinfo('success!', 'Successful adding: \nStudent id:%s\nFirst name:%s\nLast Name: %s'
                                            '\nDepartment Name: %s\nTotal Credit: %s\n' % (
                                sid, fname, lname, dept_name, tot_cred))
        cursor.close()
        conn.close()
        window_adding.destroy()

    window_adding = tk.Toplevel(window)
    window_adding.geometry('400x250+500+500')
    window_adding.title('Add student')

    tk.Label(window_adding, text='please enter the student information:').place(x=10, y=10)

    new_id = tk.StringVar()
    tk.Label(window_adding, text='student id').place(x=10, y=40)
    enter_new_id = tk.Entry(window_adding, textvariable=new_id)
    enter_new_id.place(x=150, y=40)

    new_fname = tk.StringVar()
    tk.Label(window_adding, text='first name').place(x=10, y=70)
    enter_new_fname = tk.Entry(window_adding, textvariable=new_fname)
    enter_new_fname.place(x=150, y=70)

    new_lname = tk.StringVar()
    tk.Label(window_adding, text='last name').place(x=10, y=100)
    enter_new_lname = tk.Entry(window_adding, textvariable=new_lname)
    enter_new_lname.place(x=150, y=100)

    new_dept = tk.StringVar()
    tk.Label(window_adding, text='department name').place(x=10, y=130)
    enter_new_dept = tk.Entry(window_adding, textvariable=new_dept)
    enter_new_dept.place(x=150, y=130)

    new_tot_crd = tk.StringVar()
    tk.Label(window_adding, text='total credit').place(x=10, y=160)
    enter_new_tot_crd = tk.Entry(window_adding, textvariable=new_tot_crd)
    enter_new_tot_crd.place(x=150, y=160)

    btn_comfirm = tk.Button(window_adding, text = 'comfirm', command = add_to_database)
    btn_comfirm.place(x=150, y= 200)

def delete():
    def delete_from_database():
        sid = new_id.get()
        a = tk.messagebox.askokcancel('warnning', 'Are you sure you want to delete student(%s)? '%(sid))

        if (a == True):
            conn = pymysql.connect(
                host="127.0.0.1",
                port=3306,
                user="root",
                password="jasper980906",
                database="student_info",

                charset="utf8"
            )
            cursor = conn.cursor()
            ret = cursor.execute("SELECT * FROM student")
            results = cursor.fetchall()
            for row in results:
                if (row[0] == sid):
                    insert_sql = "DELETE FROM student WHERE (id = '" + sid + "');"
                    cursor.execute(insert_sql)
                    conn.commit()

                    messagebox.showinfo('success!', 'Delete successful')
                    cursor.close()
                    conn.close()
                    window_delete.destroy()
                    return
            messagebox.showinfo('warning', 'Student not exist')
            cursor.close()
            conn.close()
            window_delete.destroy()
    window_delete = tk.Toplevel(window)
    window_delete.geometry('400x250+500+500')
    window_delete.title('Delete student')

    tk.Label(window_delete, text='please enter the student id you want to delete:').place(x=10, y=50)

    new_id = tk.StringVar()
    tk.Label(window_delete, text='student id').place(x=10, y=100)
    enter_new_id = tk.Entry(window_delete, textvariable=new_id)
    enter_new_id.place(x=150, y=100)

    btn_comfirm = tk.Button(window_delete, text='comfirm', command=delete_from_database)
    btn_comfirm.place(x=150, y=150)

def enter_info(new_id):
    def add_to_database():
        sid = new_id
        fname = new_fname.get()
        lname = new_lname.get()
        dept_name = new_dept.get()
        tot_cred = new_tot_crd.get()

        conn = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="jasper980906",
            database="student_info",

            charset="utf8"
        )
        cursor = conn.cursor()

        insert_sql = "UPDATE student SET firstname = '%s', lastname = '%s', dept_name = '%s', tot_cred = '%s' WHERE (id = '%s');" % (fname, lname, dept_name, tot_cred, sid)
        cursor.execute(insert_sql)
        conn.commit()
        messagebox.showinfo('success!', 'Successful update: \nStudent id:%s\nFirst name:%s\nLast Name: %s'
                                            '\nDepartment Name: %s\nTotal Credit: %s\n' % (
                                sid, fname, lname, dept_name, tot_cred))
        cursor.close()
        conn.close()
        window_adding.destroy()

    window_adding = tk.Toplevel(window)
    window_adding.geometry('400x250+500+500')
    window_adding.title('Add student')

    tk.Label(window_adding, text='please enter the student information:').place(x=10, y=10)

    tk.Label(window_adding, text='student id').place(x=10, y=40)
    tk.Label(window_adding, text=new_id).place(x=150, y=40)

    new_fname = tk.StringVar()
    tk.Label(window_adding, text='first name').place(x=10, y=70)
    enter_new_fname = tk.Entry(window_adding, textvariable=new_fname)
    enter_new_fname.place(x=150, y=70)

    new_lname = tk.StringVar()
    tk.Label(window_adding, text='last name').place(x=10, y=100)
    enter_new_lname = tk.Entry(window_adding, textvariable=new_lname)
    enter_new_lname.place(x=150, y=100)

    new_dept = tk.StringVar()
    tk.Label(window_adding, text='department name').place(x=10, y=130)
    enter_new_dept = tk.Entry(window_adding, textvariable=new_dept)
    enter_new_dept.place(x=150, y=130)

    new_tot_crd = tk.StringVar()
    tk.Label(window_adding, text='total credit').place(x=10, y=160)
    enter_new_tot_crd = tk.Entry(window_adding, textvariable=new_tot_crd)
    enter_new_tot_crd.place(x=150, y=160)

    btn_comfirm = tk.Button(window_adding, text = 'comfirm', command = add_to_database)
    btn_comfirm.place(x=150, y= 200)

def update():
    def delete_from_database():
            sid = new_id.get()
            print(sid)
            conn = pymysql.connect(
                host="127.0.0.1",
                port=3306,
                user="root",
                password="jasper980906",
                database="student_info",

                charset="utf8"
            )
            cursor = conn.cursor()
            ret = cursor.execute("SELECT * FROM student")
            results = cursor.fetchall()
            for row in results:
                if (row[0] == sid):
                    enter_info(sid)
                    cursor.close()
                    conn.close()
                    window_delete.destroy()
                    return
            messagebox.showinfo('warning', 'Student not exist')
            cursor.close()
            conn.close()
            window_delete.destroy()

    window_delete = tk.Toplevel(window)
    window_delete.geometry('400x250+500+500')
    window_delete.title('Update student')

    tk.Label(window_delete, text='please enter the student id you want to update:').place(x=10, y=50)

    new_id = tk.StringVar()
    tk.Label(window_delete, text='student id').place(x=10, y=100)
    enter_new_id = tk.Entry(window_delete, textvariable=new_id)
    enter_new_id.place(x=150, y=100)

    btn_comfirm = tk.Button(window_delete, text='comfirm', command=delete_from_database)
    btn_comfirm.place(x=150, y=150)

window = tk.Tk()

window.title("Campus Card Recognition System")
window.geometry("400x250+500+500")
L1 = tk.Label(window,text="Take a photo of your campus card: ")
L1.place(x=20, y=50)
L1.pack()
b = tk.Button(window,text="Turn on your camera",command=imageCapture)
b.place(x=300, y=50)
b.pack()
L1 = tk.Label(window,text="Select a local photo: ")
L1.place(x=20, y=100)
L1.pack()

b1 = tk.Button(window,text="upload",command=selectFile)
b1.place(x=300, y=100)
b1.pack()

L2 = tk.Label(window,text="Add student info.: ")
L2.place(x=20, y=150)
L2.pack()
b2 = tk.Button(window,text="Add",command=add)
b2.place(x=300, y=150)
b2.pack()

L2 = tk.Label(window,text="Delete student info.: ")
L2.place(x=20, y=150)
L2.pack()
b3 = tk.Button(window,text="Delete",command=delete)
b3.place(x=300, y=150)
b3.pack()

L2 = tk.Label(window,text="Update student info.: ")
L2.place(x=20, y=150)
L2.pack()
b4 = tk.Button(window,text="Update",command=update)
b4.place(x=300, y=150)
b4.pack()

window.mainloop()



