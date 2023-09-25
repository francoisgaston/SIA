
class Metric:

    @staticmethod
    # Metrica que se va a utilizar para medir el rendimiento del clasificador
    def measure(self, tp=0, tn=0, fp=0, fn=0):
        pass


class Accuracy(Metric):

    @staticmethod
    def measure(self, tp=0, tn=0, fp=0, fn=0):
        return (tp + tn) / (tp + tn + fp + fn)


class Precision(Metric):

    @staticmethod
    def measure(self, tp=0, tn=0, fp=0, fn=0):
        return tp / (tp + fp)


class Recall(Metric):

    @staticmethod
    def measure(self, tp=0, tn=0, fp=0, fn=0):
        return tp / (tp + fn)


class F1(Metric):

    @staticmethod
    def measure(self, tp=0, tn=0, fp=0, fn=0):
        precision = Precision.measure(tp, tn, fp, fn)
        recall = Recall.measure(tp, tn, fp, fn)
        return 2 * precision * recall / (precision + recall)


class TPR(Metric):

    @staticmethod
    def measure(self, tp=0, tn=0, fp=0, fn=0):
        return Recall.measure(tp, tn, fp, fn)


class FPR(Metric):

    @staticmethod
    def measure(self, tp=0, tn=0, fp=0, fn=0):
        return fp / (fp + tn)


def from_str(metric):
    match metric.upper():
        case "ACCURACY": return Accuracy.measure
        case "PRECISION": return Precision.measure
        case "RECALL": return Recall.measure
        case "F1": return F1.measure
        case "TPR": return TPR.measure
        case "FPR": return FPR.measure
        case _: raise ValueError("Nombre de métrica inválido")
