import os

class Review:
    
    cols= ['Total','Excel','VG', 'Ave','Poor','Terr','Loc','Sleep','Rm','Serv','Val','Clean']
    rows = ['All', 'Fam', 'Coup', 'Solo', 'Busi']
    directory = "D:\\Reviews\\"
    replace_sign = [("/","OR")]
    file_path = "D:\\Reviews\\new york.csv"
    
    @classmethod
    
    def __init__(self,hotel_name,address, thumb_up, rank):
        
        self.reviewers = [] # total reviewer
        self.families = []  # Families
        self.couples = []   #Couples
        self.solo = []  #Solo
        self.business = []  #Business
        self.table = [] #table
        self.table.append(self.reviewers)
        self.table.append(self.families)
        self.table.append(self.couples)
        self.table.append(self.solo)
        self.table.append(self.business)
        self.address = address
        self.thumb_up = thumb_up
        self.rank = rank
        self.hotel_name = hotel_name.replace('/',' ').replace(",", '')#standardlize file name

    def write_into_file(self):
        '''write into txt file'''
        #file_path = os.path.join(Review.directory,self.hotel_name + ".txt")
        file_handle = open(Review.file_path,'a')
        #file_handle.write(csv_line + "\n")
        #name = self.hotel_name.replace(Review.replace_sign[0][1],Review.replace_sign[0][0])
        data = self.hotel_name + "," + self.address + "," + self.thumb_up + "," + self.rank + ","
        for row in Review.rows:
            index = Review.rows.index(row)
            
            list_index = self.table[index]
            for col in Review.cols:
                i = Review.cols.index(col)
                data = data + list_index[i] + ","
        file_handle.write(data + "\n")
                
        ##write the first line into file
        ##file_handle.write(self.txt_title + '\n')
        
        ##write the table head into file
        ##table_head = []
        ##for data in Review.rows:
            ##table_head.append(str(data).center(15))
        ##table_head = pad.join(table_head) 
        ##file_handle.write(table_head + '\n')
        ##write table lines into file
        ##for attr in Review.cols:
            ##table_line= []
            ##table_line.append(attr.center(15))
            ##index = Review.cols.index(attr)
            ##for data in self.table:
                ##if index < len(data) and data[index] is not None :
                   
                    ##table_line.append(str(data[index]).center(15))
                ##else:
                    ##table_line.append(str(0).center(15))
            ##table_line = pad.join(table_line)    
            ##file_handle.write(table_line + "\n")
        ##file_handle.close()
        ##print "finish " + self.hotel_name + " !"
        