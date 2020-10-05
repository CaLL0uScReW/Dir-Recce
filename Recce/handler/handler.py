
import os
import sys

# --
from utils.reports import *
from utils.settings import *

# ---
from .output import *
from .fuzzerdict import *
from .reportmanger import *
from .fuzzer import *
from net.request import *


class Handler(Request, Output):
    def __init__(self, url, kwargs):
        self.kwargs = kwargs
        Output.__init__(self)
        Request.__init__(self, url, kwargs)
        try:
            # test the connection to the TARGET
            try:
                resp = self.http("", "GET")
                if type(resp) == bool:
                    self.printWarn(
                        "CONNECTION ERROR: check your Connection or Target URL!", False
                    )
                    pass
            except Exception as e:
                print("An exception ocurred:\n{0}".format(str(e)))
                pass
            # init
            self.reportManager = ReportManager()
            self.setupReports()
            self.dict_ = FuzzerDict(self.kwargs["wordlist"], self.kwargs)
            fuzzer = Fuzzer(
                url, kwargs, self.dict_, kwargs["threads"], self.reportManager
            )
            fuzzer.start()
            fuzzer.wait()
        except Exception as e:
            self.printWarn(e)
            sys.exit(0)
        except (KeyboardInterrupt, SystemExit) as e:
            self.printWarn("Terminated by user...")
            sys.exit(0)
        if (
            kwargs["recursive"] is False
            or kwargs["multiple"] is False
            or kwargs["subDir"] == []
        ):
            print("\nTask Completed")

    def setupReports(self):
        # -- output report ---
        if self.kwargs["output"] != None:
            output = self.kwargs["output"]
            try:
                path, ext = output.split(".")
            except ValueError as e:
                self.printWarn(
                    "OUTPUT ERROR: Extension file (text or json) not specified!", not 0
                )
            # --
            if ext == "txt":
                self.reportManager.addOutput(TextReport(output))
            elif ext == "json":
                self.reportManager.addOutput(JsonReport(output))
            else:
                self.printWarn("Output file extension not supported!", not 0)
