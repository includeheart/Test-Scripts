class Height(object):
    def __init__(self, feet, inches):
        self.feet = feet
        self.inches = inches
    def __str__(self):
        output = str(self.feet) + ' feet, ' + str(self.inches) + ' inches'
        return output
    def __add__(self, other):
        height_A_inches = self.feet * 12 + self.inches
        height_B_inches = other.feet * 12 + other.inches
        total_height_inches = height_A_inches + height_B_inches
        output_feet = total_height_inches // 12
        output_inches = total_height_inches - (output_feet * 12)
        return Height(output_feet, output_inches)
    def __sub__(self, other):
        height_A_inches = self.feet * 12 + self.inches
        height_C_inches = other.feet * 12 + other.inches
        total_height_inches = height_A_inches - height_C_inches
        output_feet = total_height_inches // 12
        output_inches = total_height_inches - (output_feet * 12)
        return Height(output_feet, output_inches)
    def __lt__(self, other):
        height_A_inches = self.feet * 12 + self.inches
        height_B_inches = other.feet * 12 + other.inches
        return height_A_inches < height_B_inches
    def __gt__(self, other):
        height_A_inches = self.feet * 12 + self.inches
        height_B_inches = other.feet * 12 + other.inches
        return height_A_inches > height_B_inches
    def __le__(self, other):
        height_A_inches = self.feet * 12 + self.inches
        height_B_inches = other.feet * 12 + other.inches
        return height_A_inches <= height_B_inches
    def __ge__(self, other):
        height_A_inches = self.feet * 12 + self.inches
        height_B_inches = other.feet * 12 + other.inches
        return height_A_inches >= height_B_inches
    def __eq__(self, other):
        height_A_inches = self.feet * 12 + self.inches
        height_B_inches = other.feet * 12 + other.inches
        return height_A_inches == height_B_inches
    def __ne__(self, other):
        height_A_inches = self.feet * 12 + self.inches
        height_B_inches = other.feet * 12 + other.inches
        return height_A_inches != height_B_inches
person_A_height = Height(5, 10)
person_B_height = Height(4, 10)
person_C_height = Height(3, 9)
height_sum = person_A_height + person_B_height
height_diff = person_A_height - person_C_height
print('Height sum:', height_sum)
print('Height difference:', height_diff)
print('Is person A taller than person B?', person_A_height > person_B_height)
print('Is person A shorter than person B?', person_A_height < person_B_height)
print('Is person A equal to person B?', person_A_height == person_B_height)
print('Is person A not equal to person B?', person_A_height != person_B_height)