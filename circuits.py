class BasicCircuit(object):
    def __init__(self, in1: int, in2: int):
        self._in1: int = in1
        self._in2: int = in2


def bin32_to_dec(bin32: list[int]) -> int:
    num: int = 0
    for p in range(16):
        if bin32[31 - p] == 1:
            num += pow(2, p)
    return num


class Memory:
    def __init__(self, n_bytes: int, base_addr: list[int], initial_value: int):
        self._memory: list[int] = [initial_value] * n_bytes * 4 * 8
        self._base_addr: list[int] = base_addr

    def set_mem_val(self, addr: list[int], value_to_set: list[int]) -> None:
        index: int = (bin32_to_dec(addr) - bin32_to_dec(self._base_addr)) * 8
        if index < 0 or index > (len(self._memory) - 1):
            print("Invalid memory address!")
            return
        offset: int = index
        for v in value_to_set:
            self._memory[offset] = v
            offset += 1

    def get_mem_val(self, addr: list[int]) -> list[int]:
        index: int = (bin32_to_dec(addr) - bin32_to_dec(self._base_addr)) * 8
        if index < 0 or index > (len(self._memory) - 1):
            print("Invalid memory address!")
            return []
        return self._memory[index:index + 32]


class RegFile:
    def __init__(self, reg_initial_value: list[int]):
        self._regs: list[list[int]] = [reg_initial_value] * 32

    def set_reg_val(self, o_reg_decoder: list[int], value_to_set: list[int]) -> None:
        self._regs[o_reg_decoder.index(1)] = value_to_set

    def get_reg_val(self, o_reg_decoder: list[int]) -> list[int]:
        return self._regs[o_reg_decoder.index(1)]

    def get_all_reg_vals(self) -> list[list[int]]:
        return self._regs


class AndGate(BasicCircuit):
    def get_output(self) -> int:
        if self._in1 == 1 and self._in2 == 1:
            return 1
        else:
            return 0


class OrGate(BasicCircuit):
    def get_output(self) -> int:
        if self._in1 == 0 and self._in2 == 0:
            return 0
        else:
            return 1


class OrGate3(BasicCircuit):
    def __init__(self, in1: int, in2: int, in3: int):
        super().__init__(in1, in2)
        self._in3: int = in3

    def get_output(self) -> int:
        org0 = OrGate(self._in1, self._in2)
        out_org0 = org0.get_output()

        org1 = OrGate(out_org0, self._in3)
        out_org1 = org1.get_output()
        return out_org1


class OrGate4(BasicCircuit):
    def __init__(self, in1: int, in2: int, in3: int, in4: int):
        super().__init__(in1, in2)
        self._in3: int = in3
        self._in4: int = in4

    def get_output(self) -> int:
        org0 = OrGate(self._in1, self._in2)
        out_org0 = org0.get_output()

        org1 = OrGate(out_org0, self._in3)
        out_org1 = org1.get_output()

        org2 = OrGate(out_org1, self._in4)
        out_org2 = org2.get_output()
        return out_org2


class NotGate:
    def __init__(self, in1: int):
        self._in1: int = in1

    def get_output(self) -> int:
        if self._in1 == 1:
            return 0
        else:
            return 1


class AndGate3(BasicCircuit):
    def __init__(self, in1: int, in2: int, in3: int):
        super().__init__(in1, in2)
        self._in3: int = in3

    def get_output(self) -> int:
        andg_0 = AndGate(self._in1, self._in2)
        out_andg_0 = andg_0.get_output()

        andg_1 = AndGate(out_andg_0, self._in3)
        out_andg_1 = andg_1.get_output()

        return out_andg_1


class AndGate4(BasicCircuit):
    def __init__(self, in1: int, in2: int, in3: int, in4: int):
        super().__init__(in1, in2)
        self._in3: int = in3
        self._in4: int = in4

    def get_output(self) -> int:
        andg3_0 = AndGate3(self._in1, self._in2, self._in3)
        out_andg3_0 = andg3_0.get_output()

        andg_0 = AndGate(out_andg3_0, self._in4)
        return andg_0.get_output()


class AndGate5(BasicCircuit):
    def __init__(self, in1: int, in2: int, in3: int, in4: int, in5: int):
        super().__init__(in1, in2)
        self._in3: int = in3
        self._in4: int = in4
        self._in5: int = in5

    def get_output(self) -> int:
        andg4_0 = AndGate4(self._in1, self._in2, self._in3, self._in4)
        out_andg4_0 = andg4_0.get_output()

        andg_0 = AndGate(out_andg4_0, self._in5)
        return andg_0.get_output()


class Mux2To1:
    def __init__(self, d0: int, d1: int, s: int):
        self._d0: int = d0
        self._d1: int = d1
        self._s: int = s

    def get_output(self) -> int:
        not_s = NotGate(self._s)
        andg0 = AndGate(self._d0, not_s.get_output())
        andg1 = AndGate(self._d1, self._s)
        org0 = OrGate(andg0.get_output(), andg1.get_output())
        out_org0 = org0.get_output()
        return out_org0


class Mux4To1:
    def __init__(self, d0: int, d1: int, d2: int, d3: int, s0: int, s1: int):
        self._d0: int = d0
        self._d1: int = d1
        self._d2: int = d2
        self._d3: int = d3
        self._s0: int = s0
        self._s1: int = s1

    def get_output(self) -> int:
        mux0 = Mux2To1(self._d0, self._d1, self._s0)
        out_mux0 = mux0.get_output()
        mux1 = Mux2To1(self._d2, self._d3, self._s0)
        out_mux1 = mux1.get_output()
        mux2 = Mux2To1(out_mux0, out_mux1, self._s1)
        out_mux2 = mux2.get_output()
        return out_mux2


class FullAdder:
    def __init__(self, a: int, b: int, c_in: int):
        self._a: int = a
        self._b: int = b
        self._c_in: int = c_in

    def get_output_sum(self) -> int:
        not_a = NotGate(self._a)
        not_b = NotGate(self._b)
        not_c_in = NotGate(self._c_in)

        andg3_0 = AndGate3(not_a.get_output(),
                           not_b.get_output(),
                           self._c_in)

        andg3_1 = AndGate3(not_a.get_output(),
                           self._b,
                           not_c_in.get_output())

        andg3_2 = AndGate3(self._a,
                           not_b.get_output(),
                           not_c_in.get_output())

        andg3_3 = AndGate3(self._a,
                           self._b,
                           self._c_in)

        org4_0 = OrGate4(andg3_0.get_output(),
                         andg3_1.get_output(),
                         andg3_2.get_output(),
                         andg3_3.get_output())

        out_org4_0 = org4_0.get_output()
        return out_org4_0

    def get_output_carry(self) -> int:
        andg_0 = AndGate(self._a, self._b)
        andg_1 = AndGate(self._b, self._c_in)
        andg_2 = AndGate(self._a, self._c_in)

        org3_0 = OrGate3(andg_0.get_output(),
                         andg_1.get_output(),
                         andg_2.get_output())

        return org3_0.get_output()


class RegDecoder:
    def __init__(self, instr_reg: list[int]):
        self._a: int = instr_reg[0]
        self._b: int = instr_reg[1]
        self._c: int = instr_reg[2]
        self._d: int = instr_reg[3]
        self._e: int = instr_reg[4]

    def get_output(self) -> list[int]:
        not_a = NotGate(self._a)
        out_not_a = not_a.get_output()
        not_b = NotGate(self._b)
        out_not_b = not_b.get_output()
        not_c = NotGate(self._c)
        out_not_c = not_c.get_output()
        not_d = NotGate(self._d)
        out_not_d = not_d.get_output()
        not_e = NotGate(self._e)
        out_not_e = not_e.get_output()

        output = [0] * 32

        andg5_0 = AndGate5(out_not_a, out_not_b, out_not_c, out_not_d, out_not_e)
        output[0] = andg5_0.get_output()
        andg5_1 = AndGate5(out_not_a, out_not_b, out_not_c, out_not_d, self._e)
        output[1] = andg5_1.get_output()
        andg5_2 = AndGate5(out_not_a, out_not_b, out_not_c, self._d, out_not_e)
        output[2] = andg5_2.get_output()
        andg5_3 = AndGate5(out_not_a, out_not_b, out_not_c, self._d, self._e)
        output[3] = andg5_3.get_output()
        andg5_4 = AndGate5(out_not_a, out_not_b, self._c, out_not_d, out_not_e)
        output[4] = andg5_4.get_output()
        andg5_5 = AndGate5(out_not_a, out_not_b, self._c, out_not_d, self._e)
        output[5] = andg5_5.get_output()
        andg5_6 = AndGate5(out_not_a, out_not_b, self._c, self._d, out_not_e)
        output[6] = andg5_6.get_output()
        andg5_7 = AndGate5(out_not_a, out_not_b, self._c, self._d, self._e)
        output[7] = andg5_7.get_output()
        andg5_8 = AndGate5(out_not_a, self._b, out_not_c, out_not_d, out_not_e)
        output[8] = andg5_8.get_output()
        andg5_9 = AndGate5(out_not_a, self._b, out_not_c, out_not_d, self._e)
        output[9] = andg5_9.get_output()
        andg5_10 = AndGate5(out_not_a, self._b, out_not_c, self._d, out_not_e)
        output[10] = andg5_10.get_output()
        andg5_11 = AndGate5(out_not_a, self._b, out_not_c, self._d, self._e)
        output[11] = andg5_11.get_output()
        andg5_12 = AndGate5(out_not_a, self._b, self._c, out_not_d, out_not_e)
        output[12] = andg5_12.get_output()
        andg5_13 = AndGate5(out_not_a, self._b, self._c, out_not_d, self._e)
        output[13] = andg5_13.get_output()
        andg5_14 = AndGate5(out_not_a, self._b, self._c, self._d, out_not_e)
        output[14] = andg5_14.get_output()
        andg5_15 = AndGate5(out_not_a, self._b, self._c, self._d, self._e)
        output[15] = andg5_15.get_output()
        andg5_16 = AndGate5(self._a, out_not_b, out_not_c, out_not_d, out_not_e)
        output[16] = andg5_16.get_output()
        andg5_17 = AndGate5(self._a, out_not_b, out_not_c, out_not_d, self._e)
        output[17] = andg5_17.get_output()
        andg5_18 = AndGate5(self._a, out_not_b, out_not_c, self._d, out_not_e)
        output[18] = andg5_18.get_output()
        andg5_19 = AndGate5(self._a, out_not_b, out_not_c, self._d, self._e)
        output[19] = andg5_19.get_output()
        andg5_20 = AndGate5(self._a, out_not_b, self._c, out_not_d, out_not_e)
        output[20] = andg5_20.get_output()
        andg5_21 = AndGate5(self._a, out_not_b, self._c, out_not_d, self._e)
        output[21] = andg5_21.get_output()
        andg5_22 = AndGate5(self._a, out_not_b, self._c, self._d, out_not_e)
        output[22] = andg5_22.get_output()
        andg5_23 = AndGate5(self._a, out_not_b, self._c, self._d, self._e)
        output[23] = andg5_23.get_output()
        andg5_24 = AndGate5(self._a, self._b, out_not_c, out_not_d, out_not_e)
        output[24] = andg5_24.get_output()
        andg5_25 = AndGate5(self._a, self._b, out_not_c, out_not_d, self._e)
        output[25] = andg5_25.get_output()
        andg5_26 = AndGate5(self._a, self._b, out_not_c, self._d, out_not_e)
        output[26] = andg5_26.get_output()
        andg5_27 = AndGate5(self._a, self._b, out_not_c, self._d, self._e)
        output[27] = andg5_27.get_output()
        andg5_28 = AndGate5(self._a, self._b, self._c, out_not_d, out_not_e)
        output[28] = andg5_28.get_output()
        andg5_29 = AndGate5(self._a, self._b, self._c, out_not_d, self._e)
        output[29] = andg5_29.get_output()
        andg5_30 = AndGate5(self._a, self._b, self._c, self._d, out_not_e)
        output[30] = andg5_30.get_output()
        andg5_31 = AndGate5(self._a, self._b, self._c, self._d, self._e)
        output[31] = andg5_31.get_output()

        return output


class MainControl:
    def __init__(self, op5: int, op4: int, op3: int, op2: int, op1: int, op0: int):
        self._op5: int = op5
        self._op4: int = op4
        self._op3: int = op3
        self._op2: int = op2
        self._op1: int = op1
        self._op0: int = op0

    def get_output_reg_dst(self) -> int:
        pass

    def get_output_branch(self) -> int:
        pass

    def get_output_mem_read(self) -> int:
        pass

    def get_output_mem_reg(self) -> int:
        pass

    def get_output_alu_op0(self) -> int:
        pass

    def get_output_alu_op1(self) -> int:
        pass

    def get_output_mem_write(self) -> int:
        pass

    def get_output_alu_src(self) -> int:
        pass

    def get_output_reg_write(self) -> int:
        pass


class SignExt:
    def __init__(self, bits16: list[int]):
        self._bits16 = bits16

    def get_output(self) -> list[int]:
        output = [self._bits16[0]] * 16
        output.extend(self._bits16)
        return output


class ALU1Bit:
    def __init__(self, a: int, b: int, carry_in: int, op0: int, op1: int):
        self._a: int = a
        self._b: int = b
        self._carry_in: int = carry_in
        self._op0: int = op0
        self._op1: int = op1

    def get_output_sum(self) -> int:
        pass

    def get_output_carry_out(self) -> int:
        pass


class ALUControl:
    def __init__(self, f0: int, f1: int, f2: int, f3: int, f4: int, f5: int, alu_op0: int, alu_op1: int):
        self._f0: int = f0
        self._f1: int = f1
        self._f2: int = f2
        self._f3: int = f3
        self._f4: int = f4
        self._f5: int = f5
        self._alu_op0: int = alu_op0
        self._alu_op1: int = alu_op1

    def get_output(self) -> list[int]:
        org_0 = OrGate(self._f0, self._f3)
        andg_0 = AndGate(org_0.get_output(), self._alu_op1)
        output = [andg_0.get_output()]

        notg_0 = NotGate(self._f2)
        notg_1 = NotGate(self._alu_op1)
        org_1 = OrGate(notg_0.get_output(),
                       notg_1.get_output())
        output.append(org_1.get_output())

        andg_1 = AndGate(self._f1, self._alu_op1)
        org_2 = OrGate(self._alu_op0, andg_1.get_output())
        output.append(org_2.get_output())

        notg_2 = NotGate(self._alu_op0)
        andg_2 = AndGate(self._alu_op0, notg_2.get_output())
        output.append(andg_2.get_output())
        return output


class SimpleMIPS:
    def __init__(self, reg_file: RegFile):
        self._reg_file: RegFile = reg_file

    def input_instruction(self, instr: list[int]):
        pass

    def get_output(self):
        pass


class ALU32Bit:
    def __init__(self, a: list[int], b: list[int], carry_in: int, alu_ctrl_sig: list[int]):
        self._a: list[int] = a
        self._b: list[int] = b
        self._carry_in: int = carry_in
        self._alu_ctrl_sig: list[int] = alu_ctrl_sig

    def get_output_overflow(self) -> int:
        pass

    def get_output_result(self) -> list[int]:
        pass

    def get_output_zero(self) -> int:
        pass

    def get_carry_out(self) -> int:
        pass

    """
    Implement a 32 bit ALU by using the 1 bit ALU.
    Your 32-bit ALU should be able to compute 32-bit AND, OR, addition, subtraction, slt(set on if less than).
    The inputs are:

    two python lists with length 32, e.g.:
    A = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1]
    B = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1],
    please note that bit 0 is at the end of the list, which means that bit 0 of A is A[31], bit 31 of A is A[0], bit 0
    of B is B[31] and bit 31 of B is B[0].

    carryIn for the 0th 1-bit ALU, which take care of the bit 0.

    aluctrs, which could be a list of alu control signals:
    aluctrs[0] controls the all the 2to1 mux in each 1-bit ALU for bits of input A,
    aluctrs[1] controls the all the 2to1 mux in each 1-bit ALU for bits of input B.
    aluctrs[2] and aluctrs[3] controls all the 4to1 mux in each 1-bit ALU for choose what as output, 00 choose out from
    AND, 01 choose out from OR, 10 choose out from adder, 11 choose the less.

    Please note that the carryOut output of each 1-bit ALU except the 31st one should be the carryIn the next 1 bit ALU,
    you may use for loop here for the computation of the sequential 1-bit ALU.

    And please also note that in order to make slt work, we need to use the sum output from the adder of the 31st 1-bit
    ALU and make it as the less input of the 0th 1bit ALU.
    """
