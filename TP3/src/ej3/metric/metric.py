class Metric:

    name = None

    # Metrica que se va a utilizar para medir el rendimiento del clasificador
    def measure(self, tp=0, tn=0, fp=0, fn=0):
        pass



class Accuracy(Metric):

    name = "Accuracy"

    def measure(self, tp=0, tn=0, fp=0, fn=0):
        return (tp + tn) / (tp + tn + fp + fn) if tp + tn + fp + fn != 0 else 0


class Precision(Metric):

    name = "Precision"

    def measure(self, tp=0, tn=0, fp=0, fn=0):
        return tp / (tp + fp) if tp + fp != 0 else 0


class Recall(Metric):

    name = "Recall"

    def measure(self, tp=0, tn=0, fp=0, fn=0):
        return tp / (tp + fn) if tp + fn != 0 else 0


class F1(Metric):

    name = "F1-SCORE"

    def measure(self, tp=0, tn=0, fp=0, fn=0):
        precision = Precision.measure(tp, tn, fp, fn)
        recall = Recall.measure(tp, tn, fp, fn)
        return 2 * precision * recall / (precision + recall) if precision + recall != 0 else 0


class TPR(Metric):

    name = "Tasa de verdaderos positivos"

    def measure(self, tp=0, tn=0, fp=0, fn=0):
        return Recall.measure(tp, tn, fp, fn)


class FPR(Metric):

    name = "Tasa de falsos positivos"

    def measure(self, tp=0, tn=0, fp=0, fn=0):
        return fp / (fp + tn) if fp + tn != 0 else 0


def from_str(metric):
    match metric.upper():
        case "ACCURACY": return Accuracy()
        case "PRECISION": return Precision()
        case "RECALL": return Recall()
        case "F1": return F1()
        case "TPR": return TPR()
        case "FPR": return FPR()
        case _: raise ValueError("Nombre de métrica inválido")
