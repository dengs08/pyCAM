import re
from statemachine import StateMachine
from treelib import Tree, Node

pblock = re.compile('\S+\s+\S+\s+Description\s*\n\s*-+\n+')
pline = re.compile('.*\n')
pdimension = re.compile('\s([\w]{3,6})\s{8,18}(\d{1,6})\s{11,16}((\S+\s{1,16})+)\s')
pcomment =  re.compile('\s{20,}((\S+\s{1,16})+)\s')
pvariable = re.compile('^\s[\w|\(|\)|,]{1,20}',re.M)
Tree_Dim = Tree()
Tree_Dim.create_node("Dimension","dimension")

def desp_pos(line):
    pos = [m.start() for m in re.finditer('\w+',line)]
    if pos[0] != 1:
        return True,pos[0]
    else:
        return False,pos[2]

def indent_handler(cur_id,cur_tag,last_id,num_dent):
    if num_dent == 1:
        #print(cur_tag, cur_id,last_id)
        cur_id = last_id+"%"+cur_id
        Tree_Dim.create_node(cur_tag, cur_id, parent=last_id)
        last_id = cur_id
        return True,last_id
    else:
        print("Wrong Indentation!\n")
        last_id = cur_id
        return False,last_id

def dedent_handler(cur_id,cur_tag,last_id,num_dent):
    for i in range(num_dent-1,0):
        parent = Tree_Dim.parent(last_id).identifier
        last_id = parent
    Tree_Dim.create_node(cur_tag, cur_id, parent=parent)
    last_id = cur_id 
    return True,last_id

def nodent_handler(cur_id,cur_tag,last_id,num_dent):
    if num_dent == 0:
        parent = Tree_Dim.parent(last_id).identifier
        Tree_Dim.create_node(cur_tag, cur_id, parent=parent)
        
        #print(item[0],current_parent)
        return True,cur_id
    else:
        return False,cur_id

def end_handler(cur_id,cur_tag,last_id,num_dent):
    return True,cur_id
    #return newState

def parse_dimension(line):
    IsPureComment, description_pos = desp_pos(line)
    

if __name__ == "__main__":
    
    sm = StateMachine()
    sm.add_state("Indent", indent_handler)
    sm.add_state("Dedent", dedent_handler)
    sm.add_state("Nodent", nodent_handler)
    sm.add_state("Endent", end_handler,end_state=1)
    
    with open('变量字典.txt','r') as f:
        data = f.read()
    m = pblock.split(data)
    
    Dict_Dim = []

    i,j = 1,1
    ndm = 0
    for rawmatch in m:
        match = re.sub('\n{1,}','\n',rawmatch)
        if i == 1: # 变量字典的说明
            pass
        elif i == 2: # 数组尺寸声明
            lines = pline.findall(match)
            sm.set_start("Dedent")
            sm.handler = sm.handlers[sm.startState]
            for i,line in enumerate(lines):
                
                if i != 0:
                    if description_pos >=20:
                        if description_pos == last_pos:
                            newState = "Nodent"
                        elif description_pos < last_pos:
                            newState = "Dedent"
                        else:
                            newState = "Indent"
                        num_dent = int((description_pos-last_pos)/3)
                    else:
                         newState = "Endent"
                else:
                    newState = "Indent"
                    last_id = "dimension"
                    num_dent = 1
                last_pos = description_pos
                sm.handler = sm.handlers[newState.upper()]
                
                print(newState,line)
                if IsPureComment:
                    dimset = pcomment.match(line)
                    if dimset != None:
                        item = (dimset.group(1).rstrip(), None)
                else:
                    dimset = pdimension.match(line)
                    if dimset != None:         
                        item = (dimset.group(1).strip(),(dimset.group(2)+' '+dimset.group(3).strip()))
                        ndm += 1
                print(newState,num_dent)
                success,last_id = sm.handler(item[0].lower(),item[0],last_id,num_dent)
                
                
        else:
            variables = pvariable.findall(match)
            #print(i-2,':')
            #for variable in variables:
            #    print(variable)
        i += 1
        
    ncomm = len(m)-2    
    print('Number of Commons:',ncomm)
    print('Number of Dimensions:',ndm)    
