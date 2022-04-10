class DoFile:
    def __init__(self, name):
        self.name = name
        self.__parse()

    def __parse(self):
        with open(self.name, "r") as f:
            # Parse the header section
            firstline = f.readline().rstrip()
            if firstline.startswith("###"):
                while True:
                    line = f.readline().rstrip()
                    if line.startswith("#depends on:"):
                        self.dependencies = list(map(str.strip, line.split(':')[1].split(",")))
                        print(self.dependencies)
                    else:
                        break

            # Retain actual code
            self.code = f.read()
        
def build_dependencies(doFiles):
    pass

def compile(do_file_names):
    files = [DoFile("./testDoFiles/" + file_name + ".do") for file_name in do_file_names]
    with open("compiled.do", "w") as myfile:
        for file in files:
            myfile.write("######################" + file.name + "######################\n")
            myfile.write("preserve\n")
            myfile.write(file.code)
            myfile.write("restore\n\n")

do_file_names = ["PS1_w22_solutions_part_B", "PS2_w22_solutions", "PS3_2022_solutions", "ps4_w22_solutions_compuational"]
compile(do_file_names)