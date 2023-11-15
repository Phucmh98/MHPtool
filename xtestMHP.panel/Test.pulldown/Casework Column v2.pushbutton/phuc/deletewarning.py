
import Autodesk
from Autodesk.Revit.DB import FailureSeverity, ElementCategoryFilter, Transaction, InstanceVoidCutUtils, FailureProcessingResult
from pyrevit import revit, DB, script, forms
from rpw.ui.forms import FlexForm, Label, TextBox, Button, ComboBox, CheckBox, Separator,Alert
import rpw
from rpw import DB,ui
from rpw.ui.forms import SelectFromList
from pyrevit.forms import ProgressBar

def PreprocessFailures(failuresAccessor):
    FailureMessageAccessor = []
    failList = failuresAccessor.GetFailureMessages()
    FailureMessageAccessor.append(failList)
    if failList.Count > 0:
        for failure in failList:
            s = failure.GetSeverity()
            if s == FailureSeverity.Warning:
                failuresAccessor.DeleteWarning(failure)
            elif s == FailureSeverity.Error:
                failuresAccessor.ResolveFailure(failure)
        return FailureProcessingResult.ProceedWithCommit
    else:
        return  FailureProcessingResult.Continue


