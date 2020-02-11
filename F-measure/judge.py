import csv


class F_measure:
    def __init__(self, True_Positive, False_Positive, False_Negative, result):
        self.TP = True_Positive
        self.FP = False_Positive
        self.FN = False_Negative
        self.res = result

    def F_print(self, name, numerator, denominator):
        print(name + " = " + str(numerator) + "/" + str(denominator) + " = " + '%.2f' % (numerator / denominator))

    def calculate_recall(self):
        R = self.TP / (self.TP + self.FN)
        self.F_print("Recall", self.TP, (self.TP + self.FN))
        return R

    def calculate_precision(self):
        P = self.TP / (self.TP + self.FP)
        self.F_print("Precision", self.TP, (self.TP + self.FP))
        return P

    def calculate_result(self):
        R = self.calculate_recall()
        P = self.calculate_precision()
        self.res = 2 * P * R / (P + R)
        print("F1 = " + '%.2f' % self.res)


F1 = F_measure(0, 0, 0, 0)


class Graph:
    def __init__(self, std_path, submission_path):
        self.node_index = {}
        self.myEdges = {}
        self.stdEdges = {}
        self.nodes_cnt = 1
        self.std = std_path
        self.submission = submission_path

    def create_Graph(self):
        with open(self.std, 'r') as file:
            reader = csv.reader(file)
            i = False
            for row in reader:
                if i and row[2] == '1':
                    if row[0] not in self.node_index:
                        self.node_index[row[0]] = self.nodes_cnt
                        self.nodes_cnt += 1
                    if row[1] not in self.node_index:
                        self.node_index[row[1]] = self.nodes_cnt
                        self.nodes_cnt += 1
                else:
                    i = True

        with open(self.std, 'r') as file:
            reader = csv.reader(file)
            i = False
            for row in reader:
                if i and row[2] == '1':
                    u = self.node_index[row[0]]
                    v = self.node_index[row[1]]
                    hashing = u + v*(self.nodes_cnt+7)
                    self.stdEdges[hashing] = 1
                    self.stdEdges[v+u*(self.nodes_cnt+7)] = 1
                else:
                    i = True

        with open(self.submission, 'r') as file:
            reader = csv.reader(file)
            i = False
            for row in reader:
                if i:
                    if row[0] in self.node_index and row[1] in self.node_index:
                        u = self.node_index[row[0]]
                        v = self.node_index[row[1]]
                        self.myEdges[u + v * (self.nodes_cnt + 7)] = 1
                        self.myEdges[v + u * (self.nodes_cnt + 7)] = 1
                        if hashing in self.stdEdges:
                            F1.TP += 1
                        else:
                            F1.FP += 1
                else:
                    i = True

        with open(self.std, 'r') as file:
            reader = csv.reader(file)
            i = False
            for row in reader:
                if i and row[2] == '1':
                    u = self.node_index[row[0]]
                    v = self.node_index[row[1]]
                    hashing = u + v * (self.nodes_cnt + 7)
                    if hashing in self.myEdges:
                        F1.FN += 1
                else:
                    i = True


G1 = Graph('labeled_dataset.csv', 'submission.csv')
G1.create_Graph()
F1.calculate_result()
