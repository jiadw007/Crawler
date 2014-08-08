import os

class Review:
    
    cols= ['Total','Excellent','Very good', 'Average','Poor','Terrible','Location','Sleep quality','Rooms','Service','Value','Cleaness']
    rows = ['Attributes ', 'All Reviewer', 'Families', 'Couples', 'Solo', 'Business']
    directory = "D:\\Reviews\\"
    replace_sign = [("/","OR")]
    
    
    @classmethod
    
    def __init__(self,title):
        
        self.txt_title = title #first line in the txt file
        self.reviewers = [] # total reviewer
        self.families = []  # Families
        self.couples = []   #Couples
        self.solo = []  #Solo
        self.business = []  #Business
        self.table = []
        self.table.append(self.reviewers)
        self.table.append(self.families)
        self.table.append(self.couples)
        self.table.append(self.solo)
        self.table.append(self.business)

    def write_into_file(self, hotel_name):
        
        hotel_name = hotel_name.replace(Review.replace_sign[0][0],Review.replace_sign[0][1])        #standardlize file name
        pad = '|'
        file_path = os.path.join(Review.directory,hotel_name + ".txt")
        file_handle = open(file_path,'w')
        file_handle.write(self.txt_title + '\n')
        table_head = []
        for data in Review.rows:
            table_head.append(str(data).center(15))
        table_head = pad.join(table_head)
        file_handle.write(table_head + '\n')
        for attr in Review.cols:
            table_line= []
            table_line.append(attr.center(15))
            index = Review.cols.index(attr)
            for data in self.table:
                if index < len(data) and data[index] is not None :
                   
                    table_line.append(str(data[index]).center(15))
                else:
                    table_line.append(str(0).center(15))
            table_line = pad.join(table_line)    
            file_handle.write(table_line + "\n")
        file_handle.close()
        print "finish " + hotel_name + " !"
        