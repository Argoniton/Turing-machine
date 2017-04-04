
##  Turing Machine Visual - a software developed to simulate Turing machine
##    Copyright (C) 2017 Artemii Yanushevskyi
##
##    This program is free software: you can redistribute it and/or modify
##    it under the terms of the GNU Affero General Public License as
##    published by the Free Software Foundation, either version 3 of the
##    License, or (at your option) any later version.
##
##    This program is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU Affero General Public License for more details.
##
##    You should have received a copy of the GNU Affero General Public License
##    along with this program.  If not, see <http://www.gnu.org/licenses/>.
##
##    You can contact me by email: argoniton@gmail.com
##
##  This is BETA 6 of this application.

# clear and consice
import tkinter as tk
from Utilities import sign, compile_turing_code, open_file
canvas_width = 420 # size of canvas area

class TuringMachine(tk.Frame):
    ''' visualize machine + controls'''
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        # visualize machine
        self.machine = Machine(self, 'white', width=canvas_width, height=210, bd=0, highlightthickness=0)
        self.machine.pack()
        
        # controls
        self._make_controls()

    def _make_controls(self):
        ''' creates labels, buttons etc'''
        b = tk.Button(self, text='Act!',
                      command=self.machine.create_and_act)
        b.pack(side='right')
        leftButton = tk.Button(self, text='Turn Left',
                      command=self.machine.stripe.L)
        leftButton.pack(side='left')
        rightButton = tk.Button(self, text='Turn Right',
                      command=self.machine.stripe.R)
        rightButton.pack(side='right')
        

class Machine(tk.Canvas):
    def __init__(self, top, linecolor, *args, **kwargs):
        tk.Canvas.__init__(self, top, *args, **kwargs)
        
        self.stripe = Stripe(self) # making a stripe
        
        # make a smart variable moved and acting
        self.moving = tk.IntVar()
        self.moving.set(0) # set it equal to 1, '1' means that it is moving
        self.running = tk.IntVar()
        self.running.set(0) # program doesn't run if it's '1'
        # now sti in not moving nor running
        # no action is allowed while stripe is moving
        # and we need to wait while prorgam is running

        self.values = None
        
        self.codepath = None # stores code path        
        self.compiled = None # stores compiled code
        
        self.state = 'q1' # machine.state at the beginning
        # display self.state under stripe
        self.stateT = self.create_text(210, 164, text=self.state,
                                       tag='machineState',
                                       fill='gray',
                                       activefill='darkgray')

    def act(self):
        '''act untill stop'''
        self.running.set(1)
        
        work = True
        while work:
            work = self._action()
        
        self.running.set(0)
        print('Done')
        
    def open(self, source):
        '''open and compile code'''
        self.compiled = compile_turing_code(source)

    def _action(self):
        '''make a single move'''
        work = True
        # 210, 170
        # obtain new values
        action = self.compiled[(self.state, self.stripe.current.value)]
        # 'unpack action'
        self.state = action[0]
        value = action[1]
        move = action[2]        
        self.itemconfig(self.stateT, text=self.state) # display new state
        self.stripe.valueChange(value) # change a value of current place
        # what to do next:
        if move == 'L' or move == 'l':
            self.stripe.L()
        elif move == 'R' or move == 'r':
            self.stripe.R()
        elif move == 'S' or move == 's':
            self.stripe.S()
            print('machine has stopped')
            work = False
        else:
            print('error executing', move, 'move doesn\'t exist')
            work = False
        return work

    def create_and_act(self):
        # provide input values
        self.values = '3 4'
        self.codepath = '/Users/argoniton/Desktop/addtiton of 2 numbers.turing'

        print(self.running.get())
        if not self.running.get():
            self.stripe.createstripe(self.values) # fill the stripe with numbers in array
            # open and compile code
            if not self.codepath:
                appname = open_file()
                self.open(appname)
                print(appname)
            else:
                if not self.compiled:
                    self.open(self.codepath)                   
        # run machine
        self.act()


class Stripe:
    def __init__(self, machine):
        self.machine = machine
        self.current = None
        self.animate = False

    def valueChange(self, value):
        self.current.value = value
        rect_id = self.current.visual[0]
        text_id = self.current.visual[1]
        self.machine.itemconfig(text_id, text=str(value))
        self.machine.itemconfig(rect_id, fill='darkgray')
        
    def makePlaceAtCenter(self, value):
        returnPlace1 = self.machine.create_rectangle(175,70,245,140, fill='gray', tag='place'),                    
        returnPlace2 = self.machine.create_text(210, 105, text=str(value), tag='place')
        return returnPlace1, returnPlace2

    def createNewPlace(self, value):
        place = Place(self, value, None, None)

        self.current = place
        place.visual = self.makePlaceAtCenter(0)
        print('place has been made', place.value, place.left, place.right)
        
        return place

    def createNewPlaceR(self, value, left):
        place = Place(self, value, left, None)
        if left == None:
            place.visual = self.makePlaceAtCenter(value)
        else:
            left.right = place
            place.visual = self.makePlaceAtCenter(value)
        self.current = place
        #print('place has been made',place.value, place.left, place.right)
        return place

    def createNewPlaceL(self, value, right):
        place = Place(self, value, None, right)
        if right == None:
            place.visual = self.makePlaceAtCenter(value)
        else:
            right.left = place
            place.visual = self.makePlaceAtCenter(value)
        self.current = place
        # print('place has been made',place.value, place.left, place.right)
        return place

    def moveL(self):
        self.moveCarefuly('place', 100, 0)
        self.current = self.current.left

    def moveR(self):
        self.moveCarefuly('place', -100, 0)
        self.current = self.current.right

    def L(self):
        if self.machine.moving.get() == 0:
            memo = self.current
            self.moveL()
            if self.current == None:
                newplace = self.createNewPlaceL(0, memo)
                self.current = newplace
        else:
            print('hold your HORSES right there for a second')

    def R(self):
        if self.machine.moving.get() == 0:
            memo = self.current
            self.moveR()
            if self.current == None:
                newplace = self.createNewPlaceR(0, memo)
                self.current = newplace
        else:
            print('hold your HORSES right there for a second')

    def S(self):
        print('Machine encountered S')

    def createstripe(self, inputNumbers):
        ''' Input might look like this: [63, 86, 12]'''
        self.machine.running.set(1)

        inputNumbers = [int(a) for a in inputNumbers.split()]
        print(inputNumbers)
        
        current = self.createNewPlace(0)
        left = current
        for n in inputNumbers:
            for i in range(n+1):
                newPlace = self.createNewPlaceR(1, left)
                self.moveR()
                left = newPlace
            #making 0
            emptyPlace = self.createNewPlaceR(0, left)
            self.moveR()
            left = emptyPlace

        self.current = emptyPlace
        
        for i in range(sum(inputNumbers)+2*len(inputNumbers)-1):
            self.L()
        
        self.machine.running.set(0)

    def moveCarefuly(self, thing, dx, dy):
        coordsX, coordsY, m1, m2 = self.machine.coords(thing)
        if (dx != 0 or dy != 0): # є що і куди переміщувати
            if self.animate: # якщо пересувати повільно
                # встановити зсув на 1 крок рівним 1, 0 або -1
                # у залежності від dx, dy
                ddx = sign(dx)
                ddy = sign(dy)
                # обчислити фінальні координати
                xfinal = coordsX + dx
                yfinal = coordsY + dy
                # запустити анімацію пересування
                self.machine.moving.set(1)
                self._movestep(thing, ddx, ddy, xfinal, yfinal)
                # очікувати зміни значення self.moving
                self.machine.wait_variable(self.machine.moving)
            else:
                # пересунути одразу на dx, dy
                self.machine.move(thing, dx, dy)

    def _movestep(self, thing, ddx, ddy, xfinal, yfinal):
        '''Зробити 1 крок для "повільного" пересування об'єкту.

           id - номер об'єкту,
           ddx, ddy - кроки по x, y,
           xfinal, yfinal - кінцеві координати лівого верхнього кута
        '''
        x, y, mx, my = self.machine.coords(thing) # отримати поточні координати
        # обчислити нові значення ddx, ddy
        if x == xfinal:
            ddx = 0
        if y == yfinal:
            ddy = 0
        if ddx or ddy: # якщо не дійшли до кінця
            self.machine.move(thing, ddx, ddy) # перемістити об'єкт
            # встановити виклик переміщення на наступний крок
            # через 5 мілісекунд
            self.machine.after(1, self._movestep, thing, ddx, ddy, xfinal, yfinal)
        else:
            # змінити self.moving, щоб зафіксувати завершення переміщення
            self.machine.moving.set(0)


class Place:
    def __init__(self, stripe, value, left, right):
        self.stripe = stripe
        self.value = value
        self.left = left
        self.right = right
        self.visual = None

    def __str__(self):
        ''' print function '''
        return str(self.value)


if __name__ == "__main__":
    root = tk.Tk()
    frame = TuringMachine(root)
    frame.pack()
    root.mainloop()
    print('app is closed')
