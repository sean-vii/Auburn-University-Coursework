'''
Adapted from: Dr. Akond Rahman
Python variable tracking
Source: https://docs.python.org/3/library/ast.html
'''
import ast
import os
import pandas as pd


def getBinOpDetails(assiTarget, assiValue, element_type = 'SINGLE_ASSIGNMENT' ):
    '''
    Takes care of element_type = 'SINGLE_ASSIGNMENT', such as, a = 5. Returns an AST node in the form
    of 'a= 5'
    '''

    lhs_var, rhs_var = '', ''
    var_assignment_list = []

    for target in assiTarget:
        if isinstance(target, ast.Name):
            lhs_var = target.id
    if isinstance(assiValue, ast.BinOp):
        operands =  assiValue.left , assiValue.right
        for op_ in operands:
            if(isinstance( op_ , ast.Name ) ):
                rhs_var = rhs_var + "," + op_.id
    elif isinstance(assiValue, ast.Constant):
        rhs_var = assiValue.value
    if len(lhs_var) > 0:
        var_assignment_list = [( lhs_var, rhs_var , element_type  ) ]
    return var_assignment_list

def getTupAssiDetails(assiTargets, assiValue, element_type = 'TUPLE_ASSIGNMENT' ):
    '''
    Takes care of element_type = 'TUPLE_ASSIGNMENT', such as, a, b, c = 5, 10, -1. Returns an AST node in the form
    of 'a, b, c= 5, 10, -1'
    '''
    var_assignment_list = []
    if  isinstance(assiValue, ast.Tuple) and isinstance(assiTargets, list):
        target_ = assiTargets[0]
        name_var_as_tuple_dict  =  target_.__dict__
        value_var_as_tuple_dict =  assiValue.__dict__

        name_var_ls, value_var_ls = name_var_as_tuple_dict['elts'], value_var_as_tuple_dict['elts']
        if len(name_var_ls) == len(value_var_ls):
            for name, value in zip(name_var_ls, value_var_ls):
                var_name = ''
                var_value = ''

                if isinstance(value, ast.Constant):      # Python 3.8+
                    var_value = value.value
                elif isinstance(value, ast.Num):         # Older Python
                    var_value = value.n
                elif isinstance(value, ast.Str):         # Older Python
                    var_value = value.s
                elif isinstance(value, ast.Name):
                    var_value = value.id

                if isinstance(name, ast.Name):
                    var_name = name.id

                var_assignment_list.append((var_name, var_value, element_type))
    return var_assignment_list

def getCommonAssiDetails(assignDict, elemType):
    assignTargets, assignValue = assignDict['targets'], assignDict['value']
    var_details_bin  = getBinOpDetails( assignTargets, assignValue , elemType )
    var_details_tup  = getTupAssiDetails( assignTargets, assignValue , elemType )
    return var_details_bin, var_details_tup

def getVariables(tree_, elemTypeParam):
    '''
    Input: Python parse tree object and the type of elements we want to extract
    Output: All expressions as list of tuples
    '''
    final_list  = []
    for stmt_ in tree_.body:
        for node_ in ast.walk(stmt_):
            assignDict = node_.__dict__
            if isinstance(node_, ast.Assign)  :
                bin_res, tup_res = getCommonAssiDetails( assignDict, elemTypeParam )
                if len(bin_res) > 0:
                    final_list = final_list + bin_res
                if len(tup_res) > 0:
                    final_list = final_list + tup_res
            elif isinstance(node_, ast.AugAssign):
                temp = []
                assignTarget, assignValue = assignDict['target'], assignDict['value']
                temp.append( assignTarget )
                var_details = getBinOpDetails( temp , assignValue )
                final_list = final_list + var_details
    return final_list

def getFunctionAssignments(full_tree):
    call_list = []
    for stmt_ in full_tree.body:
        for node_ in ast.walk(stmt_):
            if isinstance(node_, ast.Assign):
                lhs = ''
                assign_dict = node_.__dict__
                targets, value  =  assign_dict['targets'], assign_dict['value']
                if isinstance(value, ast.Call):
                    funcDict = value.__dict__
                    funcName, funcArgs, funcLineNo =  funcDict['func'], funcDict['args'], funcDict['lineno']
                    for target in targets:
                        if( isinstance(target, ast.Name) ):
                            lhs = target.id
                    for x_ in range(len(funcArgs)):
                        funcArg = funcArgs[x_]
                        if( isinstance(funcArg, ast.Name ) ) and ( isinstance(funcName, ast.Name ) ):
                            call_list.append( ( lhs, funcName.id, funcArg.id, 'FUNC_CALL_ARG:' + str(x_ + 1) )  )
    return call_list

def giveVarsInIf(body_):
    var_list = []
    assign_dict = body_.__dict__
    if (isinstance( body_, ast.IfExp )  or isinstance( body_, ast.If )):
        if 'body' in assign_dict:
            ifbody  = assign_dict['body']
            for bod_elem in ifbody:
                if isinstance(bod_elem, ast.Assign ):
                    assignDict = bod_elem.__dict__
                    bin_res, tup_res = getCommonAssiDetails( assignDict, 'FUNC_VAR_ASSIGNMENT' )
                    if len(bin_res) > 0:
                        var_list = var_list + bin_res
                    if len(tup_res) > 0:
                        var_list = var_list + tup_res
        elif 'orelse' in assign_dict:
            orlesebody  = assign_dict['orelse']
            var_list =  giveVarsInIf( orlesebody )
        return var_list
    else:
        return var_list




def getFunctionDefinitions(path2program):
    call_sequence_ls = []
    func_var_list = []
    if os.path.exists(path2program):
        full_tree = ast.parse( open( path2program  ).read() )
        for stmt_ in full_tree.body:
            for node_ in ast.walk(stmt_):
                if isinstance(node_, ast.FunctionDef):
                    func_def_dict = node_.__dict__
                    func_name, func_args, func_body_parts = func_def_dict['name'], func_def_dict['args'], func_def_dict['body']
                    if(isinstance( func_args, ast.arguments )):
                        arg_index = 1
                        args = func_args.__dict__['args']
                        for arg_ in args:
                            call_sequence_ls.append( (func_name, arg_.__dict__['arg'], 'FUNC_DEFI:' + str(arg_index) ) )
                            arg_index = arg_index + 1
                    for body_ in func_body_parts:
                        assign_dict = body_.__dict__
                        if (isinstance( body_, ast.Assign )):
                            func_var_list = func_var_list + getBinOpDetails( assign_dict['targets'], assign_dict['value'], 'FUNC_SINGLE_ASSIGNMENT' )
                        elif (isinstance( body_, ast.IfExp )  or isinstance( body_, ast.If )):
                            func_var_list = func_var_list + giveVarsInIf(  body_ )



    return call_sequence_ls, func_var_list


def trackTaint(val2track, df_list_param):
    var_, call_, func_def, func_var = df_list_param[0], df_list_param[1], df_list_param[2], df_list_param[3]

    # Step 1: find the variable directly assigned val2track (e.g. input1 = 1000)
    source_var = var_[var_['RHS'] == val2track].iloc[0]['LHS']

    # Step 2: find the variable assigned from source_var (e.g. val1 = input1)
    next_var = var_[var_['RHS'] == source_var].iloc[0]['LHS']

    # Step 3: find the function call where next_var is an argument
    call_row = call_[call_['ARG_NAME'] == next_var].iloc[0]
    func_name = call_row['FUNC_NAME']
    arg_pos   = call_row['TYPE'].split(':')[1]

    # Step 4: find the parameter name in the function definition at that position
    param_var = func_def[(func_def['FUNC_NAME'] == func_name) &
                         (func_def['TYPE'] == 'FUNC_DEFI:' + arg_pos)].iloc[0]['ARG_NAME']

    # Step 5: find the result variable inside the function that uses param_var
    result_var = func_var[func_var['RHS'].astype(str).str.contains(r'\b' + param_var + r'\b')].iloc[0]['LHS']

    print('->'.join([str(val2track), source_var, next_var, param_var, result_var]))



def checkFlow(data, code):
    full_tree = None
    if os.path.exists( code ):
       full_tree = ast.parse( open( code  ).read() )
       fullVarList = getVariables(full_tree, 'VAR_ASSIGNMENT')
       call_list = getFunctionAssignments( full_tree )
       funcDefList, funcvarList = getFunctionDefinitions( code  )
       var_df       = pd.DataFrame( fullVarList, columns =['LHS', 'RHS', 'TYPE']  )
       print(var_df.head())
       call_df      = pd.DataFrame( call_list, columns =['LHS', 'FUNC_NAME', 'ARG_NAME', 'TYPE']   )
       print(call_df.head())
       func_def_df  = pd.DataFrame( funcDefList, columns =['FUNC_NAME', 'ARG_NAME', 'TYPE']   )
       print(func_def_df.head())
       func_var_df  = pd.DataFrame( funcvarList, columns =['LHS', 'RHS', 'TYPE']   )
       print(func_var_df.head())
       info_df_list = [var_df, call_df, func_def_df, func_var_df]
       trackTaint( data , info_df_list )





if __name__=='__main__':
    input_program = 'calc.py'
    data2track    = 1000
    checkFlow( data2track, input_program )
