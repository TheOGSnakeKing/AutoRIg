import maya.cmds as cmd

def rear():
    
    #create lists
    R_LOC = ["R_rear_shldr_LOC", "R_rear_elbow_LOC", "R_rear_backFoot_LOC", "R_rear_frontFoot_LOC", "R_rear_paws_LOC"]
    L_LOC = ["L_rear_shldr_LOC", "L_rear_elbow_LOC", "L_rear_backFoot_LOC", "L_rear_frontFoot_LOC", "L_rear_paws_LOC"]
    R_JNT = ["R_rear_shldr_JNT", "R_rear_elbow_JNT", "R_rear_backFoot_JNT", "R_rear_frontFoot_JNT", "R_rear_paws_JNT"]
    L_JNT = ["L_rear_shldr_JNT", "L_rear_elbow_JNT", "L_rear_backFoot_JNT", "L_rear_frontFoot_JNT", "L_rear_paws_JNT"]
    CTRL = ["L_rear_paws_CTRL", "R_rear_paws_CTRL", "L_rear_PoleVector_CTRL", "R_rear_PoleVector_CTRL"]
    R_GEO = ["R_rear_shoulder_GEO", "R_rear_backFoot_GEO", "R_rear_frontFoot_GEO", "R_rear_paws_GEO"]
    L_GEO = ["L_rear_shoulder_GEO", "L_rear_backFoot_GEO", "L_rear_frontFoot_GEO", "L_rear_paws_GEO"]
    
    #Looping through LOC, get LOC location info and transfer the JNT
    i=0
    
    for each in R_LOC:
        x=cmd.getAttr(each+".translateX")
        y=cmd.getAttr(each+".translateY")
        z=cmd.getAttr(each+".translateZ")
        cmd.joint(p=(x,y,z),n=R_JNT[i],rad=0.1)
        i+=1
    cmd.select(R_JNT[0], r=True) #select starting joint
    cmd.parent(R_JNT[0], w = True)
    cmd.select(R_JNT[0], r=True)
    cmd.FreezeTransformations()
    cmd.joint(e=True, ch=True, oj='none', zso=True)
    
    i=0
    
    for each in L_LOC:
        x=cmd.getAttr(each+".translateX")
        y=cmd.getAttr(each+".translateY")
        z=cmd.getAttr(each+".translateZ")
        cmd.joint(p=(x,y,z),n=L_JNT[i],rad=0.1)
        i+=1
    cmd.select(L_JNT[0], r=True) #select starting joint
    cmd.parent(L_JNT[0], w = True)
    cmd.select(L_JNT[0], r=True)
    cmd.FreezeTransformations()
    cmd.joint(e=True, ch=True, oj='none', zso=True)
    
    #Looping through LOC, get LOC location infor and transfer the CTRL
    
    x=cmd.getAttr("R_rear_frontFoot_LOC.translateX")
    y=cmd.getAttr("R_rear_frontFoot_LOC.translateY")
    z=cmd.getAttr("R_rear_frontFoot_LOC.translateZ")
    cmd.circle(c=(x,y,z),n=CTRL[1],r=5,nr=(0,1,0))
    cmd.xform(cp=True)
    
    x=cmd.getAttr("L_rear_frontFoot_LOC.translateX")
    y=cmd.getAttr("L_rear_frontFoot_LOC.translateY")
    z=cmd.getAttr("L_rear_frontFoot_LOC.translateZ")
    cmd.circle(c=(x,y,z),n=CTRL[0],r=5,nr=(0,1,0))
    cmd.xform(cp=True)
    
    x=cmd.getAttr("L_rear_elbow_LOC.translateX")
    y=cmd.getAttr("L_rear_elbow_LOC.translateY")
    z=cmd.getAttr("L_rear_elbow_LOC.translateZ")
    cmd.circle(c=(x+6,y,z),n=CTRL[2],r=1,nr=(1,0,0))
    cmd.xform(cp=True)
    
    x=cmd.getAttr("R_rear_elbow_LOC.translateX")
    y=cmd.getAttr("R_rear_elbow_LOC.translateY")
    z=cmd.getAttr("R_rear_elbow_LOC.translateZ")
    cmd.circle(c=(x+6,y,z),n=CTRL[3],r=1,nr=(1,0,0))
    cmd.xform(cp=True)

   
    #Parenting meshes to joints
    
    i=0
    for each in R_GEO:
        cmd.parent(R_GEO[i],R_JNT[i])
        i+=1
    i=0
    for each in L_GEO:
        cmd.parent(L_GEO[i],L_JNT[i])
        i+=1
     
    #Assigning IK handles
        
    cmd.ikHandle(solver="ikRPsolver",n="R_rear_knee_IK",sj=R_JNT[0],ee=R_JNT[2],s="sticky")
    cmd.ikHandle(solver="ikSCsolver",n="R_rear_ball_IK",sj=R_JNT[2],ee=R_JNT[3],s="sticky")
    cmd.ikHandle(solver="ikSCsolver",n="R_rear_toe_IK",sj=R_JNT[3],ee=R_JNT[4],s="sticky")
    
    cmd.ikHandle(solver="ikRPsolver",n="L_rear_knee_IK",sj=L_JNT[0],ee=L_JNT[2],s="sticky")
    cmd.ikHandle(solver="ikSCsolver",n="L_rear_ball_IK",sj=L_JNT[2],ee=L_JNT[3],s="sticky")
    cmd.ikHandle(solver="ikSCsolver",n="L_rear_toe_IK",sj=L_JNT[3],ee=L_JNT[4],s="sticky")
    
    cmd.poleVectorConstraint(CTRL[2],"L_rear_knee_IK")
    cmd.poleVectorConstraint(CTRL[3],"R_rear_knee_IK")
    
    #Grouping and parenting
    cmd.group(CTRL[2],CTRL[3],n="rear_poleVector_GRP")
    
    cmd.group("R_rear_knee_IK",n="R_rear_Ball_GRP")
    cmd.group("R_rear_ball_IK","R_rear_toe_IK",n="R_rear_toe_GRP")
    cmd.group("R_rear_Ball_GRP","R_rear_toe_GRP",n="R_rear_ankle_GRP")
    cmd.group("R_rear_ankle_GRP",n="R_rear_foot_GRP")
    cmd.parent("R_rear_foot_GRP",CTRL[1])
    
    cmd.group("L_rear_knee_IK",n="L_rear_Ball_GRP")
    cmd.group("L_rear_ball_IK","L_rear_toe_IK",n="L_rear_toe_GRP")
    cmd.group("L_rear_Ball_GRP","L_rear_toe_GRP",n="L_rear_ankle_GRP")
    cmd.group("L_rear_ankle_GRP",n="L_rear_foot_GRP")
    cmd.parent("L_rear_foot_GRP",CTRL[0])
    
    cmd.group(CTRL[1],CTRL[0],"rear_poleVector_GRP",n="rear_legs_GRP")
      
    

def front():
    
    
    #create lists
    R_LOC = ["R_front_shldr_LOC", "R_front_elbow_LOC", "R_front_backFoot_LOC", "R_front_frontFoot_LOC", "R_front_paws_LOC"]
    L_LOC = ["L_front_shldr_LOC", "L_front_elbow_LOC", "L_front_backFoot_LOC", "L_front_frontFoot_LOC", "L_front_paws_LOC"]
    R_JNT = ["R_front_shldr_JNT", "R_front_elbow_JNT", "R_front_backFoot_JNT", "R_front_frontFoot_JNT", "R_front_paws_JNT"]
    L_JNT = ["L_front_shldr_JNT", "L_front_elbow_JNT", "L_front_backFoot_JNT", "L_front_frontFoot_JNT", "L_front_paws_JNT"]
    CTRL = ["L_front_paws_CTRL", "R_front_paws_CTRL", "L_front_PoleVector_CTRL", "R_front_PoleVector_CTRL"]
    R_GEO = ["R_front_shoulder_GEO", "R_front_backFoot_GEO", "R_front_frontFoot_GEO", "R_front_paws_GEO"]
    L_GEO = ["L_front_shoulder_GEO", "L_front_backFoot_GEO", "L_front_frontFoot_GEO", "L_front_paws_GEO"]
    
    
    #Looping through LOC, get LOC location info and transfer the JNT
    i=0
    for each in R_LOC:
        x=cmd.getAttr(each+".translateX")
        y=cmd.getAttr(each+".translateY")
        z=cmd.getAttr(each+".translateZ")
        cmd.joint(p=(x,y,z),n=R_JNT[i],rad=0.1)
        i+=1
    cmd.select(R_JNT[0], r=True) #select starting joint
    
    cmd.FreezeTransformations()
    cmd.joint(e=True, ch=True, oj='none', zso=True)
    
    i=0
    for each in L_LOC:
        x=cmd.getAttr(each+".translateX")
        y=cmd.getAttr(each+".translateY")
        z=cmd.getAttr(each+".translateZ")
        cmd.joint(p=(x,y,z),n=L_JNT[i],rad=0.1)
        i+=1
    cmd.select(L_JNT[0], r=True) #select starting joint
    cmd.parent(L_JNT[0], w=True)
    cmd.select(L_JNT[0], r=True)
    cmd.FreezeTransformations()
    cmd.joint(e=True, ch=True, oj='none', zso=True)
    
    
    #Parenting meshes to joints
    
    i=0
    for each in R_GEO:
        cmd.parent(R_GEO[i],R_JNT[i])
        i+=1
    i=0
    for each in L_GEO:
        cmd.parent(L_GEO[i],L_JNT[i])
        i+=1
    
    
    #Looping through LOC, get LOC location infor and transfer the CTRL
    
    x=cmd.getAttr("R_front_frontFoot_LOC.translateX")
    y=cmd.getAttr("R_front_frontFoot_LOC.translateY")
    z=cmd.getAttr("R_front_frontFoot_LOC.translateZ")
    cmd.circle(c=(x,y,z),n=CTRL[1],r=5,nr=(0,1,0))
    cmd.xform(cp=True)
    
    x=cmd.getAttr("L_front_frontFoot_LOC.translateX")
    y=cmd.getAttr("L_front_frontFoot_LOC.translateY")
    z=cmd.getAttr("L_front_frontFoot_LOC.translateZ")
    cmd.circle(c=(x,y,z),n=CTRL[0],r=5,nr=(0,1,0))
    cmd.xform(cp=True)
    
    x=cmd.getAttr("L_front_elbow_LOC.translateX")
    y=cmd.getAttr("L_front_elbow_LOC.translateY")
    z=cmd.getAttr("L_front_elbow_LOC.translateZ")
    cmd.circle(c=(x-6,y,z),n=CTRL[2],r=1,nr=(1,0,0))
    cmd.xform(cp=True)
    
    x=cmd.getAttr("R_front_elbow_LOC.translateX")
    y=cmd.getAttr("R_front_elbow_LOC.translateY")
    z=cmd.getAttr("R_front_elbow_LOC.translateZ")
    cmd.circle(c=(x-6,y,z),n=CTRL[3],r=1,nr=(1,0,0))
    cmd.xform(cp=True)
    
    
    #Assigning IK handles
        
    cmd.ikHandle(solver="ikRPsolver",n="R_front_knee_IK",sj=R_JNT[0],ee=R_JNT[2],s="sticky")
    cmd.ikHandle(solver="ikSCsolver",n="R_front_ball_IK",sj=R_JNT[2],ee=R_JNT[3],s="sticky")
    cmd.ikHandle(solver="ikSCsolver",n="R_front_toe_IK",sj=R_JNT[3],ee=R_JNT[4],s="sticky")
    
    cmd.ikHandle(solver="ikRPsolver",n="L_front_knee_IK",sj=L_JNT[0],ee=L_JNT[2],s="sticky")
    cmd.ikHandle(solver="ikSCsolver",n="L_front_ball_IK",sj=L_JNT[2],ee=L_JNT[3],s="sticky")
    cmd.ikHandle(solver="ikSCsolver",n="L_front_toe_IK",sj=L_JNT[3],ee=L_JNT[4],s="sticky")
    
    cmd.poleVectorConstraint(CTRL[2],"L_front_knee_IK")
    cmd.poleVectorConstraint(CTRL[3],"R_front_knee_IK")
    
    #Grouping and parenting
    cmd.group(CTRL[2],CTRL[3],n="front_poleVector_GRP")
    
    cmd.group("R_front_knee_IK",n="R_front_Ball_GRP")
    cmd.group("R_front_ball_IK","R_front_toe_IK",n="R_front_toe_GRP")
    cmd.group("R_front_Ball_GRP","R_front_toe_GRP",n="R_front_ankle_GRP")
    cmd.group("R_front_ankle_GRP",n="R_front_foot_GRP")
    cmd.parent("R_front_foot_GRP",CTRL[1])
    
    cmd.group("L_front_knee_IK",n="L_front_Ball_GRP")
    cmd.group("L_front_ball_IK","L_front_toe_IK",n="L_front_toe_GRP")
    cmd.group("L_front_Ball_GRP","L_front_toe_GRP",n="L_front_ankle_GRP")
    cmd.group("L_front_ankle_GRP",n="L_front_foot_GRP")
    cmd.parent("L_front_foot_GRP",CTRL[0])
    
    cmd.group(CTRL[1],CTRL[0],"front_poleVector_GRP",n="front_legs_GRP")
    
    
def tail():
    
    #create lists
    LOC = ["pelvis_LOC", "tail001_LOC", "tail002_LOC", "tail003_LOC", "tail004_LOC", "tail005_LOC", "tail006_LOC", "tail007_LOC"]
    JNT = ["pelvis_JNT", "tail001_JNT", "tail002_JNT", "tail003_JNT", "tail004_JNT", "tail005_JNT", "tail006_JNT", "tail007_JNT"]
    CTRL = ["pelvis_CTRL", "tail001_CTRL", "tail002_CTRL", "tail003_CTRL", "tail004_CTRL", "tail005_CTRL", "tail006_CTRL"]
    GEO = ["pelvis_GEO", "tail001_GEO", "tail002_GEO", "tail003_GEO", "tail004_GEO", "tail005_GEO", "tail006_GEO", "tail007_GEO"]
    
    
    #Looping through LOC, get LOC location info and transfer the JNT
    i=0
    
    for each in LOC:
        x=cmd.getAttr(each+".translateX")
        y=cmd.getAttr(each+".translateY")
        z=cmd.getAttr(each+".translateZ")
        cmd.joint(p=(x,y,z),n=JNT[i],rad=0.1)
        i+=1
    
    cmd.select(JNT[0], r=True) #select starting joint
    cmd.parent(JNT[0], w=True)
    cmd.FreezeTransformations()
    cmd.joint(e=True, ch=True, oj='xyz', sao='yup')
    
    #Parenting shoulder joints to pelvis
        
    cmd.parent("L_rear_shldr_JNT",JNT[0])
    cmd.parent("R_rear_shldr_JNT",JNT[0])
    
    #Parenting meshes to joints
    
    i=7
    for each in GEO:
        if(i==0):
            break
        else:
            cmd.parent(GEO[i],JNT[i-1])
            i-=1
    
    #Looping through LOC, get LOC location infor and transfer the CTRL
    i=6
    for each in CTRL:
        x=cmd.getAttr(LOC[i]+".translateX")
        y=cmd.getAttr(LOC[i]+".translateY")
        z=cmd.getAttr(LOC[i]+".translateZ")
        cmd.circle(c=(x,y,z),n=CTRL[i],r=5,nr=(1,0,0))
        cmd.xform(cp=True)
        i-=1

    
    #Parenting and grouping
    i=6
    for each in CTRL:
       if(i==0):
           cmd.pointConstraint(CTRL[i], JNT[i], mo = True)
       else:
           cmd.orientConstraint(CTRL[i], JNT[i], mo = True)
           i-=1
    i=6
    for each in CTRL:
        if(i==0):
            break
        else:
            cmd.parent(CTRL[i],CTRL[i-1])
            i-=1

def spine():
    
    #create lists
    
    LOC = ["root_LOC","spine001_LOC","spine002_LOC","spine003_LOC","chest_LOC","neck_LOC","head_LOC","mouth_LOC"]
    JNT = ["root_JNT","spine001_JNT","spine002_JNT","spine003_JNT","chest_JNT","neck_JNT","head_JNT","mouth_JNT"]
    CTRL = ["root_CTRL","spine001_CTRL","spine002_CTRL","spine003_CTRL","chest_CTRL","neck_CTRL","head_CTRL"]
    GEO = ["pelvis_GEO","root_GEO","spine001_GEO","spine002_GEO","spine003_GEO","chest_GEO","neck_GEO","head_GEO"]
    
    
    #Looping through LOC, get LOC location info and transfer the JNT
    i=0
    
    for each in LOC:
        x=cmd.getAttr(each+".translateX")
        y=cmd.getAttr(each+".translateY")
        z=cmd.getAttr(each+".translateZ")
        cmd.joint(p=(x,y,z),n=JNT[i],rad=0.1)
        i+=1
    cmd.select(JNT[0], r=True) #select starting joint
    cmd.parent(JNT[0], w=True)
    cmd.FreezeTransformations()
    cmd.joint(e=True, ch=True, oj='xyz', sao='yup')
        
    #Parenting front shoulders to chest
        
    cmd.parent("L_front_shldr_JNT",JNT[4])
    cmd.parent("R_front_shldr_JNT",JNT[4])
    cmd.parent("pelvis_JNT",JNT[0])
    
    
    #Parenting meshes to joints
    
    i=7
    for each in GEO:
        if(i==0):
            break
        else:
            cmd.parent(GEO[i],JNT[i-1])
            i-=1
            
    cmd.parent(GEO[0],JNT[0])
        
    #Controllers and IK handles
    i=6
    for each in LOC:
        x=cmd.getAttr(LOC[i]+".translateX")
        y=cmd.getAttr(LOC[i]+".translateY")
        z=cmd.getAttr(LOC[i]+".translateZ")
        cmd.circle(c=(x,y,z),n=CTRL[i],r=8,nr=(1,0,0))
        cmd.xform(cp=True)
        i-=1
    
    cmd.ikHandle(solver="ikSplineSolver",n="spine_IK",sj=JNT[0],ee=JNT[5],snc=True,ccv=True,scv=True,ns=3)
    cmd.select("curve1.cv[5]",r=True)
    cmd.cluster(n="neck_cluster")
    cmd.select("curve1.cv[4]",r=True)
    cmd.cluster(n="chest_cluster")
    cmd.select("curve1.cv[3]",r=True)
    cmd.cluster(n="spine003_cluster")
    cmd.select("curve1.cv[2]",r=True)
    cmd.cluster(n="spine002_cluster")
    cmd.select("curve1.cv[1]",r=True)
    cmd.cluster(n="spine001_cluster")
    cmd.select("curve1.cv[0]",r=True)
    cmd.cluster(n="root_cluster")
    
    #Parenting and grouping
    cmd.parent("root_clusterHandle",CTRL[0])
    cmd.parent("spine001_clusterHandle",CTRL[1])
    cmd.parent("spine002_clusterHandle",CTRL[2])
    cmd.parent("spine003_clusterHandle",CTRL[3])
    cmd.parent("chest_clusterHandle",CTRL[4])
    cmd.parent("neck_clusterHandle",CTRL[5])
    
    i=6
    for each in CTRL:
        if(i==0):
            break
        else:
            cmd.parent(CTRL[i],CTRL[i-1])
            i-=1
    
    cmd.parent("pelvis_CTRL",CTRL[0])
    
    cmd.orientConstraint(CTRL[6], JNT[6], mo = True)
    
    
    cmd.group("front_legs_GRP","rear_legs_GRP",n="legs_GRP")
    cmd.parent("legs_GRP","root_CTRL")
    cmd.group("spine_IK",CTRL[1],n="spine_GRP")
    cmd.parent("spine_GRP","root_CTRL")
    cmd.group("root_CTRL","root_JNT",n="Tiger_GRP")
    cmd.circle(c=(0,0,0),n="Master_CTRL",r=25,nr=(0,1,0))
    cmd.parent("Tiger_GRP","Master_CTRL")
    cmd.group("Master_CTRL",n="TigerA_lodA_GRP")
    
   

front()
rear()
tail()
spine()