#tkinter setup
import tkinter as tk
from tkinter import ttk

#creating the window
root = tk.Tk()
root.geometry('700x700')
root.title('Calculator')
root.configure(bg="#0f4761")

#defining the global lists
temp_initial = []
temp1 = []
 
        
#defining the numbers as strings for comparison with variables to avoid errors
nums = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
#defining mode types and their base value, then the procedure for switching the mode. Replaces/adds/removes buttons when they are associated with a mode.
anglemode = "radians"
def change_anglemode():
    global anglemode
    if anglemode == "radians":
        anglemode = "degrees"
        degrees_mode_button.place_forget()
        angle_mode_button.place(x=302, y=235)
        print("set anglemode to degrees")
    else:
        anglemode = "radians"
        angle_mode_button.place_forget()
        degrees_mode_button.place(x=302, y=235)
        print("set anglemode to radians")
        
complex_mode = "real"
def change_complexmode():
    global complex_mode
    if complex_mode == "complex":
        complex_mode = "real"
        i_button.place_forget()
        real_mode_button.place_forget()
        complex_mode_button.place(x=70, y=235)
    else:
        complex_mode = "complex"
        i_button.place(x=70, y=235)
        complex_mode_button.place_forget()
        real_mode_button.place(x=160, y=235)
        

input_mode = "standard"
#defining possible inputs
correct = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "x", "/", "X^n", "e", "pi", "i", "+", "-", "(", ")", "sin", "cos", "tan"]
e = 2.71828
pi = 3.14159265359
j = (-1) ** 0.5
print(j)
comp = ["solve_quad", "solve_cube", "indef_integ", "def_integ", "differentiate", "clear", "ent", "switch_real", "switch_complex", "switch deg", "switch_rad"]
calculus = ("x", "/", "X^n", "+", "-")


#creating a procedure to put together adjacent number inputs as one number.
def compress_nums(list1):
    if len(list1) > 1 and type(list1[-1]) == int and type(list1[-2]) == int:
        list1[-2] = list1[-2] * 10 + list1[-1]
        list1.pop(-1)

#function checks if there are any standard procedure symbols in the wrong place
def symbol_validate(list1):
    mult = True
    print(list1)
    if list1[-1] == "/" or list1[-1] == "x" or list1[-1] == "+" or list1[-1] == "-" or list1[-1] == "(":
        print("something where it shouldn't be")
        mult = False
        print(list1)
    else:
        for i in range(len(list1)):
            if list1[i] == "/" or list1[i] == "+" or list1[i] == "x" or list1[i] == "X^n":
                if type(list1[i-1]) != int and type(list1[i-1]) != float and type(list1[i-1]) != complex and list1[i-1] != ")":
                    print(list1[i], "+/1 where it shouldnt be")
                    mult = False
                elif type(list1[i+1]) != int and type(list1[i+1]) != float and type(list1[i+1]) != complex and list1[i + 1] != "(":
                    print(list1[i], "+/2 where it shouldnt be")
                    mult = False
                elif list1[i] == "/" and list1[i + 1] == 0:
                    print("divide by zero error")
                    mult = False
            elif list1[i] == "-" and type(list1[i + 1]) != int and type(list1[i + 1]) != float and type(list1[i+1]) != complex and list1[i + 1] != "(":
                print("bad -")
                mult = False
    return mult

#procedure to turn numbers negative when after a - after another symbol
def make_negative(list1):
    for i in range(len(list1)):
        if len(list1) > i + 1 and list1[i - 1] != ")":
            if list1[i] == "-" and type(list1[i + 1]) != int and type(list1[i + 1]) != float and type(list1[i+1]) != complex:
                    print("bad -, clearing inputs1")
                    clear()
            elif len(list1) > i + 2 and type(list1[i]) == str and list1[i + 1] == "-":
                print("making negative")
                list1[i + 2] = -1 * float(list1[i + 2])
                list1.pop(i +1)
            else:
                print("nope", i)
            
#procedure to get rid of brackets where only a number is in it
def less_brackets(list1):
    print("less bracket", list1)
    for i in range(len(list1)):
        if len(list1) -1 > i and list1[i] == "(" and list1[i + 1] == ")":
            list1.pop(i)
            list1.pop(i)
        elif len(list1) -1 > i + 1 and list1[i] == "(" and (type(list1[i + 1]) == int or type(list1[i + 1]) == float) and list1[i + 2] == ")":
            if i > 0 and list1[i-1] == "sin":
                list1[i-1] = sin(list1[i+1])
                list1.pop(i+2)
                list1.pop(i+1)
                list1.pop(i)
                print("sin on ", list1)
            elif i > 0 and list1[i-1] == "cos":
                list1[i-1] = cos(list1[i+1])
                for i in range(3):
                    list1.pop()
            elif i > 0 and list1[i-1] == "tan":
                list1[i-1] = tan(list1[i+1])
                for i in range(3):
                    list1.pop()
            else:
                list1.pop(i)
                list1.pop(i + 1)

#checks there are the same number of open brackets as closed brackets
def bracket_validate(list1):
    openb = 0
    closedb = 0
    for i in range(len(list1)):
        if list1[i] == "(":
            openb += 1
            print(openb, "o")
        elif list1[i] == ")":
            closedb += 1
            print(closedb, "c")
    if openb!= closedb:
        print("too many of one type of bracket, clearing inputs")
        clear()
    return openb

#for non-calculus lists. Will resolve X^n to become 1 number
def resolve_power(list1):
        for i in range(len(list1)):
            if i + 2 < len(list1) and list1[i + 1] == "X^n" and type(list1[i]) in (int, float) and type(list1[i + 2]) in (int, float):
                list1[i] = list1[i] ** list1[i + 2]
                list1.pop(i + 1)
                list1.pop(i + 1)

#alternate list creation to make_list that allows for calculus to be done on it, does not do resolve_power
def make_calculus_list(list1):
    global e, pi, i, temp1
    terminal1 = [0]
    temp1 = [0]
    for i in range(len(list1)):
        next_element1 = str(list1[i])
        if next_element1 in nums:
            terminal1.append(int(next_element1))
            temp1.append(int(next_element1))
            compress_nums(temp1)
            compress_nums(terminal1)
        elif next_element1 == "e":
            temp1.append(e)
            terminal1.append("e")
        elif next_element1 == "pi":
            temp1.append(pi)
            terminal1.append("pi")
        elif next_element1 == "i":
            temp1.append(j)
            terminal1.append("i")
        elif next_element1 in calculus:
            terminal1.append(next_element1)
            temp1.append(next_element1)       
        else:
            print("nuh uh")
        make_negative(temp1)
        print(terminal1)
        print(temp1)
    make_negative(temp1)
    symbol_validate(temp1)
    return temp1

#finding x values when y = 0 of quadratic expressions
def solve_quadratic(list1):
    global out
    print("ax^2 + bx + c")
    print(list1)
    if a_digs == 1:
        a1 = int(list1[3])
    if a_digs == 2:
        a1 = int(list1[3])
        a2 = int(list1[4])
        a1 = a1 * 10 + a2
    elif a_digs == 3:
        a1 = int(list1[3])
        a2 = list1[4]
        a3 = int(list1[5])
        if a2 == "/":
            a1 = a1 / a3
        else:
            a1 = (a1 * 10 + int(a2)) * 10 + a3
    for i in range(a_digs):
        list1.pop(2 + a_digs)
    print(list1)
    if b_digs == 1:
        b1 = int(list1[3])
    elif b_digs == 2:
        b1 = int(list1[3])
        b2 = int(list1[4])
        b1 = b1 * 10 + b2
    else:
        b1 = int(list1[3])
        b2 = list1[4]
        b3 = int(list1[5])
        if b2 == "/":
            b1 = b1 / b3
        else:
            b1 = (b1 * 10 + int(b2)) * 10 + b3
    for i in range(b_digs):
        list1.pop(2 + b_digs)
    print(list1)
    if c_digs == 1:
        c1 = int(list1[3])
    elif c_digs == 2:
        c1 = int(list1[3])
        c2 = int(list1[4])
        c1 = c1 * 10 + c2
    else:
        c1 = int(list1[3])
        c2 = list1[4]
        c3 = int(list1[5])
        if c2 == "/":
            c1 = c1 / c3
        else:
            c1 = (c1 * 10 + int(c2)) * 10 + c3
    solved1 = (b1 * -1 + ((b1 ** 2 - 4 * a1 * c1) ** 0.5)) / (2 * a1)
    print(solved1)
    solved2 = (b1 * -1 - ((b1 ** 2 - 4 * a1 * c1) ** 0.5)) / (2 * a1)
    print(solved2)
    if complex_mode == "complex":
        solved = ("x = " + str(solved1) + " x = " + str(solved2))
    else:
        if type(solved1) == complex and type(solved2) == complex:
            solved = "no real solutions"
        elif type(solved1) == complex:
            solved = ("x = " + str(solved2))
        elif type(solved2) == complex:
            solved = ("x = " + str(solved1))
        else:
            solved = ("x = " + str(solved1) + " x = " + str(solved2))            
    out.set(solved)

#same for cubic expressions
def solve_cubic(list1):
    global out
    print("ax^3 + bx^2 + cx + d")
    print(list1)
    if a_digs == 1:
        a1 = int(list1[4])
    if a_digs == 2:
        a1 = int(list1[4])
        a2 = int(list1[5])
        a1 = a1 * 10 + a2
    elif a_digs == 3:
        a1 = int(list1[4])
        a2 = list1[5]
        a3 = int(list1[6])
        if a2 == "/":
            a1 = a1 / a3
        else:
            a1 = (a1 * 10 + int(a2)) * 10 + a3
    for i in range(a_digs):
        list1.pop(3 + a_digs)
    print(list1)
    if b_digs == 1:
        b1 = int(list1[4])
    elif b_digs == 2:
        b1 = int(list1[4])
        b2 = int(list1[5])
        b1 = b1 * 10 + b2
    else:
        b1 = int(list1[4])
        b2 = list1[5]
        b3 = int(list1[6])
        if b2 == "/":
            b1 = b1 / b3
        else:
            b1 = (b1 * 10 + int(b2)) * 10 + b3
    for i in range(b_digs):
        list1.pop(3 + b_digs)
    print(list1)
    if c_digs == 1:
        c1 = int(list1[4])
    elif c_digs == 2:
        c1 = int(list1[4])
        c2 = int(list1[5])
        c1 = c1 * 10 + c2
    else:
        c1 = int(list1[4])
        c2 = list1[5]
        c3 = int(list1[6])
        if c2 == "/":
            c1 = c1 / c3
        else:
            c1 = (c1 * 10 + int(c2)) * 10 + c3
    for i in range(c_digs):
        list1.pop(3 + c_digs)
    if d_digs == 1:
        d1 = int(list1[4])
    elif d_digs == 2:
        d1 = int(list1[4])
        d2 = int(list1[5])
        d1 = d1 * 10 + d2
    else:
        d1 = int(list1[4])
        d2 = list1[5]
        d3 = int(list1[6])
        if d2 == "/":
            d1 = d1 / d3
        else:
            d1 = (d1 * 10 + int(d2)) * 10 + d3
    p = (3 * a1 * c1 - b1 ** 2) / (3 * (a1 ** 2))
    q = (2 * (b1 ** 3) - 9 * a1 * b1 * c1 + 27 * (a1 ** 2) * d1) / (27 * (a1 ** 3))
    solved1 = ((q * -1 * 0.5 + ((q ** 2) * 0.25 + (p ** 3) / 27) ** 0.5) ** (1 / 3)) + ((-1 * (q * 0.5) - ((q ** 2) / 4 + (p ** 3) / 27) ** 0.5) ** (1 / 3)) - b1 / (3 * a1)
    solved2 = (e ** (2 * pi * j / 3)) * ((q * -1 * 0.5 + ((q ** 2) * 0.25 + (p ** 3) / 27) ** 0.5) ** (1 / 3)) + (e ** (4 * pi * j / 3)) * ((-1 * (q * 0.5) - ((q ** 2) / 4 + (p ** 3) / 27) ** 0.5) ** (1 / 3)) - b1 / (3 * a1)
    solved3 = (e ** (4 * pi * j / 3)) * ((q * -1 * 0.5 + ((q ** 2) * 0.25 + (p ** 3) / 27) ** 0.5) ** (1 / 3)) + (e ** (2 * pi * j / 3)) * ((-1 * (q * 0.5) - ((q ** 2) / 4 + (p ** 3) / 27) ** 0.5) ** (1 / 3)) - b1 / (3 * a1)
    if complex_mode == "complex":
        solved = ("x = " + str(solved1) + " x = " + str(solved2) + " x = " + str(solved3))
    else:
        if type(solved1) == complex and type(solved2) == complex and type(solved3) == complex:
            solved = "no real solutions"
        elif type(solved1) == complex and type(solved2) == complex:
            solved = ("x = " + str(solved3))
        elif type(solved1) == complex and type(solved3) == complex:
            solved = ("x = " + str(solved2))
        elif type(solved1) == complex:
            solved = ("x = " + str(solved2) + " x = " + str(solved3))
        elif type(solved2) == complex and type(solved3) == complex:
            solved = ("x = " + str(solved1))
        elif type(solved2) == complex:
            solved = ("x = " + str(solved1) + " x = " + str(solved3))
        elif type(solved3) == complex:
            solved = ("x = " + str(solved1) + " x = " + str(solved2))
        else:
            solved = ("x = " + str(solved1) + " x = " + str(solved2) + " x = " + str(solved3))            
    out.set(solved)
    
#making the list of inputs to be shown on the terminal and a copy to be used in calculations to generate an output
def make_list(list1):
    global temp1
    terminal = []
    print(terminal)
    print(temp1)
    for i in range(len(list1)):
        next_element = str(list1[i])
        if next_element in nums:
            terminal.append(int(next_element))
            temp1.append(int(next_element))
            compress_nums(temp1)
            compress_nums(terminal)
        elif next_element == "e":
            temp1.append(e)
            terminal.append("e")
        elif next_element == "pi":
            temp1.append(pi)
            terminal.append("pi")
        elif next_element == "i":
            temp1.append(j)
            terminal.append("i")
        elif next_element == "sin":
            temp1.append("sin")
            terminal.append("sin")
        elif next_element == "cos":
            temp1.append("cos")
            terminal.append("cos")
        elif next_element == "tan":
            temp1.append("tan")
            terminal.append("tan")        
        elif next_element in correct:
            terminal.append(next_element)
            temp1.append(next_element)
            compress_nums(temp1)
            compress_nums(terminal)
        elif next_element[0] in nums:
            terminal.append(float(next_element))
            temp1.append(float(next_element))            
        else:
            print("invalid input")
        print(temp1)
        less_brackets(temp1)
        make_negative(temp1)
        resolve_power(temp1)
        print(temp1)
        print(terminal)
    return temp1


#does basic calculations within brackets to make them 1 number so less_brackets can eventually get things down to having no brackets       
def resolve_bracket(list1):
    count = 0
    closed = None
    while count < len(list1):
        if list1[count] == ")":
            closed = count
            break
        count += 1
    if closed == None:
        return
    count = closed
    opened = None
    while count >= 0:
        if list1[count] == "(":
            opened = count
            break
        count -= 1
    if opened == None:
        return
    i = opened + 1
    while i < closed:
        if list1[i] == "/":
            if type(list1[i - 1]) in (int, float) and type(list1[i + 1]) in (int, float):
                list1[i - 1] = list1[i - 1] / list1[i + 1]
                list1.pop(i)
                list1.pop(i)
                closed -= 2
                i -= 1
        elif list1[i] == "x":
            if type(list1[i - 1]) in (int, float) and type(list1[i + 1]) in (int, float):
                list1[i - 1] = list1[i - 1] * list1[i + 1]
                list1.pop(i)
                list1.pop(i)
                closed -= 2
                i -= 1            
        i += 1
    i = opened + 1
    while i < closed:
        if list1[i] == "+":
            if type(list1[i - 1]) in (int, float) and type(list1[i + 1]) in (int, float):
                list1[i - 1] = list1[i - 1] + list1[i + 1]
                list1.pop(i)
                list1.pop(i)
                closed -= 2
                i -= 1
        elif list1[i] == "-":
            if type(list1[i - 1]) in (int, float) and type(list1[i + 1]) in (int, float):
                list1[i - 1] = list1[i - 1] - list1[i + 1]
                list1.pop(i)
                list1.pop(i)
                closed -= 2
                i -= 1
        i += 1

    list1.pop(closed)
    list1.pop(opened)

#has make_list or make_calculus_list passed into it to run all relevant calculations on the lists created to generate the final value to be displayed on the terminal
def out_from_made_list(func, inp_mode):
    global diff, inte, temp_initial, temp1, upper, lower, definite1
    print("definite1 = ", definite1, " upper = ", upper, " and lower = ", lower)
    print(func)
    #clear the inputs if they do not make a usable equation
    if inp_mode == "diff":
        diff = True
        inte = False
    elif inp_mode == "inte":
        diff = False
        inte = True
    else:
        diff = False
        inte = False
    temp = func
    bracket_validate(temp)
    worked = True
    if symbol_validate(temp) == False:
                print("no work, clearing inputs")
                clear()
                worked = False
                out.set("maths error")

    if worked == True:
        #resolves all brackets in non-calculus calculations
        if diff == False and inte == False:
            for t in range(bracket_validate(temp)):
                print("resolving bracket set", t)
                resolve_bracket(temp)
                print(temp)

        #performs differentiation on expressions within calculus_list
        elif diff == True:
            print("diff")
            for i in range(len(temp) - 1):
                if temp[i] == "X^n":
                    temp[i - 1] = temp[i - 1] * temp[i + 1]
                    temp[i + 1] -= 1
            if len(temp) > 1 and temp[-2] != "X^n":
                temp.pop(-1)
                temp.pop(-1)

        #performs integration on expressions within calculus_list
        elif inte == True:
            print("inte")
            for i in range(len(temp)):
                if temp[i] == "X^n" and temp[i + 1] != -1:
                    temp[i + 1] += 1
                    temp[i - 1] /= temp[i + 1]
                elif temp[i] == "X^n" and temp[i + 1] == -1:
                    print("idk, ln smth")
            if len(temp) > 2 and temp[-2] != "X^n":
                temp.append("X^n")
                temp.append(1)

            print(temp)
            if definite1 == True:
                print("definite integration")
                if upper == "pi":
                    upper = pi
                elif upper == "e":
                    upper = e
                elif upper == "i":
                    upper = i
                else:
                    upper = float(upper)
                if lower == "pi":
                    lower = pi
                elif lower == "e":
                    lower = e
                elif lower == "i":
                    lower = i
                else:
                    lower = float(lower)
                uppertotal = 0
                lowertotal = 0
                for i in range(len(temp)):
                    if len(temp) > i + 1 and temp[i + 1] == "X^n":
                        print(temp[i])
                        uppertotal += ((upper ** temp[i + 2]) * temp[i])
                        print(uppertotal)
                        lowertotal += ((lower ** temp[i + 2]) * temp[i])
                        print(lowertotal)
                total = uppertotal - lowertotal
                temp = [total]

        #basic calculations done on what remains
        i = 0
        divs = False
        while len(temp) > i + 1:
            if temp[i + 1] == "/":
                temp[i] = temp[i] / temp[i + 2]
                temp.pop(i + 1)
                temp.pop(i + 1)
            elif temp[i + 1] == "x":
                temp[i] = temp[i] * temp[i + 2]
                temp.pop(i + 1)
                temp.pop(i + 1)
            else:
                i += 1
        i = 0
        if diff == True or (inte == True and definite1 == False): 
            while len(temp) > i + 3:
                if temp[i + 1] == "+" and temp[i + 3] != "X^n":
                    temp[i] = temp[i] + temp[i + 2]
                    temp.pop(i + 1)
                    temp.pop(i + 1)
                elif temp[i + 1] == "-" and temp[i + 3] != "X^n":
                    temp[i] = temp[i] - temp[i + 2]
                    temp.pop(i + 1)
                    temp.pop(i + 1)
                else:
                    i += 1

        else:
            while len(temp) > i + 1:
                if temp[i + 1] == "+":
                    temp[i] = temp[i] + temp[i + 2]
                    temp.pop(i + 1)
                    temp.pop(i + 1)
                elif temp[i + 1] == "-":
                    temp[i] = temp[i] - temp[i + 2]
                    temp.pop(i + 1)
                    temp.pop(i + 1)
                else:
                    i += 1
            
        if inte == True and definite1 == False:
            temp.append("+c")

        terminal = temp
        print(temp)
        out.set(terminal)
        temp = []

        #generates an output value for the calculator terminal by cleaning up the expression into something easily readable 
        output_value = ""
        for i in range(len(terminal)):
            if terminal[i] == "X^n":
                terminal[i] = "X^"
            elif type(terminal[i]) == complex:
                if abs(terminal[i].real) < 0.00001:
                    terminal[i] = str(terminal[i].imag) + "i"
                elif abs(terminal[i].imag) < 0.00001:
                    terminal[i] = str(terminal[i].real)        
                else:
                    terminal[i] = (str(terminal[i].imag) + "i + " + str(terminal[i].real))
            output_value += str(terminal[i])
        print(output_value)
        out.set(output_value)
        temp1 = []
        temp_initial = [output_value]
        return(output_value)




#creating the calculator terminal
out = tk.StringVar()
out.set("0")
terminal_entry = tk.Entry(root, justify="right", textvariable=out, font=("Arial", 20))
terminal_entry.place(x=10, y=30, width=680, height=100)

#setting relevant global variables for button_clicked
definite1 = False
upper = None
lower = None
solve_type = None
a_digs = None
b_digs = None
c_digs = None
d_digs = None
donea = 0
doneb = 0
donec = 0
doned = 0
#command linked to most buttons, upon a button click, it will decide based on input_mode whether to continue through standard calculations, calculus, or solving polynomials
def button_clicked(value):
    global temp_initial, out, solve_type, donea, doneb, donec, doned, a_digs, b_digs, c_digs, d_digs, upper, lower, definite1
    print(input_mode)
    if input_mode == "standard":
        if value != "enter" and value != "del":
            if value == "÷":
                temp_initial.append("/")
            else:
                temp_initial.append(value)
            print(temp_initial)
        if value == "X^n":
            value = "^"
        if (type(value) == int or value == "e" or value ==  "i" or value == "pi" or value == "sin" or value == "cos" or value == "tan") and (out.get() == "0" or out.get() == "oi" or out.get() == "quadratic(1) or cubic(2)?"):
            if value == "pi":
                value = "π"
            out.set(str(value))
            if value == "π":
                value = "pi"
        elif value == "enter":
            enter = True
            out_from_made_list(make_list(temp_initial), input_mode)
        elif value == "del":
            if len(temp_initial) > 1 or len(str(out.get())) > 1:
                if len(str(out.get())) > 1:
                    out.set("0")
                    print("lost old answer")
                else:
                    out2 = str(out.get())[:-1]
                    out.set(out2)
                    print("lost1")
                temp_initial.pop()
            elif len(str(out.get())) == 1 and len(temp_initial) > 0:
                temp_initial.pop()
                out.set("0")
                print("restarted")
        else:
            if value == "pi":
                value = "π"            
            out.set(str(out.get()) + str(value))
            if value == "π":
                value = "pi"
    elif input_mode == "diff":
        if value != "enter":
            if value == "÷":
                temp_initial.append("/")
            else:
                temp_initial.append(value)
            print(temp_initial)
        if value == "X^n":
            value = "X^"
        if (type(value) == int or value == "e" or value ==  "i" or value == "pi" or value == "sin" or value == "cos" or value == "tan") and (out.get() == "0" or out.get() == "oi" or out.get() == "quadratic(1) or cubic(2)?"):
            if value == "pi":
                value = "π"
            out.set(str(value))
            if value == "π":
                value = "pi"
        elif value == "enter":
            enter = True
            out_from_made_list(make_calculus_list(temp_initial), input_mode)
        else:
            out.set(str(out.get()) + str(value))
        print(temp_initial)
    elif input_mode == "inte":
        if out.get() == "definite(1) or indefinite(2)?":
            if value == 1:
                definite1 = True
                out.set("what is your upper x?")
            else:
                definite1 = False
                out.set(0)
        elif out.get() == "what is your upper x?":
            if str(value) in nums:
                upper = value
                out.set("what is your lower x?")
        elif out.get() == "what is your lower x?":
            lower = value
            out.set("0")
        else:        
            if value == "X^n":
                value = "X^"
            if (type(value) == int or value == "e" or value ==  "i" or value == "pi" or value == "sin" or value == "cos" or value == "tan") and (out.get() == "0" or out.get() == "oi" or out.get() == "quadratic(1) or cubic(2)?"):
                if value == "pi":
                    value = "π"
                out.set(str(value))
                if value == "π":
                    value = "pi"
                if value == "X^":
                    value = "X^n"
                temp_initial.append(value)
                print("appending")

            elif value == "enter":
                enter = True
                out_from_made_list(make_calculus_list(temp_initial), input_mode)
            else:
                if value == "X^":
                    value = "X^n"
                temp_initial.append(value)
                out.set(str(out.get()) + str(value))
                print("appending")
        print(temp_initial)
    elif input_mode == "solve":
        if out.get() == "quadratic(1) or cubic(2)?":
            if value == 1:
                solve_type = "quadratic"
            elif value == 2:
                solve_type = "cubic"
            out.set("how many digits of a? (up to 3)")
        elif out.get() == "how many digits of a? (up to 3)":
            out.set("how many digits of b? (up to 3)")
            a_digs = value
            temp_initial.append(value)
        elif out.get() == "how many digits of b? (up to 3)":
            out.set("how many digits of c? (up to 3)")
            b_digs = value
            temp_initial.append(value)
        elif out.get() == "how many digits of c? (up to 3)":
            if solve_type == "cubic":
                c_digs = value
                temp_initial.append(value)
                out.set("how many digits of d? (up to 3)")
            else:
                c_digs = value
                temp_initial.append(value)
                out.set("what is your a?")
        elif out.get() == "how many digits of d? (up to 3)":
            d_digs = value
            temp_initial.append(value)
            out.set("what is your a?")
        elif out.get() == "what is your a?":
            if a_digs == 1 and donea < 1:
                temp_initial.append(value)
                donea += 1
                print("a1")
                print(temp_initial)
            elif a_digs == 2 and donea < 2:
                temp_initial.append(value)
                donea += 1
            elif a_digs == 3 and donea < 3:
                temp_initial.append(value)
                donea += 1
            if (a_digs == 1 and donea == 1) or (a_digs == 2 and donea == 2) or (a_digs == 3 and donea == 3):
                out.set("what is your b?")
        elif out.get() == "what is your b?":
            if b_digs == 1 and doneb < 1:
                temp_initial.append(value)
                doneb += 1
            elif b_digs == 2 and doneb < 2:
                temp_initial.append(value)
                doneb += 1
            elif b_digs == 3 and doneb < 3:
                temp_initial.append(value)
                doneb += 1
            if (b_digs == 1 and doneb == 1) or (b_digs == 2 and doneb == 2) or (b_digs == 3 and doneb == 3):
                out.set("what is your c?")
        elif out.get() == "what is your c?":
            if c_digs == 1 and donec < 1:
                temp_initial.append(value)
                donec += 1
            elif c_digs == 2 and donec < 2:
                temp_initial.append(value)
                donec += 1
            elif c_digs == 3 and donec < 3:
                temp_initial.append(value)
                donec += 1
            if (c_digs == 1 and donec == 1) or (c_digs == 2 and donec == 2) or (c_digs == 3 and donec == 3):
                if solve_type == "quadratic":
                    solve_quadratic(temp_initial)
                elif solve_type == "cubic":
                    out.set("what is your d?")
        elif out.get() == "what is your d?":
            if d_digs == 1 and doned < 1:
                temp_initial.append(value)
                doned += 1
            elif d_digs == 2 and doned < 2:
                temp_initial.append(value)
                doned += 1
            elif d_digs == 3 and doned < 3:
                temp_initial.append(value)
                doned += 1
            if (d_digs == 1 and doned == 1) or (d_digs == 2 and doned == 2) or (d_digs == 3 and doned == 3):
                solve_cubic(temp_initial)
    

#replaces the reuse of make_list, sets all global variables back to their original states
def clear():
    global temp_initial, a_digs, b_digs, c_digs_, d_digs, donea, doneb, donec, doned, input_mode, terminal, temp, terminal1, temp1
    input_mode = "standard"
    temp_initial = []
    terminal = [0]
    temp = []
    temp1 = []
    terminal1 = [0]
    a_digs = 0
    b_digs = 0
    c_digs = 0
    d_digs = 0
    donea = 0
    doneb = 0
    donec = 0
    doned = 0
    global out
    out.set(0)

#resets input_mode without need for clearing    
def enter():
    global input_mode
    input_mode = "standard"



#recursive for use in trig functions
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n-1)

#trig functions using taylor series to generate a good approximation.    
def sin(num1):
    answer = 0
    num2 = 0
    pied = False
    coeff = False
    if type(num1) == str:
        num1 = list(num1)
        for k in range(len(num1)):
            if len(num1) > k + 1 and str(num1[k]) == "p" and str(num1[k + 1]) == "i" and pied == False:
                print("this1")
                pied = True
                if k > 0:
                    coeff = True
                    c = k
        if pied == True and coeff == True:
            print("this2")
            coeff2 = False
            for i in range(c):
                if c - 1 - i >= 0 and num1[c - 1 - i].isdigit() and num1[c - i].isdigit():
                    num1[c - i] = int(num1[c - i]) * 10 + int(num1[c - 1 - i])
                elif c > i + 1 and num1[i + 1] == "/":
                    print("this4")
                    j = i + 2
                    den = 0
                    while j < c and num1[j].isdigit():
                        den = den * 10 + int(num1[j])
                        j += 1

                    coeff1 = int(num1[i]) / den
                    coeff2 = True
                elif c > i and isinstance(num1[i], int) and isinstance(num1[i + 1], int):
                    print("this5")
                    num1[i] = int(num1[i]) * 10 + int(num1[i + 1])
                    num1.pop(i + 1)
            if coeff2 == True:
                num3 = coeff1 * pi
            else:
                num3 = int(num1[0]) * pi
        elif pied == True:
            num3 = pi
    else:
        num3 = float(num1)
    if anglemode == "degrees":
        num3 = num3 * pi / 180
    num3 = ((num3 + pi) % (2 * pi)) - pi
    for i in range(50):
        if i % 2 == 0:
            answer += (num3 ** (2 * i + 1)) / factorial(2 * i + 1)
        else:
            answer -= (num3 ** (2 * i + 1)) / factorial(2 * i + 1)            
    print(answer)
    return(answer)

def cos(num1):
    answer = 0
    num2 = 0
    pied = False
    coeff = False
    if type(num1) == str:
        num1 = list(num1)
        for k in range(len(num1)):
            if len(num1) > k + 1 and str(num1[k]) == "p" and str(num1[k + 1]) == "i" and pied == False:
                print("this1")
                pied = True
                if k > 0:
                    coeff = True
                    c = k
        if pied == True and coeff == True:
            print("this2")
            coeff2 = False
            for i in range(c):
                if c - 1 - i >= 0 and num1[c - 1 - i].isdigit() and num1[c - i].isdigit():
                    num1[c - i] = int(num1[c - i]) * 10 + int(num1[c - 1 - i])
                elif c > i + 1 and num1[i + 1] == "/":
                    print("this4")
                    j = i + 2
                    den = 0
                    while j < c and num1[j].isdigit():
                        den = den * 10 + int(num1[j])
                        j += 1

                    coeff1 = int(num1[i]) / den
                    coeff2 = True
                elif c > i and isinstance(num1[i], int) and isinstance(num1[i + 1], int):
                    print("this5")
                    num1[i] = int(num1[i]) * 10 + int(num1[i + 1])
                    num1.pop(i + 1)
            if coeff2 == True:
                num3 = coeff1 * pi
            else:
                num3 = int(num1[0]) * pi
        elif pied == True:
            num3 = pi
    else:
        num3 = float(num1)
    if anglemode == "degrees":
        num3 = num3 * pi / 180
    num3 = ((num3 + pi) % (2 * pi)) - pi
    for i in range(50):
        if i % 2 == 0:
            answer += (num3 ** (2 * i)) / factorial(2 * i)
        else:
            answer -= (num3 ** (2 * i)) / factorial(2 * i)            
    print(answer)
    return(answer)

#using the trig identity instead of the taylor series here as it is far simpler
def tan(num1):
    answer = sin(num1) / cos(num1)
    return answer

#starts the intergration process
def integrate():
    global input_mode, terminal_initial, out
    input_mode = "inte"
    temp = [0]
    out.set("definite(1) or indefinite(2)?")
    print(input_mode)

#starts the differentiation process
def differentiate():
    global input_mode, temp_initial, out
    input_mode = "diff"
    temp_initial = [0]
    out.set(0)
    print(input_mode)

#starts the solving process
def solve():
    global input_mode
    input_mode = "solve"
    global temp_initial
    temp_initial = []
    out.set("quadratic(1) or cubic(2)?")

#easter egg
def printoi():
    print("oi")
    out.set("oi")

#number buttons
one_button = tk.Button(root, text="1", command = lambda: button_clicked(1), width = 6, height = 3, bg="#A0A0A0")
one_button.place(x=500, y=300)
two_button = tk.Button(root, text="2", command = lambda: button_clicked(2), width = 6, height = 3, bg="#A0A0A0")
two_button.place(x=565, y=300)
three_button = tk.Button(root, text="3", command = lambda: button_clicked(3), width = 6, height = 3, bg="#A0A0A0")
three_button.place(x=630, y=300)
four_button = tk.Button(root, text="4", command = lambda: button_clicked(4), width = 6, height = 3, bg="#A0A0A0")
four_button.place(x=500, y=365)
five_button = tk.Button(root, text="5", command = lambda: button_clicked(5), width = 6, height = 3, bg="#A0A0A0")
five_button.place(x=565, y=365)
six_button = tk.Button(root, text="6", command = lambda: button_clicked(6), width = 6, height = 3, bg="#A0A0A0")
six_button.place(x=630, y=365)
seven_button = tk.Button(root, text="7", command = lambda: button_clicked(7), width = 6, height = 3, bg="#A0A0A0")
seven_button.place(x=500, y=430)
eight_button = tk.Button(root, text="8", command = lambda: button_clicked(8), width = 6, height = 3, bg="#A0A0A0")
eight_button.place(x=565, y=430)
nine_button = tk.Button(root, text="9", command = lambda: button_clicked(9), width = 6, height = 3, bg="#A0A0A0")
nine_button.place(x=630, y=430)
zero_button = tk.Button(root, text="0", command = lambda: button_clicked(0), width = 6, height = 3, bg="#A0A0A0")
zero_button.place(x=500, y=495)

#other buttons
clear_button = tk.Button(root, text="clear", command = clear, width = 11, height = 3, bg="#990000")
clear_button.place(x=500, y=235)
del_button = tk.Button(root, text="del", command = lambda: button_clicked("del"), width = 11, height = 3, bg="#990000")
del_button.place(x=595, y=235)
enter_button = tk.Button(root, text="enter", command =lambda: button_clicked("enter") , width = 15, height = 3, bg="#990000")
enter_button.place(x=566, y=495)
complex_mode_button = tk.Button(root, text="Complex", command = change_complexmode, width = 30, height = 3, bg="#3399FF")
complex_mode_button.place(x=70, y=235)
real_mode_button = tk.Button(root, text="Real", command = change_complexmode, width = 17, height = 3, bg="#3399FF")
i_button = tk.Button(root, text="i", command = lambda: button_clicked("i"), width = 10, height = 3, bg="#660099")
angle_mode_button = tk.Button(root, text="Radians", command = change_anglemode, width = 18, height = 3, bg="#3399FF")
degrees_mode_button = tk.Button(root, text="Degrees", command = change_anglemode, width = 18, height = 3, bg="#3399FF")
degrees_mode_button.place(x=302, y=235)
sin_button = tk.Button(root, text="Sin", command = lambda: button_clicked("sin"), width = 12, height = 3, bg="#008800")
sin_button.place(x=70, y=300)
cos_button = tk.Button(root, text="Cos", command = lambda: button_clicked("cos"), width = 12, height = 3, bg="#008800")
cos_button.place(x=175, y=300)
tan_button = tk.Button(root, text="Tan", command = lambda: button_clicked("tan"), width = 12, height = 3, bg="#008800")
tan_button.place(x=280, y=300)
open_button = tk.Button(root, text="(", command = lambda: button_clicked("("), width = 6, height = 3, bg="#FF8000")
open_button.place(x=385, y=300)
e_button = tk.Button(root, text="e", command = lambda: button_clicked("e"), width = 10, height = 3, bg="#660099")
e_button.place(x=70, y=365)
pi_button = tk.Button(root, text="π", command = lambda: button_clicked("pi"), width = 10, height = 3, bg = "#660099")
pi_button.place(x=162, y=365)
plus_button = tk.Button(root, text="+", command = lambda: button_clicked("+"), width = 6, height = 3, bg="#FF8000")
plus_button.place(x=255, y=365)
minus_button = tk.Button(root, text="-", command = lambda: button_clicked("-"), width = 6, height = 3, bg="#FF8000")
minus_button.place(x=320, y=365)
close_button = tk.Button(root, text=")", command = lambda: button_clicked(")"), width = 6, height = 3, bg="#FF8000")
close_button.place(x=385, y=365)
solve_button = tk.Button(root, text="Solve", command = solve, width = 18, height = 3, bg="#FFFFCC")
solve_button.place(x=70, y=430)
xn_button = tk.Button(root, text="X^n", command = lambda: button_clicked("X^n"), width = 11, height = 3, bg="#FF8000")
xn_button.place(x=218, y=430)
x_button = tk.Button(root, text="x", command = lambda: button_clicked("x"), width = 6, height = 3, bg="#FF8000")
x_button.place(x=320, y=430)
divide_button = tk.Button(root, text="÷", command = lambda: button_clicked("÷"), width = 6, height = 3, bg="#FF8000")
divide_button.place(x=385, y=430)
inte_button = tk.Button(root, text="Integrate", command = integrate, width = 24, height = 3, bg="#FFFF00")
inte_button.place(x=70, y=495)
diff_button = tk.Button(root, text="Differentiate", command = differentiate, width = 24, height = 3, bg="#FFFF00")
diff_button.place(x=260, y=495)
egg_button = tk.Button(root, text="Don't do it", command = printoi, width = 24, height = 2, bg="#0f4761")
egg_button.place(x=0, y = 660)

#tkinter procedure that lets it create and refresh the UI                
root.mainloop()
