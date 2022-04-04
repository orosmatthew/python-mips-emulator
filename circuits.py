__author__ = "Your names"
__Copyright__ = "Copyright @2022"

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

# Hint: you may implement some multi-input logic gates to help you build the circuit,
# for example, below is a 3-input andgate3 boolean algebra: Y=ABC


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


class andgate4(circuit):
    def __init__(self, in1, in2, in3, in4):
        self.in1_ = in1
        self.in2_ = in2
        self.in3_ = in3
        self.in4_ = in4

    def getCircuitOutput(self):
        andg3_0 = andgate3(self.in1_, self.in2_, self.in3_)
        out_andg3_0 = andg3_0.getCircuitOutput()

        andg_0 = andgate(out_andg3_0, self.in4_)
        return andg_0.getCircuitOutput()


class andgate5(circuit):
    def __init__(self, in1, in2, in3, in4, in5):
        self.in1_ = in1
        self.in2_ = in2
        self.in3_ = in3
        self.in4_ = in4
        self.in5_ = in5

    def getCircuitOutput(self):
        andg4_0 = andgate4(self.in1_, self.in2_, self.in3_, self.in4_)
        out_andg4_0 = andg4_0.getCircuitOutput()

        andg_0 = andgate(out_andg4_0, self.in5_)
        return andg_0.getCircuitOutput()

# 2to1 mux implemented by notgate, andgates and orgates


class mux_2to1(circuit):
    def __init__(self, d0, d1, s):
        self.d0_ = d0
        self.d1_ = d1
        self.s_ = s

    def getCircuitOutput(self):
        not_s = notgate(self.s_)
        andg0 = andgate(self.d0_, not_s.getCircuitOutput())
        andg1 = andgate(self.d1_, self.s_)
        org0 = orgate(andg0.getCircuitOutput(), andg1.getCircuitOutput())
        out_org0 = org0.getCircuitOutput()
        return out_org0

#mux = mux_2to1(1, 1, 1)
# print(mux.getCircuitOutput())

# 4to1 mux implemented by 2to1 muxes


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
        mux1 = mux_2to1(self.d2_, self.d3_, self.s0_)
        out_mux1 = mux1.getCircuitOutput()
        mux2 = mux_2to1(out_mux0, out_mux1, self.s1_)
        out_mux2 = mux2.getCircuitOutput()
        return out_mux2

# fulladder implemented with logic gates


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


class decoderReg(circuit):
    def __init__(self, instr_reg_filed):
        self.a_ = instr_reg_filed[0]
        self.b_ = instr_reg_filed[1]
        self.c_ = instr_reg_filed[2]
        self.d_ = instr_reg_filed[3]
        self.e_ = instr_reg_filed[4]

    def getCircuitOutput(self):
        not_a = notgate(self.a_)
        out_not_a = not_a.getCircuitOutput()
        not_b = notgate(self.b_)
        out_not_b = not_b.getCircuitOutput()
        not_c = notgate(self.c_)
        out_not_c = not_c.getCircuitOutput()
        not_d = notgate(self.d_)
        out_not_d = not_d.getCircuitOutput()
        not_e = notgate(self.e_)
        out_not_e = not_e.getCircuitOutput()

        output = [0] * 32

        andg5_0 = andgate5(out_not_a, out_not_b,
                           out_not_c, out_not_d, out_not_e)
        output[0] = andg5_0.getCircuitOutput()
        andg5_1 = andgate5(out_not_a, out_not_b, out_not_c, out_not_d, self.e_)
        output[1] = andg5_1.getCircuitOutput()
        andg5_2 = andgate5(out_not_a, out_not_b, out_not_c, self.d_, out_not_e)
        output[2] = andg5_2.getCircuitOutput()
        andg5_3 = andgate5(out_not_a, out_not_b, out_not_c, self.d_, self.e_)
        output[3] = andg5_3.getCircuitOutput()
        andg5_4 = andgate5(out_not_a, out_not_b, self.c_, out_not_d, out_not_e)
        output[4] = andg5_4.getCircuitOutput()
        andg5_5 = andgate5(out_not_a, out_not_b, self.c_, out_not_d, self.e_)
        output[5] = andg5_5.getCircuitOutput()
        andg5_6 = andgate5(out_not_a, out_not_b, self.c_, self.d_, out_not_e)
        output[6] = andg5_6.getCircuitOutput()
        andg5_7 = andgate5(out_not_a, out_not_b, self.c_, self.d_, self.e_)
        output[7] = andg5_7.getCircuitOutput()
        andg5_8 = andgate5(out_not_a, self.b_, out_not_c, out_not_d, out_not_e)
        output[8] = andg5_8.getCircuitOutput()
        andg5_9 = andgate5(out_not_a, self.b_, out_not_c, out_not_d, self.e_)
        output[9] = andg5_9.getCircuitOutput()
        andg5_10 = andgate5(out_not_a, self.b_, out_not_c, self.d_, out_not_e)
        output[10] = andg5_10.getCircuitOutput()
        andg5_11 = andgate5(out_not_a, self.b_, out_not_c, self.d_, self.e_)
        output[11] = andg5_11.getCircuitOutput()
        andg5_12 = andgate5(out_not_a, self.b_, self.c_, out_not_d, out_not_e)
        output[12] = andg5_12.getCircuitOutput()
        andg5_13 = andgate5(out_not_a, self.b_, self.c_, out_not_d, self.e_)
        output[13] = andg5_13.getCircuitOutput()
        andg5_14 = andgate5(out_not_a, self.b_, self.c_, self.d_, out_not_e)
        output[14] = andg5_14.getCircuitOutput()
        andg5_15 = andgate5(out_not_a, self.b_, self.c_, self.d_, self.e_)
        output[15] = andg5_15.getCircuitOutput()
        andg5_16 = andgate5(self.a_, out_not_b, out_not_c,
                            out_not_d, out_not_e)
        output[16] = andg5_16.getCircuitOutput()
        andg5_17 = andgate5(self.a_, out_not_b, out_not_c, out_not_d, self.e_)
        output[17] = andg5_17.getCircuitOutput()
        andg5_18 = andgate5(self.a_, out_not_b, out_not_c, self.d_, out_not_e)
        output[18] = andg5_18.getCircuitOutput()
        andg5_19 = andgate5(self.a_, out_not_b, out_not_c, self.d_, self.e_)
        output[19] = andg5_19.getCircuitOutput()
        andg5_20 = andgate5(self.a_, out_not_b, self.c_, out_not_d, out_not_e)
        output[20] = andg5_20.getCircuitOutput()
        andg5_21 = andgate5(self.a_, out_not_b, self.c_, out_not_d, self.e_)
        output[21] = andg5_21.getCircuitOutput()
        andg5_22 = andgate5(self.a_, out_not_b, self.c_, self.d_, out_not_e)
        output[22] = andg5_22.getCircuitOutput()
        andg5_23 = andgate5(self.a_, out_not_b, self.c_, self.d_, self.e_)
        output[23] = andg5_23.getCircuitOutput()
        andg5_24 = andgate5(self.a_, self.b_, out_not_c, out_not_d, out_not_e)
        output[24] = andg5_24.getCircuitOutput()
        andg5_25 = andgate5(self.a_, self.b_, out_not_c, out_not_d, self.e_)
        output[25] = andg5_25.getCircuitOutput()
        andg5_26 = andgate5(self.a_, self.b_, out_not_c, self.d_, out_not_e)
        output[26] = andg5_26.getCircuitOutput()
        andg5_27 = andgate5(self.a_, self.b_, out_not_c, self.d_, self.e_)
        output[27] = andg5_27.getCircuitOutput()
        andg5_28 = andgate5(self.a_, self.b_, self.c_, out_not_d, out_not_e)
        output[28] = andg5_28.getCircuitOutput()
        andg5_29 = andgate5(self.a_, self.b_, self.c_, out_not_d, self.e_)
        output[29] = andg5_29.getCircuitOutput()
        andg5_30 = andgate5(self.a_, self.b_, self.c_, self.d_, out_not_e)
        output[30] = andg5_30.getCircuitOutput()
        andg5_31 = andgate5(self.a_, self.b_, self.c_, self.d_, self.e_)
        output[31] = andg5_31.getCircuitOutput()

        return output

# 1 bit ALU implemented with logic gates


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
