
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


# version beta 7.0
# Design
import Design # design has fonts colors and UI elements

Window = Design.Window() # create a window

StatusBar = Design.StatusBar() # create a statusbar
StatusBar.pack() # place it in Window

SetupBar = Design.SetupBar() # create a setup bar
SetupBar.pack() # place it in Window
SetupBar.displayInstructions()

RunBar = Design.RunBar() # create a run button
RunBar.pack() # place it in Window
RunBar.displayInstructions()

TuringMachineFrame = Design.TuringMachineFrame() # create a frame with machine
TuringMachineFrame.pack()  # place it in Window

Design.mainloop() # run a window

# Copyright = Design.Copyright()

