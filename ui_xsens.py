#Salih Toprak
import tkinter as tk
import customtkinter as ctk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror

import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

from load_mvnx import load_mvnx

import pandas as pd

import xlsxwriter

from scipy.io import loadmat
import scipy.signal 

class body:
    file_path_mvnx = []
    file_path_mat = []
    selection_idx = None
    picked_joint = ""
    picked_move = ""

    joints = [
            "Hips",
            "Knees",
            "Ankles",
            "Ball Foots",
            "C1-Head",
            "T1-C7",
            "T9-T8",
            "L1-T12",
            "L4-L3",
            "L5-S1",
            "T4 Shoulders",
            "Shoulders",
            "Elbow",
            "Wrists"]
        
    move = [
            "Flexion/Extension",
            "Abduction/Adduction",
            "Internal/External"]

    @classmethod
    def anim(cls):
        if cls.file_path_mvnx == []:
            errorMBox = showerror("Warning", "Select a file")
            pass
        else:
            data = load_mvnx(file_name=cls.file_path_mvnx[0])
            frame_count = data.frame_count
            segment_pos = []
            
            figr = []

            for i in range(23):
                segment_pos.append(data.get_segment_pos(i))

            body_x = []
            body_y = []
            body_z = []

            figr = []

            #Organising data
            for a in range(frame_count):
                body_parts_x = []
                body_parts_y = []
                body_parts_z = []

                for k in range(23):
                    body_parts_x.append(segment_pos[k][a][0])
                    body_parts_y.append(segment_pos[k][a][1])
                    body_parts_z.append(segment_pos[k][a][2])

                #Drawing the figure in each axis
                body_x.append([body_parts_x[14], body_parts_x[13], body_parts_x[12], body_parts_x[11], body_parts_x[5], body_parts_x[6], body_parts_x[5], body_parts_x[7], body_parts_x[8], body_parts_x[9], body_parts_x[10], body_parts_x[9], body_parts_x[8], body_parts_x[7], body_parts_x[4], body_parts_x[11], body_parts_x[4], body_parts_x[3], body_parts_x[2], body_parts_x[1], body_parts_x[0], body_parts_x[15], body_parts_x[16], body_parts_x[17], body_parts_x[18], body_parts_x[17], body_parts_x[16], body_parts_x[15], body_parts_x[0], body_parts_x[19], body_parts_x[20], body_parts_x[21], body_parts_x[22]])

                body_y.append([body_parts_y[14], body_parts_y[13], body_parts_y[12], body_parts_y[11], body_parts_y[5], body_parts_y[6], body_parts_y[5], body_parts_y[7], body_parts_y[8], body_parts_y[9], body_parts_y[10], body_parts_y[9], body_parts_y[8], body_parts_y[7], body_parts_y[4], body_parts_y[11], body_parts_y[4], body_parts_y[3], body_parts_y[2], body_parts_y[1], body_parts_y[0], body_parts_y[15], body_parts_y[16], body_parts_y[17], body_parts_y[18], body_parts_y[17], body_parts_y[16], body_parts_y[15], body_parts_y[0], body_parts_y[19], body_parts_y[20], body_parts_y[21], body_parts_y[22]])

                body_z.append([body_parts_z[14], body_parts_z[13], body_parts_z[12], body_parts_z[11], body_parts_z[5], body_parts_z[6], body_parts_z[5], body_parts_z[7], body_parts_z[8], body_parts_z[9], body_parts_z[10], body_parts_z[9], body_parts_z[8], body_parts_z[7], body_parts_z[4], body_parts_z[11], body_parts_z[4], body_parts_z[3], body_parts_z[2], body_parts_z[1], body_parts_z[0], body_parts_z[15], body_parts_z[16], body_parts_z[17], body_parts_z[18], body_parts_z[17], body_parts_z[16], body_parts_z[15], body_parts_z[0], body_parts_z[19], body_parts_z[20], body_parts_z[21], body_parts_z[22]])

                #Organised data for plotting
                figr.append([body_x[a], body_y[a], body_z[a]])

                

            #Ploting the figure
            fig = plt.figure(figsize=(6.2,4.2))
            ax = fig.add_subplot(111, projection="3d")
            mngr = plt.get_current_fig_manager()
            mngr.window.geometry("+900+15")

            def func(num, data, line):
                line.set_data(data[num][0], data[num][1])
                line.set_3d_properties(data[num][2])
                ax.set_xlim3d(figr[num][0][20]-1, figr[num][0][20]+1)
                ax.set_ylim3d(figr[num][1][20]-1, figr[num][1][20]+1)
                ax.set_zlim3d(figr[num][2][20]-1, figr[num][2][20]+1)

                return line

            line, = ax.plot(figr[0][0], figr[0][1], figr[0][2], lw=2, color="black", marker="H", ms=3, mfc="red")
            ax.view_init(elev=10, azim=-120, roll=0)
            ani = animation.FuncAnimation(fig, func, frame_count, fargs=(figr, line), interval=30, blit=False)  
            plt.show()

    @classmethod
    def browseFunc(cls):
        cls.file_path_mvnx.clear()
        entry.delete(0, tk.END)
        filename = askopenfilename(filetypes=(("MVNX File", "*.mvnx"),("All Files", "*.*")))
        entry.insert(tk.END, filename)
        cls.file_path_mvnx.append(str(filename))

    @classmethod
    def browseFunc2(cls):
        cls.file_path_mat.clear()
        entryEMG.delete(0, tk.END)
        filename = askopenfilename(filetypes=(("MAT File", "*.mat"), ("All Files", "*.*")))
        entryEMG.insert(tk.END, filename)
        cls.file_path_mat.append(str(filename))

    @classmethod
    def menuJoint(cls, selection):
        selection = jointDropdown.get()
        cls.picked_joint = selection
        for i in range(len(cls.joints)):
            if cls.joints[i] == selection:
                cls.selection_idx = i
    
    @classmethod
    def menuMove(cls, selection):
        selection = moveDropdown.get()
        cls.picked_move = selection

    @classmethod
    def gait(cls):
        if cls.file_path_mvnx == []:
            errorMBox = showerror("Warning", "Select a file")
            pass

        else:
            left_heel_strikes = []
            right_heel_strikes = []
            right_joint = []
            left_joint = []
            xleft_gait_cycles = []
            yleft_gait_cycles = []
            zleft_gait_cycles = []
            xright_gait_cycles = []
            yright_gait_cycles = []
            zright_gait_cycles = []
            foot_contacts = []

            #A function for reading the joint data
            def get_joint1(RjointIndex, LjointIndex, rList, lList):
                for i in range(frame_count):
                    rList.append(data.get_joint_angle(RjointIndex)[i])
                    lList.append(data.get_joint_angle(LjointIndex)[i])
                    
            #Seperating each axis of cycles with a function
            def organise_joint(rList, lList):
                j = 1
                for j in range(len(left_heel_strikes)):
                    ltempListx = []
                    ltempListy = []
                    ltempListz = []

                    if left_heel_strikes[j] == 0:
                        continue
                    if len(range(left_heel_strikes[j-1], left_heel_strikes[j])) < 10:
                        continue
                    for x in range(left_heel_strikes[j-1], left_heel_strikes[j]):
                        ltempListx.append(lList[x][0])
                        ltempListy.append(lList[x][1])
                        ltempListz.append(lList[x][2])
                    xleft_gait_cycles.append(ltempListx)
                    yleft_gait_cycles.append(ltempListy)
                    zleft_gait_cycles.append(ltempListz)

                k = 1
                for k in range(len(right_heel_strikes)):
                    rtempListx = []
                    rtempListy = []
                    rtempListz = []

                    if right_heel_strikes[k] == 0:
                        continue
                    if len(range(right_heel_strikes[k-1], right_heel_strikes[k])) < 10:
                        continue
                    for y in range(right_heel_strikes[k-1], right_heel_strikes[k]):
                        rtempListx.append(rList[y][0])
                        rtempListy.append(rList[y][1])
                        rtempListz.append(rList[y][2])
                    xright_gait_cycles.append(rtempListx)
                    yright_gait_cycles.append(rtempListy)
                    zright_gait_cycles.append(rtempListz)
                
            if cls.picked_joint == "" and cls.picked_move == "":
                errorMBox = showerror("Warning", "Select joint and move")
                pass
            else:
                data = load_mvnx(file_name= cls.file_path_mvnx[0])
                frame_count = data.frame_count
                temp = []

                for idx in range(frame_count):
                    temp.append(data.get_foot_contacts(frame=idx))
                    foot_contacts.append(temp[idx][0])

                #Determinating the heel strikes for each foot
                i = 1
                for i in range(frame_count):
                    if foot_contacts[i-1][1] - foot_contacts[i][1] == -1:
                        left_heel_strikes.append(i)

                ix = 1
                for ix in range(frame_count):
                    if foot_contacts[ix-1][3] - foot_contacts[ix][3] == -1:
                        right_heel_strikes.append(ix)

                if cls.selection_idx == 0:#Hips
                    get_joint1(14, 18, right_joint, left_joint)
                        
                elif cls.selection_idx == 1:#Knees
                    get_joint1(15, 19, right_joint, left_joint)

                elif cls.selection_idx == 2:#Ankles
                    get_joint1(16, 20, right_joint, left_joint)

                elif cls.selection_idx == 3:#Ball Foots
                    get_joint1(17, 21, right_joint, left_joint)

                elif cls.selection_idx == 4:#C1-Head
                    get_joint1(5, 5, right_joint, left_joint)

                elif cls.selection_idx == 5:#T1-C7
                    get_joint1(4, 4, right_joint, left_joint)
                        
                elif cls.selection_idx == 6:#T9-T8
                    get_joint1(3, 3, right_joint, left_joint)

                elif cls.selection_idx == 7:#L1-T12
                    get_joint1(2, 2, right_joint, left_joint)

                elif cls.selection_idx == 8:#L4-L3
                    get_joint1(1, 1, right_joint, left_joint)

                elif cls.selection_idx == 9:#L5-S1
                    get_joint1(0, 0, right_joint, left_joint)

                elif cls.selection_idx == 10:#T4 Shoulder
                    get_joint1(6, 10, right_joint, left_joint)

                elif cls.selection_idx == 11:#Shoulder
                    get_joint1(7, 11, right_joint, left_joint)
                    
                elif cls.selection_idx == 12:#Elbow
                    get_joint1(8, 12, right_joint, left_joint)

                elif cls.selection_idx == 13:#Wrist
                    get_joint1(9, 13, right_joint, left_joint)

                organise_joint(right_joint, left_joint)

                #Plotting the final data 
                #[x,y,z] == [internal, abduct, flexion]  
                fig = plt.figure(figsize=(8.8,3))
                mngr = plt.get_current_fig_manager()
                mngr.window.geometry("+0+15")
                if cls.picked_move == "Internal/External":
                    for i in range(len(xleft_gait_cycles)):
                        plt.subplot(1, 2, 1) 
                        plt.title("Left")
                        plt.plot(xleft_gait_cycles[i], lw=0.5)

                    for i in range(len(xright_gait_cycles)):
                        plt.subplot(1, 2, 2)
                        plt.title("Right")
                        plt.plot(xright_gait_cycles[i], lw=0.5)

                if cls.picked_move == "Abduction/Adduction":
                    for i in range(len(yleft_gait_cycles)):
                        plt.subplot(1, 2, 1)
                        plt.title("Left")
                        plt.plot(yleft_gait_cycles[i], lw=0.5)

                    for i in range(len(yright_gait_cycles)):
                        plt.subplot(1, 2, 2)
                        plt.title("Right")
                        plt.plot(yright_gait_cycles[i], lw=0.5)

                if cls.picked_move == "Flexion/Extension":
                    for i in range(len(zleft_gait_cycles)):
                        plt.subplot(1, 2, 1) 
                        plt.title("Left")
                        plt.plot(zleft_gait_cycles[i], lw=0.5)

                    for i in range(len(zright_gait_cycles)):
                        plt.subplot(1, 2, 2)
                        plt.title("Right")
                        plt.plot(zright_gait_cycles[i], lw=0.5)

                plt.suptitle(cls.picked_joint+" "+cls.picked_move)
                plt.show()

    #Func for saving cycles as an excel file
    @classmethod
    def writeExcel(cls):
        if cls.file_path_mvnx != [] and cls.picked_joint != "":
            frame_count = None
            f_contacts = []
            heel_left = []
            heel_right = []
            right_joint = []
            left_joint = []
            xRgait = []
            yRgait = []
            zRgait = []
            xLgait = []
            yLgait = []
            zLgait = []

            data = load_mvnx(file_name= cls.file_path[0])

            def organise_joint1(jointData1, jointData2, lHeel, rHeel, xRgait, yRgait, zRgait, xLgait, yLgait, zLgait):
                j = 1
                for j in range(len(lHeel)):
                    ltempListx = []
                    ltempListy = []
                    ltempListz = []

                    if lHeel[j] == 0:
                        continue
                    if len(range(lHeel[j-1], lHeel[j])) < 10:
                        continue
                    for x in range(lHeel[j-1], lHeel[j]):
                        ltempListx.append(jointData1[x][0])
                        ltempListy.append(jointData1[x][1])
                        ltempListz.append(jointData1[x][2])
                    xLgait.append(ltempListx)
                    yLgait.append(ltempListy)
                    zLgait.append(ltempListz)

                k = 1
                for k in range(len(rHeel)):
                    rtempListx = []
                    rtempListy = []
                    rtempListz = []

                    if rHeel[k] == 0:
                        continue
                    if len(range(rHeel[k-1], rHeel[k]))<10:
                        continue
                    for y in range(rHeel[k-1], rHeel[k]):
                        rtempListx.append(jointData2[y][0])
                        rtempListy.append(jointData2[y][1])
                        rtempListz.append(jointData2[y][2])
                    xRgait.append(rtempListx)
                    yRgait.append(rtempListy)
                    zRgait.append(rtempListz)
            
            def get_joint1(jointIndex1, jointIndex2, rList, lList):
                for i in range(frame_count):
                    rList.append(data.get_joint_angle(jointIndex1)[i])
                    lList.append(data.get_joint_angle(jointIndex2)[i])

            frame_count = data.frame_count
            temp = []

            for idx in range(frame_count):
                temp.append(data.get_foot_contacts(frame=idx))
                f_contacts.append(temp[idx][0])

            #Determinating the heel strikes for each foot
            i = 1
            for i in range(frame_count):
                if f_contacts[i-1][1] - f_contacts[i][1] == -1:
                    heel_left.append(i)

            ix = 1
            for ix in range(frame_count):
                if f_contacts[ix-1][3] - f_contacts[ix][3] == -1:
                    heel_right.append(ix)

            if cls.selection_idx == 0:#Hips
                get_joint1(14, 18, right_joint ,left_joint )
                    
            elif cls.selection_idx == 1:#Knees
                get_joint1(15, 19, right_joint, left_joint)

            elif cls.selection_idx == 2:#Ankles
                get_joint1(16, 20, right_joint, left_joint)

            elif cls.selection_idx == 3:#Ball Foots
                get_joint1(17, 21, right_joint, left_joint)

            elif cls.selection_idx == 4:#C1-Head
                get_joint1(5, 5, right_joint, left_joint)

            elif cls.selection_idx == 5:#T1-C7
                get_joint1(4, 4, right_joint, left_joint)
                    
            elif cls.selection_idx == 6:#T9-T8
                get_joint1(3, 3, right_joint, left_joint)

            elif cls.selection_idx == 7:#L1-T12
                get_joint1(2, 2, right_joint, left_joint)

            elif cls.selection_idx == 8:#L4-L3
                get_joint1(1, 1, right_joint, left_joint)

            elif cls.selection_idx == 9:#L5-S1
                get_joint1(0, 0, right_joint, left_joint)

            elif cls.selection_idx == 10:#T4 Shoulder
                get_joint1(6, 10, right_joint, left_joint)

            elif cls.selection_idx == 11:#Shoulder
                get_joint1(7, 11, right_joint, left_joint)
                
            elif cls.selection_idx == 12:#Elbow
                get_joint1(8, 12, right_joint, left_joint)

            elif cls.selection_idx == 13:#Wrist
                get_joint1(9, 13, right_joint, left_joint)


            organise_joint1(right_joint, left_joint, heel_left, heel_right, xRgait, yRgait, zRgait, xLgait, yLgait, zLgait)
            
            workbook = xlsxwriter.Workbook(cls.picked_joint+".xlsx")
            worksheetFlexL = workbook.add_worksheet("Flexion-Extension Left")
            worksheetFlexR = workbook.add_worksheet("Flexion-Extension Right")
            worksheetAbductL = workbook.add_worksheet("Abduction-Adduction Left")
            worksheetAbductR = workbook.add_worksheet("Abduction-Adduction Right")
            worksheetRotateL = workbook.add_worksheet("Int-Ext Rotation Left")
            worksheetRotateR = workbook.add_worksheet("Int-Ext Rotation Right")

            #[x,y,z] == [internal, abduct, flexion]
            def writeSheet(sheet, entry):
                for a in range(len(entry)):
                    for b in range(len(entry[a])):
                        sheet.write(b, a, entry[a][b])

            writeSheet(worksheetRotateL, xLgait)
            writeSheet(worksheetRotateR, xRgait)
            writeSheet(worksheetAbductL, yLgait)
            writeSheet(worksheetAbductR, yRgait)
            writeSheet(worksheetFlexL, zLgait)
            writeSheet(worksheetFlexR, zRgait)

            workbook.close()
        else:
            errorMBox = showerror("Warning", "Select a file and joint")
            pass

    #EMG func
    @classmethod 
    def emg(cls):
        #Checking if user selected a file. If not error pop-up
        if cls.file_path_mat == [] or cls.file_path_mvnx == []:
            showerror("Warning", "Select files")
        else:
            #Importing .mat file
            data = loadmat(file_name=cls.file_path_emg[0])
            dd = data.get("Data")
            channels = data.get("Channels")
            df = scipy.signal.detrend(dd)
            fs = int(data.get("Fs")[0])
            fc = 10

            foot_contacts = []
            left_heel_strikes = []
            right_heel_strikes = []
            left_temp = []
            right_temp = []
            left_cycles = []
            right_cycles = []

            #Importing the walking data
            data = load_mvnx(cls.file_path[0])
            frame_count = data.frame_count
            temp = []

            for idx in range(frame_count):
                temp.append(data.get_foot_contacts(frame=idx))
                foot_contacts.append(temp[idx][0])

            #Determinating the heel strikes for each foot
            i = 1
            for i in range(frame_count):
                if foot_contacts[i-1][1] - foot_contacts[i][1] == -1:
                    left_heel_strikes.append(i)

            ix = 1
            for ix in range(frame_count):
                if foot_contacts[ix-1][3] - foot_contacts[ix][3] == -1:
                    right_heel_strikes.append(ix)

            #Making EMG's x-axis values compatible with XSENS data 
            for a in range(len(left_heel_strikes)):
                left_temp.append((left_heel_strikes[a]/60)*2148)
            for b in range(len(right_heel_strikes)):
                right_temp.append((right_heel_strikes[b]/60)*2148)

            #Organising the data
            mxl = []
            for x in range(len(df)):
                ltempList1 = []
                z = 1
                for z in range(len(left_temp)):
                    ltempList2 = []
                    mx = []
                    for y in range(int(left_temp[z-1]),int(left_temp[z])):
                        ltempList2.append(abs(df[x][y]))
                    if ltempList2 != []:
                        mx.append(max(ltempList2))
                    ltempList1.append(ltempList2)
                mxl.append(max(mx))
                left_cycles.append(ltempList1)
            mxr = []
            for c in range(len(df)):
                rtempList1 = []
                a = 1
                for a in range(len(right_temp)):
                    rtempList2 = []
                    mx = []
                    for b in range(int(right_temp[a-1]), int(right_temp[a])):
                        rtempList2.append(abs(df[c][b]))
                    if rtempList2 != []:
                        mx.append(max(rtempList2))
                    rtempList1.append(rtempList2)
                mxr.append(max(mx))
                right_cycles.append(rtempList1)

            #Plotting func
            def plot(num):
                for i in range(len(left_cycles[num])):
                    if len(left_cycles[num][i]) == 0:
                        continue
                    #Normalization parts
                    b, a = scipy.signal.butter(2, fc/(fs/2))
                    filtfilted = scipy.signal.filtfilt(b, a, left_cycles[num][i])

                    norm = filtfilted/mxl[num]
                   
                    y = pd.DataFrame(norm)
                    y_new = y.iloc[:,0].rolling(250).mean()

                    xaxisR = []
                    for j in range(len(left_cycles[num][i])):
                        temp = (j/2148)*60
                        xaxisR.append(temp)

                    plt.title(channels[num])
                    plt.subplot(1, 2, 1)
                    plt.plot(xaxisR, y_new, lw=0.25, color="black")

                for k in range(len(right_cycles[num+1])):
                    if len(right_cycles[1][k]) == 0:
                        continue
                    #Normalization parts
                    b, a = scipy.signal.butter(2, fc/(fs/2))
                    filtfilted = scipy.signal.filtfilt(b, a, right_cycles[num+1][k])

                    norm = filtfilted/mxr[num+1]

                    y = pd.DataFrame(norm)
                    y_new = y.iloc[:,0].rolling(250).mean()

                    xaxisL = []
                    for c in range(len(right_cycles[num+1][k])):
                        temp = (c/2148)*60
                        xaxisL.append(temp)

                    plt.title(channels[num+1])
                    plt.subplot(1, 2, 2)
                    plt.plot(xaxisL, y_new, lw=0.25, color="black")

            index = 0
            while index < len(df):
                if index%2==0:
                    figg = plt.figure()
                    mng = plt.get_current_fig_manager()
                    mng.window.geometry("+0+400")
                    plot(index)
                    index+=1
                else:
                    index+=1
                    continue
            plt.show()
    
bodyC = body()

ctk.set_appearance_mode("System")
ctk.set_default_color_theme(r"C:\Users\Salih\OneDrive\Desktop\Scripts\VS\mvnx-desktop-app-main\Themes\MoonlitSky.json")
ctk.set_window_scaling(1.2)
ctk.set_widget_scaling(1)

form = ctk.CTk(screenName="MVNX-UI")
form.title("MVNX-UI")
form.geometry("500x300+650+520")

#Setting the font size
font1 = ctk.CTkFont(size=14)

#Text ".mvnx File directory:"
labelBrowser = ctk.CTkLabel(form, text=".mvnx file directory:", font=font1)
labelBrowser.place(x=15, y=10)
labelBrowser.pack

#Text "Joint :"
labelDd1 = ctk.CTkLabel(form, text="Joint:", font=font1)
labelDd1.place(x=15, y=65)
labelDd1.pack

#Text "Movement :"
labelDd2 = ctk.CTkLabel(form, text="Movement:", font=font1)
labelDd2.place(x=215, y=65)
labelDd2.pack

#Text ".csv, .xlsx File directory:"
labelBrowser2 = ctk.CTkLabel(form, text=".csv, .xlsx file directory", font=font1)
labelBrowser2.place(x=15, y=125)
labelBrowser2.pack

#File browser
entry = ctk.CTkEntry(form, width=400, height=25, font=font1)
entry.place(x=15, y=35)
entry.pack

#Browse button
buttonBrowse = ctk.CTkButton(form, text="Browse", command=bodyC.browseFunc, font=font1)
buttonBrowse.place(x=445, y=35)
buttonBrowse.pack

#Play button
buttonPlay = ctk.CTkButton(form, text="Play", command=bodyC.anim, font=font1)
buttonPlay.place(x=445, y=260)
buttonPlay.pack

#Gait button
buttonGait = ctk.CTkButton(form, text="Gait", command=bodyC.gait, font=font1)
buttonGait.place(x=445, y=90)
buttonGait.pack

#Joint dropdown
jointDropdown = ctk.CTkOptionMenu(form, values=bodyC.joints, command=bodyC.menuJoint, width=180, font=font1)
jointDropdown.place(x=15, y=90)
jointDropdown.set("")
jointDropdown.pack

#Movement dropdown
moveDropdown = ctk.CTkOptionMenu(form, values=bodyC.move, command=bodyC.menuMove, width=180, font=font1)
moveDropdown.place(x=215, y=90)
moveDropdown.set("")
moveDropdown.pack

#Excel save button
buttonExcel = ctk.CTkButton(form, text="Save Cycles", command=bodyC.writeExcel, font=font1)
buttonExcel.place(x=290, y=260)
buttonExcel.pack

#EMG data browser
entryEMG = ctk.CTkEntry(form, width=380, height=25, font=font1)
entryEMG.place(x=15, y=150)
entryEMG.pack

#Browse button for EMG data
buttonBrowseEmg = ctk.CTkButton(form, text="Browse", command=bodyC.browseFunc2, width=100, font=font1)
buttonBrowseEmg.place(x=425, y=150)
buttonBrowseEmg.pack

#EMG plot button
buttonEMG = ctk.CTkButton(form, text="EMG", command=body.emg, width=50, font=font1)
buttonEMG.place(x=535, y=150)
buttonEMG.pack

form.mainloop()