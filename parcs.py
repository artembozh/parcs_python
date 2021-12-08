from Pyro4 import expose

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers

    def solve(self):
        arr = self.read_input()
        step = int(arr) / len(self.workers)

        mapped = []
        for i in range(0, len(self.workers)):
            mapped.append(self.workers[i].mymap(i * step, (i + 1) * step))

        reduced = self.myreduce(mapped)

        self.write_output(reduced)

    @staticmethod
    @expose
    def mymap(a, b):
        res = 1.
        for i in range(a, b):
            if i != 0:
                res *= Solver.count(i)
        return res
    
    @staticmethod
    @expose
    def count(a):
        return(float(2*a)**2)/float((2*a-1)*(2*a+1))

    @staticmethod
    @expose
    def myreduce(mapped):
        output = 1.
        for x in mapped:
            output *= float(x.value)
        return 2*output

    def read_input(self):
        f = open(self.input_file_name, 'r')
        line = f.readline()
        f.close()
        return int(line)

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        f.write(str('{:.100f}'.format(output)))
        f.close()