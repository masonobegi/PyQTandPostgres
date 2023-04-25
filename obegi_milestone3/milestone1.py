
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget,QTableWidgetItem,QVBoxLayout
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QIcon, QPixmap
import psycopg2


qtCreatorFile = "milestone1App.ui" # Enter file here.


Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)


class milestone1(QMainWindow):
   def __init__(self):
       super(milestone1, self).__init__()
       self.ui = Ui_MainWindow()
       self.ui.setupUi(self)
       # inits our defs
       self.loadStateList()
       self.ui.stateList.currentTextChanged.connect(self.stateChanged)
       self.ui.cityList.itemSelectionChanged.connect(self.cityChanged)
       self.ui.zipList.itemSelectionChanged.connect(self.zipChanged)
       self.ui.bname2.textChanged.connect(self.categoryChanged)
       self.ui.clearButton.clicked.connect(self.buttonClicked)
       self.ui.refreshButton.clicked.connect(self.refreshClicked)
       self.ui.searchButton.clicked.connect(self.searchButtonClicked)





   def executeQuery(self,sql_str):
       #try except to execute out query and connect to database
       try:
           """
           
           REAL PASSWORD NOT USED
           
           
           
           """



           conn = psycopg2.connect("dbname='milestone1db' user = 'postgres' host='localhost' password ='PASSWORD HERE'")
       except:
           print('Unable to connect to the database')
       # makes cursor, executes, commits gets result and returns
       cur = conn.cursor()
       cur.execute(sql_str)
       conn.commit()
       result = cur.fetchall()
       conn.close()
       return result


   #loads the state list
   def loadStateList(self):
       #clears query for bugs, and makes our sql statement
       self.ui.stateList.clear()
       sql_str = "SELECT distinct state_2let FROM business ORDER BY state_2let"
       #adds item in stateList, if cant then tell us it failed
       try:
           results = self.executeQuery(sql_str)
           for row in results:
               self.ui.stateList.addItem(row[0])
       except:
               print("Query failed")
       #makes ui look better
       self.ui.stateList.setCurrentIndex(-1)
       self.ui.stateList.clearEditText()


   #for when state changes
   def stateChanged(self):
       #bug fix
       self.ui.cityList.clear()
       # sets state
       state = self.ui.stateList.currentText()
       if (self.ui.stateList.currentIndex()>=0):
           #our query
           sql_str = "SELECT distinct city FROM business WHERE state_2let ='" + state + "'ORDER BY city;"
           #tries to add item and if not then tell us we failed
           try:
               results = self.executeQuery(sql_str)
               for row in results:
                   self.ui.cityList.addItem(row[0])
           except:
               print("Query failed")
           # takes every row out before we execute


   #for when city changes
   def cityChanged(self):
       # clear
       self.ui.zipList.clear()
       # if we have a city and state
       if (self.ui.stateList.currentIndex() >= 0) and (len(self.ui.cityList.selectedItems())>0):
           #makes our variables
           state = self.ui.stateList.currentText()
           city = self.ui.cityList.selectedItems()[0].text()
           sql_str = "SELECT distinct zipcode FROM business WHERE city ='" + city + "'ORDER BY zipcode;"
           # tries to add item and if not then tell us we failed
           try:
               results = self.executeQuery(sql_str)
               for row in results:
                   self.ui.zipList.addItem(row[0])
           except:
               print("Query failed")


   #for when zip changes
   def zipChanged(self):
       # clear lit
       self.ui.categoryList.clear()
       if (self.ui.stateList.currentIndex() >= 0):
           #makes our variables
           zipcode = self.ui.zipList.selectedItems()[0].text()
           sql_str = "SELECT distinct cat.category_id FROM category cat, business b WHERE zipcode ='" + zipcode + "' AND cat.business_id = b.business_id ORDER BY cat.category_id;"
           # tries to add item and if not then tell us we failed
           try:
               results = self.executeQuery(sql_str)
               for row in results:
                   self.ui.categoryList.addItem(row[0])
           except:
               print("Query failed")
            #sets our variables
           zipcode = self.ui.zipList.selectedItems()[0].text()


           sql_str = "SELECT CAST(count(business_id) AS VARCHAR) from business  WHERE zipcode = '" + zipcode + "'"
           # try to execute but if cannot then tell us we failed
           try:
               self.ui.numberOfBusinesses.clear()
               results = self.executeQuery(sql_str)
               for row in results:
                   self.ui.numberOfBusinesses.addItem(row[0])
           except:
               print("Query failed for num bus")

           sql_str = "SELECT CAST(population AS VARCHAR) FROM zipcodedata WHERE zipcode = '" + zipcode + "'"
           # try to execute but if cannot then tell us we failed
           try:
               self.ui.totalPop.clear()
               results = self.executeQuery(sql_str)
               for row in results:
                   self.ui.totalPop.addItem(row[0])
           except:
               print("Query failed for total pop")


           sql_str = "SELECT CAST(meanincome AS VARCHAR) FROM zipcodedata WHERE zipcode = '" + zipcode + "'"
           # try to execute but if cannot then tell us we failed
           try:
               self.ui.averageIncome.clear()
               results = self.executeQuery(sql_str)
               for row in results:
                   self.ui.averageIncome.addItem(row[0])
           except:
               print("Query failed for average income")


           sql_str = "SELECT CAST(count(cat.category_id) AS VARCHAR), cat.category_id FROM category cat, business b WHERE b.zipcode = '" + zipcode + "' AND cat.business_id = b.business_id GROUP BY cat.category_id ORDER BY count(cat.category_id) DESC"
           # tries to add item and if not then tell us we failed
           try:
               # makes our varibles and and then does some styling
               results = self.executeQuery(sql_str)
               style = "''section{""background-color: #f3f3f3; }"
               self.ui.zipBus.horizontalHeader().setStyleSheet(style)
               self.ui.zipBus.setColumnCount(len(results[0]))
               self.ui.zipBus.setRowCount(len(results))
               self.ui.zipBus.setHorizontalHeaderLabels(['# of businesses', 'category'])
               self.ui.zipBus.resizeColumnsToContents()
               self.ui.zipBus.setColumnWidth(0, 130)
               self.ui.zipBus.setColumnWidth(1, 150)
               # setting items in zipbus

               currentRowCount = 0
               for row in results:
                   for colCount in range(0, len(results[0])):
                       self.ui.zipBus.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
                   currentRowCount += 1
           except:
               print("Query failed for the zip bus")

   #when category changes
   def categoryChanged(self):
       #clear

       self.ui.businesses_3.clear()
       # makes our variables
       category = self.ui.categoryList.selectedItems()[0].text()
       zipcode = self.ui.zipList.selectedItems()[0].text()
       businessname = self.ui.bname2.text()

       sql_str = "SELECT DISTINCT b.name, b.address, b.city, CAST(b.stars AS varchar),CAST(b.reviewcount AS varchar), CAST(b.reviewrating AS varchar), CAST(b.numcheckins AS varchar) from business b, category cat WHERE name LIKE '%" + businessname + "%' AND b.zipcode = '" + zipcode + "' AND cat.category_id = '" + category + "' AND b.business_id = cat.business_id ORDER BY name;"
       # tries to add item and if not then tell us we failed
       try:
           # makes our varibles and and then does some styling
           results = self.executeQuery(sql_str)
           style = "''section{""background-color: #f3f3f3; }"
           self.ui.businesses_3.horizontalHeader().setStyleSheet(style)
           self.ui.businesses_3.setColumnCount(len(results[0]))
           self.ui.businesses_3.setRowCount(len(results))
           self.ui.businesses_3.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Stars', 'Review Count', 'Review Rating', 'Num Checkins'])
           self.ui.businesses_3.resizeColumnsToContents()
           self.ui.businesses_3.setColumnWidth(0, 300)
           self.ui.businesses_3.setColumnWidth(1, 300)
           self.ui.businesses_3.setColumnWidth(2, 100)
           # setting items in businesses_3
           currentRowCount = 0
           for row in results:
               for colCount in range(0, len(results[0])):
                   self.ui.businesses_3.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
               currentRowCount += 1
       except:
           print("Query failed")


       self.ui.popularTable.clear()
       sql_str = "SELECT b.name, CAST(b.numcheckins AS VARCHAR), CAST(b.reviewcount AS VARCHAR) FROM business b, category cat where cat.business_id = b.business_id AND cat.category_id = '" + category + "' AND b.zipcode = '" + zipcode + "' ORDER BY b.numcheckins DESC"
       # tries to add item and if not then tell us we failed
       try:
           # makes our varibles and and then does some styling
           results = self.executeQuery(sql_str)
           style = "''section{""background-color: #f3f3f3; }"
           self.ui.popularTable.horizontalHeader().setStyleSheet(style)
           self.ui.popularTable.setColumnCount(len(results[0]))
           self.ui.popularTable.setRowCount(len(results))
           self.ui.popularTable.setHorizontalHeaderLabels(['Business Name', '# of checkins', '# of reviews'])
           self.ui.popularTable.resizeColumnsToContents()
           self.ui.popularTable.setColumnWidth(0, 300)
           self.ui.popularTable.setColumnWidth(1, 150)
           # setting items in pop table

           currentRowCount = 0
           for row in results:
               for colCount in range(0, len(results[0])):
                   self.ui.popularTable.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
               currentRowCount += 1
       except:
           print("Query failed for the pop table")


       self.ui.sucTable.clear()
       sql_str = "SELECT b.name, CAST(b.stars AS VARCHAR), CAST(b.reviewrating AS VARCHAR) FROM business b, category cat where cat.business_id = b.business_id AND cat.category_id = '" + category + "' AND b.zipcode = '" + zipcode + "' ORDER BY stars DESC"
       # tries to add item and if not then tell us we failed
       try:
           # makes our varibles and and then does some styling
           results = self.executeQuery(sql_str)
           style = "''section{""background-color: #f3f3f3; }"
           self.ui.sucTable.horizontalHeader().setStyleSheet(style)
           self.ui.sucTable.setColumnCount(len(results[0]))
           self.ui.sucTable.setRowCount(len(results))
           self.ui.sucTable.setHorizontalHeaderLabels(['Business Name', 'Stars', 'Review Rating'])
           self.ui.sucTable.resizeColumnsToContents()
           self.ui.sucTable.setColumnWidth(0, 300)
           self.ui.sucTable.setColumnWidth(1, 150)
           # setting items in suc table

           currentRowCount = 0
           for row in results:
               for colCount in range(0, len(results[0])):
                   self.ui.sucTable.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
               currentRowCount += 1
       except:
           print("Query failed for the suc table")

   def buttonClicked(self):
       self.ui.popularTable.clear()
       self.ui.sucTable.clear()
       self.ui.businesses_3.clear()
       self.ui.bname2.clear()
       style = "''section{""background-color: #f3f3f3; }"
       self.ui.businesses_3.horizontalHeader().setStyleSheet(style)
       self.ui.businesses_3.setColumnCount(7)
       self.ui.businesses_3.setRowCount(0)
       self.ui.businesses_3.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Stars', 'Review Count', 'Review Rating', 'Num Checkins'])
       self.ui.businesses_3.resizeColumnsToContents()
       self.ui.businesses_3.setColumnWidth(0, 300)
       self.ui.businesses_3.setColumnWidth(1, 300)
       self.ui.businesses_3.setColumnWidth(2, 100)
       self.ui.sucTable.horizontalHeader().setStyleSheet(style)
       self.ui.sucTable.setColumnCount(3)
       self.ui.sucTable.setRowCount(0)
       self.ui.sucTable.setHorizontalHeaderLabels(['Business Name', 'Stars', 'Review Rating'])
       self.ui.sucTable.resizeColumnsToContents()
       self.ui.sucTable.setColumnWidth(0, 300)
       self.ui.sucTable.setColumnWidth(1, 150)
       self.ui.popularTable.horizontalHeader().setStyleSheet(style)
       self.ui.popularTable.setColumnCount(3)
       self.ui.popularTable.setRowCount(0)
       self.ui.popularTable.setHorizontalHeaderLabels(['Business Name', '# of checkins', '# of reviews'])
       self.ui.popularTable.resizeColumnsToContents()
       self.ui.popularTable.setColumnWidth(0, 300)
       self.ui.popularTable.setColumnWidth(1, 150)

   def searchButtonClicked(self):
       category = self.ui.categoryList.selectedItems()[0].text()
       zipcode = self.ui.zipList.selectedItems()[0].text()

       sql_str = "SELECT DISTINCT b.name, b.address, b.city, CAST(b.stars AS varchar),CAST(b.reviewcount AS varchar), CAST(b.reviewrating AS varchar), CAST(b.numcheckins AS varchar) from business b, category cat WHERE b.zipcode = '" + zipcode + "' AND cat.category_id = '" + category + "' AND b.business_id = cat.business_id ORDER BY name;"
       # tries to add item and if not then tell us we failed
       try:
           # makes our varibles and and then does some styling
           results = self.executeQuery(sql_str)
           style = "''section{""background-color: #f3f3f3; }"
           self.ui.businesses_3.horizontalHeader().setStyleSheet(style)
           self.ui.businesses_3.setColumnCount(len(results[0]))
           self.ui.businesses_3.setRowCount(len(results))
           self.ui.businesses_3.setHorizontalHeaderLabels(['Business Name', 'Address', 'City', 'Stars', 'Review Count', 'Review Rating', 'Num Checkins'])
           self.ui.businesses_3.resizeColumnsToContents()
           self.ui.businesses_3.setColumnWidth(0, 300)
           self.ui.businesses_3.setColumnWidth(1, 300)
           self.ui.businesses_3.setColumnWidth(2, 100)
           # setting items in businesses_3
           currentRowCount = 0
           for row in results:
               for colCount in range(0, len(results[0])):
                   self.ui.businesses_3.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
               currentRowCount += 1
       except:
           print("Query failed")

       self.ui.popularTable.clear()
       sql_str = "SELECT b.name, CAST(b.numcheckins AS VARCHAR), CAST(b.reviewcount AS VARCHAR) FROM business b, category cat where cat.business_id = b.business_id AND cat.category_id = '" + category + "' AND b.zipcode = '" + zipcode + "' ORDER BY b.numcheckins DESC"
       # tries to add item and if not then tell us we failed
       try:
           # makes our varibles and and then does some styling
           results = self.executeQuery(sql_str)
           style = "''section{""background-color: #f3f3f3; }"
           self.ui.popularTable.horizontalHeader().setStyleSheet(style)
           self.ui.popularTable.setColumnCount(len(results[0]))
           self.ui.popularTable.setRowCount(len(results))
           self.ui.popularTable.setHorizontalHeaderLabels(['Business Name', '# of checkins', '# of reviews'])
           self.ui.popularTable.resizeColumnsToContents()
           self.ui.popularTable.setColumnWidth(0, 300)
           self.ui.popularTable.setColumnWidth(1, 150)
           # setting items in pop table

           currentRowCount = 0
           for row in results:
               for colCount in range(0, len(results[0])):
                   self.ui.popularTable.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
               currentRowCount += 1
       except:
           print("Query failed for the pop table")

       self.ui.sucTable.clear()
       sql_str = "SELECT b.name, CAST(b.stars AS VARCHAR), CAST(b.reviewrating AS VARCHAR) FROM business b, category cat where cat.business_id = b.business_id AND cat.category_id = '" + category + "' AND b.zipcode = '" + zipcode + "' ORDER BY stars DESC"
       # tries to add item and if not then tell us we failed
       try:
           # makes our varibles and and then does some styling
           results = self.executeQuery(sql_str)
           style = "''section{""background-color: #f3f3f3; }"
           self.ui.sucTable.horizontalHeader().setStyleSheet(style)
           self.ui.sucTable.setColumnCount(len(results[0]))
           self.ui.sucTable.setRowCount(len(results))
           self.ui.sucTable.setHorizontalHeaderLabels(['Business Name', 'Stars', 'Review Rating'])
           self.ui.sucTable.resizeColumnsToContents()
           self.ui.sucTable.setColumnWidth(0, 300)
           self.ui.sucTable.setColumnWidth(1, 150)
           # setting items in suc table

           currentRowCount = 0
           for row in results:
               for colCount in range(0, len(results[0])):
                   self.ui.sucTable.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
               currentRowCount += 1
       except:
           print("Query failed for the suc table")


   def refreshClicked(self):
       category = self.ui.categoryList.selectedItems()[0].text()
       zipcode = self.ui.zipList.selectedItems()[0].text()
       self.ui.popularTable.clear()
       sql_str = "SELECT b.name, CAST(b.numcheckins AS VARCHAR), CAST(b.reviewcount AS VARCHAR) FROM business b, category cat where cat.business_id = b.business_id AND cat.category_id = '" + category + "' AND b.zipcode = '" + zipcode + "' ORDER BY b.numcheckins DESC"
       # tries to add item and if not then tell us we failed
       try:
           # makes our varibles and and then does some styling
           results = self.executeQuery(sql_str)
           style = "''section{""background-color: #f3f3f3; }"
           self.ui.popularTable.horizontalHeader().setStyleSheet(style)
           self.ui.popularTable.setColumnCount(len(results[0]))
           self.ui.popularTable.setRowCount(len(results))
           self.ui.popularTable.setHorizontalHeaderLabels(['Business Name', '# of Checkins', '# of Reviews'])
           self.ui.popularTable.resizeColumnsToContents()
           self.ui.popularTable.setColumnWidth(0, 300)
           self.ui.popularTable.setColumnWidth(1, 150)
           # setting items in pop table

           currentRowCount = 0
           for row in results:
               for colCount in range(0, len(results[0])):
                   self.ui.popularTable.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
               currentRowCount += 1
       except:
           print("Query failed for the pop table")


       self.ui.sucTable.clear()
       sql_str = "SELECT b.name, CAST(b.stars AS VARCHAR), CAST(b.reviewrating AS VARCHAR) FROM business b, category cat where cat.business_id = b.business_id AND cat.category_id = '" + category + "' AND b.zipcode = '" + zipcode + "' ORDER BY stars DESC"
       # tries to add item and if not then tell us we failed
       try:
           # makes our varibles and and then does some styling
           results = self.executeQuery(sql_str)
           style = "''section{""background-color: #f3f3f3; }"
           self.ui.sucTable.horizontalHeader().setStyleSheet(style)
           self.ui.sucTable.setColumnCount(len(results[0]))
           self.ui.sucTable.setRowCount(len(results))
           self.ui.sucTable.setHorizontalHeaderLabels(['Business Name', 'Stars', 'Review Rating'])
           self.ui.sucTable.resizeColumnsToContents()
           self.ui.sucTable.setColumnWidth(0, 300)
           self.ui.sucTable.setColumnWidth(1, 150)
           # setting items in suc table

           currentRowCount = 0
           for row in results:
               for colCount in range(0, len(results[0])):
                   self.ui.sucTable.setItem(currentRowCount, colCount, QTableWidgetItem(row[colCount]))
               currentRowCount += 1
       except:
           print("Query failed for the suc table")

if __name__ == "__main__":
   app = QApplication(sys.argv)
   window = milestone1()
   window.show()
   sys.exit(app.exec_())


