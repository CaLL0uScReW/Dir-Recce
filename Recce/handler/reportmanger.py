


class ReportManager(object):
    def __init__(self):
        self.outputs = []

    def addOutput(self, output):
        self.outputs.append(output)

    def addPath(self, status, path, content, method):
        for output in self.outputs:
            output.addPath(status, path, content, method)

    def save(self):
        for output in self.outputs:
            output.save()

    def close(self):
        for output in self.outputs:
            output.close()
