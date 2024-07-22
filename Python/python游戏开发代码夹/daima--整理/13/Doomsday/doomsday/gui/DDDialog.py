from direct.gui.DirectGui import *

NoButtons = 0
Acknowledge = 1
CancelOnly = 2
TwoChoice = 3
YesNo = 4
TwoChoiceCustom = 5



class DDDialog(DirectDialog):
    
    def __init__(self, parent = None, style = NoButtons, **kw):
        if parent == None:
            parent = aspect2d
        self.style = style
        buttons = None
        if self.style != NoButtons:
            buttons = loader.loadModel(self.path)
        if self.style == TwoChoiceCustom:
            okImageList = (buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr'))
            cancelImageList = (buttons.find('**/CloseBtn_UP'), buttons.find('**/CloseBtn_DN'), buttons.find('**/CloseBtn_Rllvr'))
            buttonImage = [okImageList, cancelImageList]
            buttonValue = [DGG.DIALOG_OK, DGG.DIALOG_CANCEL]
            if 'buttonText' in kw:
                buttonText = kw['buttonText']
                del kw['buttonText']
            else:
                buttonText = ['OK', 'Cancel']
        elif self.style == TwoChoice:
            okImageList = (buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr'))
            cancelImageList = (buttons.find('**/CloseBtn_UP'), buttons.find('**/CloseBtn_DN'), buttons.find('**/CloseBtn_Rllvr'))
            buttonImage = [okImageList, cancelImageList]
            buttonText = ['OK', 'Cancel']
            buttonValue = [DGG.DIALOG_OK, DGG.DIALOG_CANCEL]
        elif self.style == YesNo:
            okImageList = (buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr'))
            cancelImageList = (buttons.find('**/CloseBtn_UP'), buttons.find('**/CloseBtn_DN'), buttons.find('**/CloseBtn_Rllvr'))
            buttonImage = [okImageList, cancelImageList]
            buttonText = ['Yes', 'No']
            buttonValue = [DGG.DIALOG_OK, DGG.DIALOG_CANCEL]
        elif self.style == Acknowledge:
            okImageList = (buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr'))
            buttonImage = [okImageList]
            buttonText = ['OK']
            buttonValue = [DGG.DIALOG_OK]
        elif self.style == CancelOnly:
            cancelImageList = (buttons.find('**/CloseBtn_UP'), buttons.find('**/CloseBtn_DN'), buttons.find('**/CloseBtn_Rllvr'))
            buttonImage = [cancelImageList]
            buttonText = ['Cancel']
            buttonValue = [DGG.DIALOG_CANCEL]
        elif self.style == NoButtons:
            buttonImage = []
            buttonText = []
            buttonValue = []
        else:
            self.notify.error('No such style as: ' + str(self.style))
        optiondefs = (('buttonImageList', buttonImage, DGG.INITOPT),
         ('buttonTextList', buttonText, DGG.INITOPT),
         ('buttonValueList', buttonValue, DGG.INITOPT),
         ('buttonPadSF', 2.2, DGG.INITOPT),
         ('text_font', DGG.getDefaultFont(), None),
         ('text_wordwrap', 12, None),
         ('text_scale', 0.07, None),
         ('buttonSize', (-0.05, 0.05, -0.05, 0.05), None),
         ('button_pad', (0, 0), None),
         ('button_relief', None, None),
         ('button_text_pos', (0, -0.1), None),
         ('fadeScreen', 0.5, None),
         ('image_color', (1, 1, 0.75, 1), None))
        self.defineoptions(kw, optiondefs)
        DirectDialog.__init__(self, parent)
        self.initialiseoptions(DDDialog)
        if buttons != None:
            buttons.removeNode()
        return

class GlobalDialog(DDDialog):
    __module__ = __name__

    def __init__(self, message = '', doneEvent = None, style = NoButtons, okButtonText = 'OK', cancelButtonText = 'Cancel', **kw):
        if not hasattr(self, 'path'):
            self.path = 'phase_3/models/gui/dialog_box_buttons_gui.bam'
        if doneEvent == None and style != NoButtons:
            self.notify.error('Boxes with buttons must specify a doneEvent.')
        self.__doneEvent = doneEvent
        if style == NoButtons:
            buttonText = []
        elif style == Acknowledge:
            buttonText = [okButtonText]
        elif style == CancelOnly:
            buttonText = [cancelButtonText]
        else:
            buttonText = [okButtonText, cancelButtonText]
        optiondefs = (('dialogName', 'globalDialog', DGG.INITOPT),
         ('buttonTextList', buttonText, DGG.INITOPT),
         ('text', message, None),
         ('command', self.handleButton, None))
        self.defineoptions(kw, optiondefs)
        DDDialog.__init__(self, style=style)
        self.initialiseoptions(GlobalDialog)
        return
    
    def handleButton(self, value):
        if value == DGG.DIALOG_OK:
            self.doneStatus = 'ok'
            messenger.send(self.__doneEvent)
        elif value == DGG.DIALOG_CANCEL:
            self.doneStatus = 'cancel'
            messenger.send(self.__doneEvent)