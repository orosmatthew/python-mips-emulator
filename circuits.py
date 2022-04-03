__author__ = "Your names"
__Copyright__ =  "Copyright @2022"

from typing import overload

class circuit(object):
    def __init__(self, in1, in2):
        self.in1_ = in1
        self.in2_ = in2


class registerFile(circuit):
    def __init__(self, reg_initial_value):
        pass
    def setRegValue(self, o_reg_decoder, value_to_set):
        pass
    def getRegValue(self, o_reg_decoder):
        pass
    def getAllRegValues(self):
        pass

class andgate(circuit):
    def getCircuitOutput(self):
        if self.in1_ == 1 and self.in2_ == 1:
            return 1
        else:
            return 0

class orgate(circuit):
    def getCircuitOutput(self):
        if self.in1_ == 0 and self.in2_ == 0:
            return 0
        else:
            return 1

class orgate3(circuit):
    def __init__(self, in1, in2, in3):
        self.in1_ = in1
        self.in2_ = in2
        self.in3_ = in3

    def getCircuitOutput(self):
        org0 = orgate(self.in1_, self.in2_)
        out_org0 = org0.getCircuitOutput()

        org1 = orgate(out_org0, self.in3_)
        out_org1 = org1.getCircuitOutput()
        return out_org1

class orgate4(circuit):
    def __init__(self, in1, in2, in3, in4):
        self.in1_ = in1
        self.in2_ = in2
        self.in3_ = in3
        self.in4_ = in4

    def getCircuitOutput(self):
        org0 = orgate(self.in1_, self.in2_)
        out_org0 = org0.getCircuitOutput()

        org1 = orgate(out_org0, self.in3_)
        out_org1 = org1.getCircuitOutput()

        org2 = orgate(out_org1, self.in4_)
        out_org2 = org2.getCircuitOutput()
        return out_org2


class notgate(circuit):
    def __init__(self, in1):
        self.in1_ = in1

    def getCircuitOutput(self):
        if self.in1_ == 1:
            return 0
        elif self.in1_ == 0:
            return 1

#Hint: you may implement some multi-input logic gates to help you build the circuit,
#for example, below is a 3-input andgate3 boolean algebra: Y=ABC
class andgate3(circuit):
    def __init__(self, in1, in2, in3):
        self.in1_ = in1
        self.in2_ = in2
        self.in3_ = in3

    def getCircuitOutput(self):
        andg0 = andgate(self.in1_, self.in2_)
        out_andg0 = andg0.getCircuitOutput()

        andg1 = andgate(out_andg0, self.in3_)
        out_andg1 = andg1.getCircuitOutput()

        return out_andg1


#2to1 mux implemented by notgate, andgates and orgates
class mux_2to1(circuit):
    def __init__(self, d0, d1, s):
        self.d0_ = d0
        self.d1_ = d1
        self.s_ = s

    def getCircuitOutput(self):
        not_s = notgate(self.s_)
        andg0 = andgate(self.d0_, not_s.getCircuitOutput())
        andg1 = andgate(self.d1_,self.s_)
        org0 = orgate(andg0.getCircuitOutput(), andg1.getCircuitOutput())
        out_org0 = org0.getCircuitOutput()
        return out_org0

#mux = mux_2to1(1, 1, 1)
#print(mux.getCircuitOutput())

#4to1 mux implemented by 2to1 muxes
class mux_4to1(circuit):
    def __init__(self, d0, d1, d2, d3, s0, s1):
        self.d0_ = d0
        self.d1_ = d1
        self.d2_ = d2
        self.d3_ = d3
        self.s0_ = s0
        self.s1_ = s1

    def getCircuitOutput(self):
        mux0 = mux_2to1(self.d0_, self.d1_, self.s0_)
        out_mux0 = mux0.getCircuitOutput()
        mux1 = mux_2to1(self.d2_,self.d3_, self.s0_)
        out_mux1 = mux1.getCircuitOutput()
        mux2 = mux_2to1(out_mux0, out_mux1, self.s1_)
        out_mux2 = mux2.getCircuitOutput()
        return out_mux2

#fulladder implemented with logic gates
class fulladder(circuit):
    def __init__(self, a, b, c_in):
        self.a_ = a
        self.b_ = b
        self.c_in_ = c_in

    def getCircuitOutputSum(self):
        
        not_a = notgate(self.a_)
        not_b = notgate(self.b_)
        not_c_in = notgate(self.c_in_)

        andg3_0 = andgate3(not_a.getCircuitOutput(), 
                           not_b.getCircuitOutput(), 
                           self.c_in_)
                           
        andg3_1 = andgate3(not_a.getCircuitOutput(), 
                           self.b_, 
                           not_c_in.getCircuitOutput())

        andg3_2 = andgate3(self.a_, 
                           not_b.getCircuitOutput(), 
                           not_c_in.getCircuitOutput())
                           
        andg3_3 = andgate3(self.a_, 
                           self.b_, 
                           self.c_in_)

        org4_0 = orgate4(andg3_0.getCircuitOutput(), 
                         andg3_1.getCircuitOutput(), 
                         andg3_2.getCircuitOutput(), 
                         andg3_3.getCircuitOutput())
                         
        out_org4_0 = org4_0.getCircuitOutput()
        return out_org4_0

    def getCircuitOutputCarry(self):

        andg_0 = andgate(self.a_, self.b_)
        andg_1 = andgate(self.b_, self.c_in_)
        andg_2 = andgate(self.a_, self.c_in_)

        org3_0 = orgate3(andg_0.getCircuitOutput(), 
                         andg_1.getCircuitOutput(), 
                         andg_2.getCircuitOutput())

        return org3_0.getCircuitOutput()

#1 bit ALU implemented with logic gates
class ALU_1bit(object):
    '''
    Implement a 1-bit ALU by using the above circuits, e.g.,  mux_2to1, fulladder and mux_4to1, etc.
    '''

class aluControl(circuit):
    '''
    Implement the ALU control circuit shown in Figure D.2.2 on page 7 of the slides 10_ALU_Control.pdf.
    There are eight inputs: aluOp1, aluOp2, f5, f4, f3, f2, f1, f0.
    There are four outputs of the circuit, you may put them in a python list and return as a whole.
    '''


class ALU_32bit(object):
    '''
    Implement a 32 bit ALU by using the 1 bit ALU.
    Your 32-bit ALU should be able to compute 32-bit AND, OR, addition, subtraction, slt(set on if less than).
    The inputs are:

    two python lists with lenth 32, e.g.:
    A = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1]
    B = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1],
    please note that bit 0 is at the end of the list, which means that bit 0 of A is A[31], bit 31 of A is A[0], bit 0 of B is B[31] and bit 31 of B is B[0].

    carryIn for the 0th 1-bit ALU, which take care of the bit 0.

    aluctrs, which could be a list of alu control signals:
    aluctrs[0] controls the all the 2to1 mux in each 1-bit ALU for bits of input A,
    aluctrs[1] controls the all the 2to1 mux in each 1-bit ALU for bits of input B.
    aluctrs[2] and aluctrs[3] controls all the 4to1 mux in each 1-bit ALU for choose what as output, 00 choose out from AND, 01 choose out from OR, 10 choose out from adder, 11 choose the less.

    Please note that the carryOut output of each 1-bit ALU except the 31th one should be the carryIn the next 1 bit ALU, you may use for loop here for the computation of the sequential 1-bit ALU.

    And please also note that in order to make slt work, we need to use the sum output from the adder of the 31th 1-bit ALU and make it as the less input of the 0th 1bit ALU.


    '''


