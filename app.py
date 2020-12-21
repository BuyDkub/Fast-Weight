from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
from shiboken2 import wrapInstance
import maya.cmds as mc
import maya.mel as mel
import maya.OpenMaya as om
import pymel.core as pm 

import ui2
reload(ui2)

class MainApp(QtWidgets.QMainWindow):
    def __init__(self ,parent=None):
        super(MainApp ,self).__init__(parent=parent)
        self.ui2 = ui2.Ui_MainWindow()
        self.ui2.setupUi(self)

        self.hideM_button = 0
        self.hideMD_button = 0

        self.model = []
        self.model_dup = []
        self.model_cut = []
        self.joint = []
        self.joint_dup = []
        self.extentBox = []
        self.transform = []
        
        self.dataWeight = {}

        self.groupPos = {}

        self.ui2.Add_pushButton.clicked.connect(self.add)

        self.ui2.comboBox.currentIndexChanged.connect(self.setHeadTreeWidget)
        
        self.ui2.hideModel_pushButton.clicked.connect(self.hide_model)
        self.ui2.hideDup_pushButton.clicked.connect(self.hide_modelDup)

        self.ui2.Create_blog_pushButton.clicked.connect(self.create_snapJoint)
        self.ui2.cut_pushButton.clicked.connect(self.cal)
        self.ui2.setWeight_pushButton.clicked.connect(self.setSkinWeight)

        self.ui2.duplicate_pushButton.clicked.connect(self.duplicates)
        self.ui2.duplicate2_pushButton.clicked.connect(self.duplicates)
        #self.ui2.envelope_Slider.

        self.ui2.transfer_pushButton.clicked.connect(self.transform_f)
        self.ui2.transform_pushButton.clicked.connect(self.transform_f)
        self.ui2.transfer2_pushButton.clicked.connect(self.transfer)

        self.ui2.treeWidget.itemClicked.connect(self.selItem)


        self.ui2.takeOut_pushButton.clicked.connect(self.takeOut)

        self.ui2.delete_pushButton.clicked.connect(self.delete)
        self.ui2.clear_pushButton.clicked.connect(self.clear)

    def selItem(self):
        item = self.ui2.treeWidget.selectedItems()
        print item[0].text(0)

        mc.select(item[0].text(0))
    def add(self):
        sel = mc.ls(sl=True, type='transform')
        headName = self.ui2.treeWidget.headerItem()
        headName = headName.text(0)
        
        if headName == 'All' or headName == 'Model':
            for i in sel:
                if not self.model:
                    self.model.append(i)
                    self.Item_model = QtWidgets.QTreeWidgetItem(self.ui2.treeWidget)
                    self.Item_model .setText(0,'Model')
                    ItemC = QtWidgets.QTreeWidgetItem()
                    ItemC.setText(0,i)
                    self.Item_model.addChild(ItemC)
                    self.ui2.treeWidget.expandAll()
                    
                    skinClusterStr = 'findRelatedSkinCluster("' + i + '")'
                    skinCluster = mel.eval(skinClusterStr)

                    if skinCluster:
                        Joint = mc.skinCluster(skinCluster ,q=True ,inf=True)
                        for j in Joint:
                            if j not in self.joint:
                                if not self.joint:
                                    self.joint.append(j)
                                    self.Item_joint = QtWidgets.QTreeWidgetItem(self.ui2.treeWidget)
                                    self.Item_joint.setText(0,'Joint')
                                    ItemC = QtWidgets.QTreeWidgetItem()
                                    ItemC.setText(0,j)
                                    self.Item_joint.addChild(ItemC)
                                    self.ui2.treeWidget.expandAll()
                                else:
                                    self.joint.append(j)
                                    ItemC = QtWidgets.QTreeWidgetItem()
                                    ItemC.setText(0,j)
                                    self.Item_joint.addChild(ItemC)
                                    self.ui2.treeWidget.expandAll()
                        self.upDate_jointComboBox()
                else:
                    if i not in self.model:
                        self.model.append(i)
                        ItemC = QtWidgets.QTreeWidgetItem()
                        ItemC.setText(0,i)
                        self.Item_model.addChild(ItemC)
                        self.ui2.treeWidget.expandAll()

                        skinClusterStr = 'findRelatedSkinCluster("' + i + '")'
                        skinCluster = mel.eval(skinClusterStr)

                        if skinCluster:
                            Joint = mc.skinCluster(skinCluster ,q=True ,inf=True)
                            for j in Joint:
                                if j not in self.joint:
                                    if not self.joint:
                                        self.joint.append(j)
                                        self.Item_joint = QtWidgets.QTreeWidgetItem(self.ui2.treeWidget)
                                        self.Item_joint.setText(0,'Joint')
                                        ItemC = QtWidgets.QTreeWidgetItem()
                                        ItemC.setText(0,j)
                                        self.Item_joint.addChild(ItemC)
                                        self.ui2.treeWidget.expandAll()
                                    else:
                                        self.joint.append(j)
                                        ItemC = QtWidgets.QTreeWidgetItem()
                                        ItemC.setText(0,j)
                                        self.Item_joint.addChild(ItemC)
                                        self.ui2.treeWidget.expandAll()
        if headName == 'Extent Box':
            for i in sel:
                if not self.extentBox:
                    self.extentBox.append(i)
                    Item = QtWidgets.QTreeWidgetItem(self.ui2.treeWidget)
                    Item.setText(0,i)
                else:
                    if i not in self.extentBox:
                        self.extentBox.append(i)
                        Item = QtWidgets.QTreeWidgetItem(self.ui2.treeWidget)
                        Item.setText(0,i)

        if headName == 'Joint':
            for i in sel:
                if not self.joint:
                    self.joint.append(i)
                    Item = QtWidgets.QTreeWidgetItem(self.ui2.treeWidget)
                    Item.setText(0,i)
                else:
                    if i not in self.joint:
                        self.joint.append(i)
                        Item = QtWidgets.QTreeWidgetItem(self.ui2.treeWidget)
                        Item.setText(0,i)

        if headName == 'Model Duplicated':
            for i in sel:
                if not self.model_dup:
                    self.model_dup.append(i)
                    Item = QtWidgets.QTreeWidgetItem(self.ui2.treeWidget)
                    Item.setText(0,i)
                else:
                    if i not in self.model_dup:
                        self.model_dup.append(i)
                        Item = QtWidgets.QTreeWidgetItem(self.ui2.treeWidget)
                        Item.setText(0,i)

        if headName == 'Model Cut':
            for i in sel:
                print i
                if not self.model_cut:
                    self.model_cut.append(i)
                    print self.model_cut
                    Item = QtWidgets.QTreeWidgetItem(self.ui2.treeWidget)
                    Item.setText(0,i)
                else:
                    if i not in self.model_cut:
                        self.model_cut.append(i)
                        print self.model_cut
                        Item = QtWidgets.QTreeWidgetItem(self.ui2.treeWidget)
                        Item.setText(0,i)
            print self.model_cut

        if headName == 'Joint Duplicated':
            for i in sel:
                if not self.joint_dup:
                    self.joint_dup.append(i)
                    Item = QtWidgets.QTreeWidgetItem(self.ui2.treeWidget)
                    Item.setText(0,i)
                else:
                    if i not in self.joint_dup:
                        self.joint_dup.append(i)
                        Item = QtWidgets.QTreeWidgetItem(self.ui2.treeWidget)
                        Item.setText(0,i)
    def upDate_jointComboBox(self):
        if  self.joint:
            for i in range(len(self.joint)):
                self.ui2.joint_comboBox.addItem("")
                self.ui2.joint_comboBox.setItemText(i, QtWidgets.QApplication.translate("MainWindow", '{}'.format(self.joint[i]), None, -1))
        else:
            pass
    def setHeadTreeWidget(self):
        newHead = self.ui2.comboBox.currentText()
        self.ui2.treeWidget.setHeaderLabel(newHead)
        self.ui2.treeWidget.clear()
        #self.ui2.treeWidget.expandAll()
        if newHead == 'All':
            if self.model:
                Item = QtWidgets.QTreeWidgetItem(self.ui2.treeWidget)
                Item.setText(0,'Model')
                for i in self.model:
                    ItemC = QtWidgets.QTreeWidgetItem()
                    ItemC.setText(0,i)
                    Item.addChild(ItemC)
                self.ui2.treeWidget.expandAll()
            if self.model_cut:
                Item = QtWidgets.QTreeWidgetItem(self.ui2.treeWidget)
                Item.setText(0,'Model Cut')
                for i in self.model_cut:
                    ItemC = QtWidgets.QTreeWidgetItem()
                    ItemC.setText(0,i)
                    Item.addChild(ItemC)
                self.ui2.treeWidget.expandAll()
            if self.model_dup:
                Item = QtWidgets.QTreeWidgetItem(self.ui2.treeWidget)
                Item.setText(0,'Model Duplicated')
                for i in self.model_dup:
                    ItemC = QtWidgets.QTreeWidgetItem()
                    ItemC.setText(0,i)
                    Item.addChild(ItemC)
                self.ui2.treeWidget.expandAll()
            if self.joint:
                Item = QtWidgets.QTreeWidgetItem(self.ui2.treeWidget)
                Item.setText(0,'Joint')
                for i in self.joint:
                    ItemC = QtWidgets.QTreeWidgetItem()
                    ItemC.setText(0,i)
                    Item.addChild(ItemC)
                self.ui2.treeWidget.expandAll()
            if self.joint_dup:
                Item = QtWidgets.QTreeWidgetItem(self.ui2.treeWidget)
                Item.setText(0,'Joint Duplicated')
                for i in self.joint_dup:
                    ItemC = QtWidgets.QTreeWidgetItem()
                    ItemC.setText(0,i)
                    Item.addChild(ItemC)
                self.ui2.treeWidget.expandAll()
            if self.extentBox:
                Item = QtWidgets.QTreeWidgetItem(self.ui2.treeWidget)
                Item.setText(0,'Extent Box')
                for i in self.extentBox:
                    ItemC = QtWidgets.QTreeWidgetItem()
                    ItemC.setText(0,i)
                    Item.addChild(ItemC)
                    self.ui2.treeWidget.expandAll()
        if newHead == 'Model':
            if self.model:
                Item = QtWidgets.QTreeWidgetItem(self.ui2.treeWidget)
                Item.setText(0,'Model')
                for i in self.model:
                    ItemC = QtWidgets.QTreeWidgetItem()
                    ItemC.setText(0,i)
                    Item.addChild(ItemC)
                self.ui2.treeWidget.expandAll()

        if newHead == 'Model Duplicated':
            if self.model_dup:
                Item = QtWidgets.QTreeWidgetItem(self.ui2.treeWidget)
                Item.setText(0,'Model Duplicated')
                for i in self.model_dup:
                    ItemC = QtWidgets.QTreeWidgetItem()
                    ItemC.setText(0,i)
                    Item.addChild(ItemC)
                self.ui2.treeWidget.expandAll()
        if newHead == 'Model Cut':
            if self.model_cut:
                Item = QtWidgets.QTreeWidgetItem(self.ui2.treeWidget)
                Item.setText(0,'Model Cut')
                for i in self.model_cut:
                    ItemC = QtWidgets.QTreeWidgetItem()
                    ItemC.setText(0,i)
                    Item.addChild(ItemC)
                self.ui2.treeWidget.expandAll()
        if newHead == 'Joint':
            if self.joint:
                Item = QtWidgets.QTreeWidgetItem(self.ui2.treeWidget)
                Item.setText(0,'Joint')
                for i in self.joint:
                    ItemC = QtWidgets.QTreeWidgetItem()
                    ItemC.setText(0,i)
                    Item.addChild(ItemC)
                self.ui2.treeWidget.expandAll()
        if newHead == 'Joint Duplicated':
            if self.joint_dup:
                Item = QtWidgets.QTreeWidgetItem(self.ui2.treeWidget)
                Item.setText(0,'Joint Duplicated')
                for i in self.joint_dup:
                    ItemC = QtWidgets.QTreeWidgetItem()
                    ItemC.setText(0,i)
                    Item.addChild(ItemC)
                self.ui2.treeWidget.expandAll()
        if newHead == 'Extent Box':
            if self.extentBox:
                Item = QtWidgets.QTreeWidgetItem(self.ui2.treeWidget)
                Item.setText(0,'Extent Box')
                for i in self.extentBox:
                    ItemC = QtWidgets.QTreeWidgetItem()
                    ItemC.setText(0,i)
                    Item.addChild(ItemC)
                self.ui2.treeWidget.expandAll()
    def create_snapJoint(self):
        joint_name = ''
        joint_name = self.ui2.joint_comboBox.currentText()
        extentBox_name = ''
        if joint_name :
            if joint_name != 'None'or joint_name != '' : 
                parent = mc.listRelatives(joint_name ,c=True ,pa=True)
                if parent != None:
                    extentBox_name = mc.polyCube(n=joint_name+'_extentBox')
                    #self.extentBox.append(extentBox_name)
                    
                    x = mc.xform(joint_name,q=True ,rp=True,ws=True)[0]
                    y = mc.xform(joint_name,q=True ,rp=True,ws=True)[1]
                    z = mc.xform(joint_name,q=True ,rp=True,ws=True)[2]
                    scaleX = 1
                    scaleY = 1
                    scaleZ = 1
                    SJ = [0,0,0]
                    if len(parent) == 1:
                        XJ1 = mc.xform(joint_name,q=True ,rp=True,ws=True)[0]
                        YJ1 = mc.xform(joint_name,q=True ,rp=True,ws=True)[1]
                        ZJ1 = mc.xform(joint_name,q=True ,rp=True,ws=True)[2]

                        XJ2 = mc.xform(parent[0],q=True ,rp=True,ws=True)[0]
                        YJ2 = mc.xform(parent[0],q=True ,rp=True,ws=True)[1]
                        ZJ2 = mc.xform(parent[0],q=True ,rp=True,ws=True)[2]
                        x = (XJ1 + XJ2)/2
                        y = (YJ1 + YJ2)/2
                        z = (ZJ1 + ZJ2)/2
                        SJ[0] = (XJ1 - XJ2)
                        SJ[1] = (YJ1 - YJ2)
                        SJ[2] = (ZJ1 - ZJ2)
                        for j in range(len(SJ)):
                            if SJ[j] < 0:
                                SJ[j] = SJ[j]*(-1)

                        if SJ[0] > SJ[1] and SJ[0] > SJ[2]:
                            scaleX = SJ[0]
                        elif SJ[1] > SJ[0] and SJ[1] > SJ[2]:
                            scaleY = SJ[1]
                        elif SJ[2] > SJ[0] and SJ[2] > SJ[1]:
                            scaleZ = SJ[2]
                        mc.xform(extentBox_name,t=(x,y,z),s=(scaleX,scaleY,scaleZ))
                    else :
                        num = 1
                        XJ1 = mc.xform(joint_name,q=True ,rp=True,ws=True)[0]
                        YJ1 = mc.xform(joint_name,q=True ,rp=True,ws=True)[1]
                        ZJ1 = mc.xform(joint_name,q=True ,rp=True,ws=True)[2]
                        x = XJ1
                        y = YJ1
                        z = ZJ1
                        
                        for i in parent :
                            check = mc.objectType(i) 
                            if check == 'joint':
                                XJ2 = mc.xform(i,q=True ,rp=True ,ws=True)[0]
                                YJ2 = mc.xform(i,q=True ,rp=True ,ws=True)[1]
                                ZJ2 = mc.xform(i,q=True ,rp=True ,ws=True)[2]
                                x = x + XJ2
                                y = y + YJ2
                                z = z + ZJ2
                                num += 1
                                SJ[0] += (XJ1 - XJ2)
                                SJ[1] += (YJ1 - YJ2)
                                SJ[2] += (ZJ1 - ZJ2)
                                for j in range(len(SJ)):
                                    if SJ[j] < 0:
                                        SJ[j] = SJ[j]*(-1)
                        x = x/num
                        y = y/num
                        z = z/num
                        if SJ[0] > SJ[1] and SJ[0] > SJ[2]:
                            scaleX = SJ[0]
                        elif SJ[1] > SJ[0] and SJ[1] > SJ[2]:
                            scaleY = SJ[1]
                        elif SJ[2] > SJ[0] and SJ[2] > SJ[1]:
                            scaleZ = SJ[2]

                        mc.xform(extentBox_name ,t=(x,y,z),s=(scaleX,scaleY,scaleZ))
                if extentBox_name:
                    mc.select(extentBox_name)
                    mc.viewFit(f=0.3)
                    self.extentBox.append(extentBox_name[0])
                    print self.extentBox
        index = self.ui2.joint_comboBox.currentIndex()
        self.ui2.joint_comboBox.setCurrentIndex(index+1)

    def cal(self):
        #model = 'cn_body'
        #box = 'C_back02_jnt_extentBox'
        #joint = ['aadf','fdfdfdfdfd','C_back02_jnt','asdfgggg']
        self.groupV = {}
        for model in self.model:
            for box in self.extentBox:
                N = mc.polyEvaluate(model,v=True)
                posBox = mc.xform(box,q=True,bb=True)
                xmin = posBox[0]
                xmax = posBox[3]
                ymin = posBox[1]
                ymax = posBox[4]
                zmin = posBox[2]
                zmax = posBox[5]
                vertex = []
                vert = []
                
                for i in self.joint :
                    if i in box:
                        nameGrp = i
                        print nameGrp
                for i in range(N):
                    pos = mc.pointPosition('{}.vtx[{}]'.format(model,i))
                    if pos[0]>xmin and pos[0]<xmax and pos[1]>ymin and pos[1]<ymax and pos[2]>zmin and pos[2]<zmax:
                        vertex.append('{}.vtx[{}]'.format(model,i))
                for v in vertex:
                    result = rayintersect( box ,v)
                    if result == 'inside':
                        vert.append(v)
                if vert:
                    self.groupV[nameGrp] = vert
                    print vert
                #print '{} {}'.format(nameGrp,len(groupV[nameGrp]))
        #print 'groupV = {}'.format(groupV.keys())
        print 'groupV = {}'.format(len(self.groupV.keys()))
        print len(self.joint)
        print len(self.extentBox)
        print '!COMPLETED!'

    def setSkinWeight(self):
        for joint in self.groupV.keys():
            for vert in self.groupV[joint]:
                obj = vert.split('.')[0]
                skinClusterStr = 'findRelatedSkinCluster("' + obj + '")'
                skinCluster = mel.eval(skinClusterStr)
                mc.skinPercent(skinCluster ,vert ,tv=[(joint,1.0)])
                print vert

        print '!COMPLETED!'

    def duplicates(self):
        self.main_joint = find_parentUp(self.joint[0])
        #if not mc.objExists(allJoint[0] + '_dup'):
        
        self.joint_dup = mc.duplicate( self.main_joint ,n='{}'.format(self.main_joint)+'_dup')
        seachAndReplaceNamse(self.joint_dup[0])
        
        for model in self.model:
            obj = model
            if not obj:
                return
            if mc.objExists(obj + '_dup'):
                print (obj + '_dup already exists!')
                return

            self.obj_dup = mc.duplicate(obj ,n=obj + '_dup')
            self.model_dup.append(self.obj_dup)

            skinClusterStr = 'findRelatedSkinCluster("' + obj + '")'
            skinCluster = mel.eval(skinClusterStr)
            joint = mc.skinCluster(skinCluster ,q=True ,inf=True)

            obj_dup = obj+'_dup'
            self.new_joint = self.main_joint+'_dup'

            try :
                mc.bakeDeformer(ss=self.main_joint ,sm=obj ,ds=self.new_joint ,dm=obj_dup ,mi=3)
                mc.deltaMush(obj_dup ,smoothingIterations=25 ,smoothingStep=0.35 ,pinBorderVertices=True
                        ,inwardConstraint=1 ,outwardConstraint=0 ,envelope=1)
            except:
                print obj
                pass
            
            skinClusterStr2 = 'findRelatedSkinCluster("' + obj_dup + '")'
            skinCluster2 = mel.eval(skinClusterStr2)
            mc.select(obj_dup)
            mc.skinPercent(skinCluster2,prw=0.01)

        #self.joint_dup = mc.skinCluster(skinCluster2 ,q=True ,inf=True)
        
        for jnt in self.joint:
            if mc.nodeType(jnt) == 'joint':
                mc.parentConstraint(jnt ,'{}'.format(jnt)+'_dup',mo=1)
        
        print '!!! COMPLETED !!!'
        
    def transform_f(self):
        if not mc.objExists(self.main_joint+'_trf'):
            joint_trf = mc.duplicate( self.main_joint ,n='{}'.format(self.main_joint)+'_trf')
            seachAndReplaceNamse(joint_trf[0])
            for jnt in self.joint:
                if mc.nodeType(jnt) == 'joint':
                    mc.parentConstraint(jnt ,'{}'.format(jnt)+'_trf',mo=1)

        for obj in self.model:
            if not obj:
                return
            if not (mc.objExists(obj) or mc.objExists(obj + '_dup')):
                print('Missing mesh or mush!')
                return

            if not mc.objExists(obj+'_trf'):
                obj_trf = mc.duplicate(obj ,n=obj + '_trf')[0]

            obj_dup = obj + '_dup'
            new_joint = self.main_joint+'_trf'
            #try:
            mc.bakeDeformer(ss=self.new_joint ,sm=obj_dup ,ds=new_joint ,dm=obj_trf ,mi=3)
            #except:
                #print 'error {}'.format(obj_trf)
                #pass

            numV = mc.polyEvaluate(obj_trf,v=True)

            skinClusterStr = 'findRelatedSkinCluster("' + obj_trf + '")'
            skinCluster = mel.eval(skinClusterStr)

            jointInf = mc.skinCluster(obj_trf ,q=True ,inf= True)
            #dataWeight = {}
            for n in range(numV):
                data = []
                weightInf = mc.skinPercent(skinCluster,'{}.vtx[{}]'.format(obj_trf,n),q=True,v=True)
                for i in range(len(weightInf)):
                    if weightInf[i] != 0 :
                        data.append( [jointInf[i],weightInf[i]] )
                        print '{}.vtx[{}],{} = {}'.format(obj_trf,n,jointInf[i],weightInf[i])
                self.dataWeight['{}.vtx[{}]'.format(obj_trf ,n)] = data
        print self.dataWeight

        '''
        skinClusterStr = 'findRelatedSkinCluster("' + obj + '")'
        skinCluster = mel.eval(skinClusterStr)
        mc.skinPercent(skinCluster,prw=0.01)'''
        print '!!! COMPLETED !!!'

    def transfer(self):
        sel = mc.ls(sl=True)
        numV = []
        for obj in sel:
            check = mc.nodeType(obj)
            if check == 'mesh':
                if 'vtx' in obj:
                    if ':' in obj:
                        num = (((obj.split('.')[1]).split('[')[1]).split(']')[0]).split(':')
                        for i in range(int(num[0]),int(num[1])+1):
                            numV.append(i)
                            print i 
                    else :
                        n = ((obj.split('.')[1]).split('[')[1]).split(']')[0]
                        numV.append(int(n))
                        print n
        print numV
            #self.ui2.weight_comboBox

    def delete(self):
        sel = self.ui2.treeWidget.selectedItems()
        dnot = ['All','Model','Model Duplicated','Model Cut','Extent Box','Joint','Joint Duplicated']
        topChild = sel[0].parent()
        if sel[0].text(0) not in dnot:
            if topChild.text(0) == 'Model' or topChild.text(0) == 'Joint':
                topChild = sel[0].parent()
                child_idx = topChild.indexOfChild(sel[0])
                topChild.takeChild(child_idx)
                if topChild.text(0) == 'Model':
                    model = self.model 
                    self.model = []
                    for i in model:
                        if i != sel[0].text(0):
                            self.model.append(i)
                if topChild.text(0) == 'Joint':
                    joint = self.joint 
                    self.joint = []
                    for i in joint:
                        if i != sel[0].text(0):
                            self.joint.append(i)
            else :
                topChild = sel[0].parent()
                child_idx = topChild.indexOfChild(sel[0])
                topChild.takeChild(child_idx)
                mc.delete(sel[0].text(0))
                if topChild.text(0) == 'Model Duplicated':
                    model_dup = self.model_dup 
                    self.model_dup = []
                    for i in model_dup:
                        if i != sel[0].text(0):
                            self.model_dup.append(i)
                if topChild.text(0) == 'Model Cut':
                    model_cut = self.model_cut 
                    self.model_cut = []
                    for i in model_cut:
                        if i != sel[0].text(0):
                            self.model_cut.append(i)
                if topChild.text(0) == 'Joint Duplicated':
                    joint_dup = self.joint_dup 
                    self.joint_dup = []
                    for i in joint_dup:
                        if i != sel[0].text(0):
                            self.joint_dup.append(i)
                if topChild.text(0) == 'Extent Box':
                    extentBox = self.extentBox 
                    self.extentBox = []
                    for i in extentBox:
                        if i != sel[0].text(0):
                            self.extentBox.append(i)
    def takeOut(self):
        sel = self.ui2.treeWidget.selectedItems()
        dnot = ['All','Model','Model Duplicated','Model Cut','Extent Box','Joint','Joint Duplicated']
        if sel[0].text(0) not in dnot:
            topChild = sel[0].parent()
            child_idx = topChild.indexOfChild(sel[0])
            topChild.takeChild(child_idx)
            if topChild.text(0) == 'Model':
                model = self.model 
                self.model = []
                for i in model:
                    if i != sel[0].text(0):
                        self.model.append(i)
            if topChild.text(0) == 'Joint':
                joint = self.joint 
                self.joint = []
                for i in joint:
                    if i != sel[0].text(0):
                        self.joint.append(i)
            if topChild.text(0) == 'Model Duplicated':
                model_dup = self.model_dup 
                self.model_dup = []
                for i in model_dup:
                    if i != sel[0].text(0):
                        self.model_dup.append(i)
            if topChild.text(0) == 'Model Cut':
                model_cut = self.model_cut 
                self.model_cut = []
                for i in model_cut:
                    if i != sel[0].text(0):
                        self.model_cut.append(i)
            if topChild.text(0) == 'Joint Duplicated':
                joint_dup = self.joint_dup 
                self.joint_dup = []
                for i in joint_dup:
                    if i != sel[0].text(0):
                        self.joint_dup.append(i)
            if topChild.text(0) == 'Extent Box':
                extentBox = self.extentBox 
                self.extentBox = []
                for i in extentBox:
                    if i != sel[0].text(0):
                        self.extentBox.append(i)    
    def clear(self):
        self.ui2.treeWidget.clear()
        self.model = []
        self.model_dup = []
        self.model_cut = []
        self.joint = []
        self.joint_dup = []
        self.extentBox = []
    def hide_model(self):
        #self.ui2.hideModel_pushButton()
        if self.hideM_button == 0 :
            for i in self.model:
                mc.hide(self.model)
                self.hideM_button = self.hideM_button+1
        else:
            for i in self.model:
                mc.showHidden(self.model)
                self.hideM_button = 0 
    def hide_modelDup(self):
        #self.ui2.hideModel_pushButton()
        if self.hideMD_button == 0 :
            for i in self.model_dup:
                mc.hide(i)
                self.hideMD_button = self.hideMD_button+1
        else:
            for i in self.model_dup:
                mc.showHidden(i)
                self.hideMD_button = 0 

def find_parentUp(joint):
    upJoint = ''
    if mc.nodeType(joint) == 'joint':
        i = 0
        while i == 0:
            upJoint = joint
            joint = mc.listRelatives(joint ,c=True ,p=True)[0]
            if joint == None or mc.nodeType(joint) != 'joint':
                i = 1
                break
    return upJoint

def rayintersect(box,vertex):
    pos = pm.xform(pm.PyNode(vertex), q=True, ws=True, t=True)
    cube = pm.PyNode(box)
    
    # -----------------------------
    # ---------- get cube cubeMfnMesh, normals
    cubeName = cube.shortName()
    mSel = om.MSelectionList() 
    mSel.add(cubeName)
    
    # get dag path
    cubeMDagPath = om.MDagPath()
    mSel.getDagPath(0, cubeMDagPath)
    
    # get MFnMesh
    cubeMfnMesh = om.MFnMesh(cubeMDagPath)
    
    # iterate thru each face of the cube, get face normal and invert it
    faceIt = om.MItMeshPolygon(cubeMDagPath)
    normals = []
    
    while not faceIt.isDone():
        normalMVector = om.MVector()
        faceIt.getNormal(normalMVector, om.MSpace.kWorld)
    
        # convert MVector to MFloat vector
        normalMFVector = om.MFloatVector(normalMVector)
        normals.append(normalMFVector)
    
        # go next
        faceIt.next()
    
    # -----------------------------
    # -----------------------------
    
    # iterate each nomals and shoot ray in that direction to see if ray hits
    raySrc = om.MFloatPoint(pos[0], pos[1], pos[2])  # the point to consider
    # cubeAccelParams = cubeMfnMesh.autoUniformGridParams()  # accelerator
    hitPoint = om.MFloatPoint()  # storage for point that ray hits
    # intersect each normal on cut cube
    for normal in normals:
        hit = cubeMfnMesh.anyIntersection(raySrc,  # raySource 
                    normal,     # rayDirection 
                    None,       # faceIds 
                    None,       # triIds 
                    True,       # idsSorted 
                    om.MSpace.kWorld,  # space
                    10000,     # maxParam 
                    False,      # testBothDirections 
                    None,  # accelParams
                    hitPoint,  # hitPoints
                    None,  # hitRayParams 
                    None,  # hitFaces
                    None,  # hitTriangles
                    None,  # hitBary1s
                    None,  # hitBary2s
                    1e-03)  # tolerance
        # not intersecting even only 1 normal means the point is outside the cut cube
        if not hit:
            return 'outside'
            break
    else:
        return 'inside'

def rename_joint(joint):
    rename_joint = []
    if joint :
        parent = mc.listRelatives( joint,c=True,pa=True)
        if parent :
            for i in parent:
                if  mc.objExists(split_Lastname(i)+'_dup'): 
                    rename = mc.rename(i,split_Lastname(i)+'_trf')
                else:
                    rename = mc.rename(i,split_Lastname(i)+'_dup')
                rename_joint.append(rename)
    return rename_joint

def seachAndReplaceNamse(input_joint):
    joint = []
    next = []
    rename = []
    joint.append(input_joint)
    while joint:
        for i in joint:
            rename = rename_joint(i)
            for j in rename:
                if rename:
                    #print j
                    next.append(j)
        joint = []
        if next: 
            for k in next:
                joint.append(k)
        next = []

def create_ExtentBox():
    #joint = mc.
    nameBox = mc.polyCube(n='Extent')[0]

def split_Lastname(name):
    newname = name.split('|')
    return newname[-1]

def show():
    app = MainApp(getMayaWindow())
    app.show()
def getMayaWindow():
    import maya.OpenMayaUI as mui
    ptr = mui.MQtUtil.mainWindow()
    return wrapInstance(long(ptr),QtWidgets.QWidget) 


