import threading


class SumOfSquares(threading.Thread):
    def __init__(self, num, **kwargs):
        self.num = num
        super(SumOfSquares, self).__init__(**kwargs)

        self.start()
    
    def _calculate(self):
        sum = 0
        for i in range(self.num):
            sum += self.num ** 2
        print(sum)

    def run(self):
        self._calculate()