import GA
import sys
import time
import random
import numpy as np

from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from AnaSayfaUI import *

app=QApplication(sys.argv)
mainWindow=QMainWindow()
ui=Ui_MainWindow()
ui.setupUi(mainWindow)
mainWindow.show()
ui.solutionTable.setColumnWidth(0,75)
ui.solutionTable.setColumnWidth(1,110)
ui.solutionTable.setColumnWidth(2,365)
ui.solutionTable.setColumnWidth(3,75)
ui.MplWidget.canvas.setStyleSheet("background-color:transparent")
ui.MplWidget.canvas.figure.patch.set_facecolor("None")
ui.MplWidget.canvas.axes.set_facecolor("#19232d")
ui.MplWidget.canvas.axes.tick_params(colors='white', which='both') 


def updateStatus(text):
    ui.statusLabel.setText(text)
def clearTable():
    ui.solutionTable.clearContents()
    ui.solutionTable.setRowCount(0)
def changeStatusColor(color):
    if color == "orange":
        rgb = "rgb(255, 171, 0)";
    elif color == "red":
        rgb = "rgb(255, 48, 21)";
    elif color == "cyan":
        rgb = "rgb(56, 255, 166)";
    ui.statusLabel.setStyleSheet("color:"+str(rgb)+";font-size:15px;font-weight:bold;")
    
def generateButtonClicked():
    equationInputs = ui.equationInputsEdit.text()
    numberWeights = ui.numberWeightsEdit.text()
    solutionPopulation = ui.solutionPopulationEdit.text()
    low = ui.lowEdit.text()
    high = ui.highEdit.text()
    numOfGenerations = ui.numOfGenerationsEdit.text()
    numParentsMating = ui.numParentsMatingEdit.text()
    clearTable()
    ui.MplWidget.canvas.axes.clear()
    changeStatusColor("orange")
    updateStatus("Status: Processing Please Wait")
    ui.generateButton.setEnabled(False)
    ui.centralwidget.repaint()
    hesapla(equationInputs, numberWeights, solutionPopulation, low, high, numOfGenerations,numParentsMating)
    ui.generateButton.setEnabled(True)
    changeStatusColor("cyan")
    updateStatus("Status: Process Done")

def clearInputs():
    ui.equationInputsEdit.setText("");
    ui.numberWeightsEdit.setText("");
    ui.solutionPopulationEdit.setText("");
    ui.lowEdit.setText("");
    ui.highEdit.setText("");
    ui.numOfGenerationsEdit.setText("");
    ui.numParentsMatingEdit.setText("");
    ui.MplWidget.canvas.axes.clear()
    ui.MplWidget.canvas.draw()

def resetButtonClicked():
    clearInputs()
    clearTable()

def clearInputsButtonClicked():
    clearInputs()

def exitButtonClicked():
    sys.exit()

def addDataToTable(row, generation, bestResult, bestSolution, bestFitness):
    ui.solutionTable.setItem(row, 0, QTableWidgetItem(generation))
    ui.solutionTable.setItem(row, 1, QTableWidgetItem(bestResult))
    ui.solutionTable.setItem(row, 2, QTableWidgetItem(bestSolution))
    ui.solutionTable.setItem(row, 3, QTableWidgetItem(bestFitness))
    
    
def hesapla(equationInputs, numberWeights, solutionPopulation, low, high, numOfGenerations,numParentsMating):
    try:
        arr = [ float(x.strip()) for x in equationInputs.split(',') ]
        equation_inputs = arr #girdiler [4,-2,3.5,5,-11,-4.7]
        print(equation_inputs)
        num_weights = int(numberWeights)   #Ağırlıkların sayısı, 

        #Bir sonraki adım, başlangıç ​​popülasyonunu tanımlamaktır. 
        import numpy
        sol_per_pop = int(solutionPopulation) #Popülasyon başına çözüm sayısı
        pop_size = (sol_per_pop,num_weights) #Herbiri 6 adet genden oluşan 8 kromozom

        #Başlangıç popülasyonunun numpy.random.uniform ile random oluşturulması
        new_population = numpy.random.uniform(low=float(low), high=float(high), size=pop_size)
        print(new_population)

        num_generations = int(numOfGenerations)
        num_parents_mating = int(numParentsMating)  #eşleşme havuzundaki birey sayısı
        count = 0;
        xCor = np.array([0])
        yCor = np.array([0])
        for generation in range(num_generations):
            updateStatus("Status: Processing Please Wait ("+str(generation)+"/"+str(num_generations)+")")
            ui.solutionTable.setRowCount(count+1)
            ui.solutionTable.scrollToBottom()
            ui.centralwidget.repaint()
            print("Generation : ", generation)
            # Popülasyondaki her kromozom için uygunluk değerini hesapla
            fitness = GA.cal_pop_fitness(equation_inputs, new_population)
            #eşleşme havuzundaki en iyi bireylerin seçimi
            parents = GA.select_mating_pool(new_population, fitness, num_parents_mating)
            
            #Çaprazlama ile yeni birey üretimi
            offspring_crossover = GA.crossover(parents,
                                               offspring_size=(pop_size[0]-parents.shape[0], num_weights))
            #Mutasyon uygulanması
            offspring_mutation = GA.mutation(offspring_crossover)
            
            #Yeni popülasyon oluşturulması
            new_population[0:parents.shape[0], :] = parents
            new_population[parents.shape[0]:, :] = offspring_mutation
            
            #Geçerli iterasyondaki en iyi sonuç
            print("Best result : ", numpy.max(numpy.sum(new_population*equation_inputs, axis=1)))
            #Tüm nesilleri bitirmeyi yineledikten sonra en iyi çözümü elde etmek için 
            #İlk olarak, son nesildeki her bir çözüm için uygunluk hesaplanır.
            fitness = GA.cal_pop_fitness(equation_inputs, new_population)
            
            #Ardından, bu çözümün en iyi uygunluğa karşılık gelen indeksini döndürün.
            best_match_idx = numpy.where(fitness == numpy.max(fitness))
            print("Best solution : ", new_population[best_match_idx, :])
            print("Best solution fitness : ", fitness[best_match_idx])
            addDataToTable(count, str(generation+1), str(numpy.max(numpy.sum(new_population*equation_inputs, axis=1))), str(new_population[best_match_idx, :]), str(fitness[best_match_idx]))
            xCor = np.append(xCor, generation)
            yCor = np.append(yCor, fitness[best_match_idx][0])
            ui.MplWidget.canvas.axes.plot(xCor, yCor)
            count += 1
        ui.MplWidget.canvas.draw()
    except Exception as err:
        updateStatus("Error, check your inputs")
        print(err)


ui.generateButton.clicked.connect(generateButtonClicked)
ui.resetAllDataButton.clicked.connect(resetButtonClicked)
ui.clearInputsButton.clicked.connect(clearInputsButtonClicked)
ui.exitButton.clicked.connect(exitButtonClicked)

app.exec_()
