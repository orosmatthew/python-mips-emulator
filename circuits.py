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


class MemData:
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


class Memory:
    def __init__(self, mem_data: MemData, mem_write: int, mem_read: int, address: list[int], write_data: list[int]):
        self._mem_data: MemData = mem_data
        self._mem_write: int = mem_write
        self._mem_read: int = mem_read
        self._address: list[int] = address
        self._write_data: list[int] = write_data

    def get_output_read_data(self) -> list[int]:
        return_data: list[int] = [0] * 32
        if self._mem_read == 1:
            return_data = self._mem_data.get_mem_val(self._address)

        if self._mem_write == 1:
            self._mem_data.set_mem_val(self._address, self._write_data)

        return return_data


class RegData:
    def __init__(self, reg_initial_value: list[int]):
        self._regs: list[list[int]] = [reg_initial_value] * 32

    def set_reg_val(self, o_reg_decoder: list[int], value_to_set: list[int]) -> None:
        self._regs[o_reg_decoder.index(1)] = value_to_set

    def get_reg_val(self, o_reg_decoder: list[int]) -> list[int]:
        return self._regs[o_reg_decoder.index(1)]

    def get_all_reg_vals(self) -> list[list[int]]:
        return self._regs


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


class Registry:
    def __init__(self, reg_data: RegData, reg_write: int, read_reg_1: list[int], read_reg_2: list[int],
                 write_reg: list[int], write_data: list[int]):
        self._reg_data: RegData = reg_data
        self._reg_write: int = reg_write
        self._read_reg_1: list[int] = read_reg_1
        self._read_reg_2: list[int] = read_reg_2
        self._write_reg: list[int] = write_reg
        self._write_data: list[int] = write_data

        if self._reg_write == 1:
            reg_dec: RegDecoder = RegDecoder(self._write_reg)
            self._reg_data.set_reg_val(reg_dec.get_output(), self._write_data)

    def get_output_read(self) -> tuple[list[int], list[int]]:
        reg_dec1: RegDecoder = RegDecoder(self._read_reg_1)
        reg_dec2: RegDecoder = RegDecoder(self._read_reg_2)

        read_data: tuple[list[int], list[int]] = (self._reg_data.get_reg_val(reg_dec1.get_output()),
                                                  self._reg_data.get_reg_val(reg_dec2.get_output()))

        if self._reg_write == 1:
            reg_dec_w: RegDecoder = RegDecoder(self._write_reg)
            self._reg_data.set_reg_val(reg_dec_w.get_output(), self._write_data)

        return read_data


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


class AndGate6(BasicCircuit):
    def __init__(self, in1: int, in2: int, in3: int, in4: int, in5: int, in6: int):
        super().__init__(in1, in2)
        self._in3: int = in3
        self._in4: int = in4
        self._in5: int = in5
        self._in6: int = in6

    def get_output(self) -> int:
        andg5_0 = AndGate5(self._in1, self._in2, self._in3, self._in4, self._in5)
        out_andg5_0 = andg5_0.get_output()

        andg_0 = AndGate(out_andg5_0, self._in6)
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


class SignExt:
    def __init__(self, bits16: list[int]):
        self._bits16 = bits16

    def get_output(self) -> list[int]:
        output = [self._bits16[0]] * 16
        output.extend(self._bits16)
        return output


class ALU1Bit:
    def __init__(self, a: int, b: int, func_code: list[int], carry_in: int, less: int):
        self._a: int = a
        self._b: int = b
        self._a_inv: int = func_code[0]
        self._b_inv: int = func_code[1]
        self._carry_in: int = carry_in
        self._op1: int = func_code[2]
        self._op0: int = func_code[3]
        self._less: int = less

    def get_output_result(self) -> int:
        mux_2to1_0 = Mux2To1(self._a, NotGate(self._a).get_output(), self._a_inv)
        mux_2to1_1 = Mux2To1(self._b, NotGate(self._b).get_output(), self._b_inv)

        andg_0 = AndGate(mux_2to1_0.get_output(), mux_2to1_1.get_output()).get_output()
        org_0 = OrGate(mux_2to1_0.get_output(), mux_2to1_1.get_output()).get_output()
        full_adder_0 = FullAdder(mux_2to1_0.get_output(), mux_2to1_1.get_output(), self._carry_in).get_output_sum()

        mux_4to1_0 = Mux4To1(andg_0, org_0, full_adder_0, self._less, self._op0, self._op1)
        return mux_4to1_0.get_output()

    def get_output_overflow(self) -> int:
        result = self.get_output_result()
        not_result = NotGate(self.get_output_result())
        a = self._a
        not_a = NotGate(self._a)
        b = self._b
        not_b = NotGate(self._b)

        andg_1 = AndGate3(not_result.get_output(), a, b)
        andg_2 = AndGate3(result, not_a.get_output(), not_b.get_output())

        org_0 = OrGate(andg_1.get_output(), andg_2.get_output())
        return org_0.get_output()

    def get_output_carry_out(self) -> int:
        mux_2to1_0 = Mux2To1(self._a, NotGate(self._a).get_output(), self._a_inv)
        mux_2to1_1 = Mux2To1(self._b, NotGate(self._b).get_output(), self._b_inv)
        full_adder_0 = FullAdder(mux_2to1_0.get_output(), mux_2to1_1.get_output(), self._carry_in)
        return full_adder_0.get_output_carry()

    def get_output_set(self) -> int:
        mux_2to1_0 = Mux2To1(self._a, NotGate(self._a).get_output(), self._a_inv)
        mux_2to1_1 = Mux2To1(self._b, NotGate(self._b).get_output(), self._b_inv)

        full_adder_0 = FullAdder(mux_2to1_0.get_output(), mux_2to1_1.get_output(), self._carry_in).get_output_sum()
        return full_adder_0


class MainControl:
    def __init__(self, op5: int, op4: int, op3: int, op2: int, op1: int, op0: int):
        self._op0: int = op0
        self._op1: int = op1
        self._op2: int = op2
        self._op3: int = op3
        self._op4: int = op4
        self._op5: int = op5
        self._not_op0: int = NotGate(self._op0).get_output()
        self._not_op1: int = NotGate(self._op1).get_output()
        self._not_op2: int = NotGate(self._op2).get_output()
        self._not_op3: int = NotGate(self._op3).get_output()
        self._not_op4: int = NotGate(self._op4).get_output()
        self._not_op5: int = NotGate(self._op5).get_output()

    def _get_output_r(self) -> int:
        andg_1 = AndGate6(self._not_op0, self._not_op1, self._not_op2, self._not_op3, self._not_op4,
                          self._not_op5).get_output()
        return andg_1

    def _get_output_lw(self) -> int:
        andg_2 = AndGate6(self._op0, self._op1, self._not_op2, self._not_op3, self._not_op4, self._op5).get_output()
        return andg_2

    def get_output_sw(self) -> int:
        andg_3 = AndGate6(self._op0, self._op1, self._not_op2, self._op3, self._not_op4, self._op5).get_output()
        return andg_3

    def _get_output_beq(self) -> int:
        andg_4 = AndGate6(self._not_op0, self._not_op1, self._op2, self._not_op3, self._not_op4,
                          self._not_op5).get_output()
        return andg_4

    def get_reg_dst(self) -> int:
        return self._get_output_r()

    def get_alu_src(self) -> int:
        org_1 = OrGate(self._get_output_lw(), self.get_output_sw()).get_output()
        return org_1

    def get_mem_to_reg(self) -> int:
        return self._get_output_lw()

    def get_reg_write(self) -> int:
        org_2 = OrGate(self._get_output_r(), self._get_output_lw()).get_output()
        return org_2

    def get_mem_read(self) -> int:
        return self._get_output_lw()

    def get_mem_write(self) -> int:
        return self.get_output_sw()

    def get_branch(self) -> int:
        return self._get_output_beq()

    def get_alu_op(self) -> list[int]:
        alu_op = [self._get_output_r(), self._get_output_beq()]
        return alu_op


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
        notg_2 = NotGate(self._alu_op0)
        andg_2 = AndGate(self._alu_op0, notg_2.get_output())
        output= [andg_2.get_output()]

        andg_1 = AndGate(self._f1, self._alu_op1)
        org_2 = OrGate(self._alu_op0, andg_1.get_output())
        output.append(org_2.get_output())

        notg_0 = NotGate(self._f2)
        notg_1 = NotGate(self._alu_op1)
        org_1 = OrGate(notg_0.get_output(),
                       notg_1.get_output())
        output.append(org_1.get_output())

        org_0 = OrGate(self._f0, self._f3)
        andg_0 = AndGate(org_0.get_output(), self._alu_op1)
        output.append(andg_0.get_output())
        return output



class SimpleMIPS:
    def __init__(self, reg_data: RegData, mem_data: MemData):
        self._reg_data: RegData = reg_data
        self._mem_data: MemData = mem_data

    def input_instruction(self, instr: list[int]):

        main_control = MainControl(instr[0], instr[1], instr[2], instr[3], instr[4], instr[5])
        read_reg1 = instr[6:11]
        read_reg2 = instr[11:16]
        rd = instr[16:21]
        imm = instr[16:32]
        func = instr[26:32]

        write_reg = [0] * 5
        for i in range(5):
            mux = Mux2To1(read_reg2[i], rd[i], main_control.get_reg_dst())
            write_reg[i] = mux.get_output()

        sign_ext = SignExt(imm)
        sign_ext_val = sign_ext.get_output()

        regs = Registry(self._reg_data, main_control.get_reg_write(), read_reg1, read_reg2, write_reg, [0] * 32)
        read_data = regs.get_output_read()
        read_data1 = read_data[0]
        read_data2 = read_data[1]
        alu_input_2 = [0] * 32
        for i in range(32):
            mux = Mux2To1(read_data2[i], sign_ext_val[i], main_control.get_alu_src())
            alu_input_2[i] = mux.get_output()

        alu_control = ALUControl(func[5], func[4], func[3], func[2], func[1], func[0], main_control.get_alu_op()[1], main_control.get_alu_op()[0])
        alu_control_out = alu_control.get_output()
        alu = ALU32Bit(read_data1, alu_input_2, alu_control_out[1], alu_control_out)
        alu_result = alu.get_output_result()
        
        
        memory = Memory(self._mem_data, main_control.get_mem_write(), main_control.get_mem_read(), alu_result, read_data2)
        mem_read_data = memory.get_output_read_data()

        write_data = [0] * 32
        for i in range(32):
            mux = Mux2To1(alu_result[i], mem_read_data[i], main_control.get_mem_to_reg())
            write_data[i] = mux.get_output()
        
        regs2 = Registry(self._reg_data, main_control.get_reg_write(), read_reg1, read_reg2, write_reg, write_data)
        regs2.get_output_read()

        
    # regs = Registry()

    def get_reg_data(self) -> RegData:
        return self._reg_data

    def get_mem_data(self) -> MemData:
        return self._mem_data


# m = SimpleMIPS(RegData([0] * 32), MemData(256, [0] * 32, 0))
# m.input_instruction([0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

class ALU32Bit:
    def __init__(self, a: list[int], b: list[int], carry_in: int, alu_ctrl_sig: list[int]):
        self._a: list[int] = a
        self._b: list[int] = b
        self._carry_in: int = carry_in
        self._alu_ctrl_sig: list[int] = alu_ctrl_sig

    def get_output_overflow(self) -> int:
        result = self.get_output_result()[0]
        not_result = NotGate(self.get_output_result()[0])
        not_b = NotGate(self._b[0])
        b_inv = self._alu_ctrl_sig[1]
        not_b_inv = NotGate(b_inv).get_output()
        andg_3 = AndGate(not_b.get_output(), b_inv)
        andg_4 = AndGate(self._b[0], not_b_inv)
        calc_b = OrGate(andg_3.get_output(), andg_4.get_output()).get_output()
        not_calc_b = NotGate(calc_b).get_output()

        not_a = NotGate(self._a[0])

        andg_1 = AndGate3(not_result.get_output(), self._a[0], calc_b)
        andg_2 = AndGate3(result, not_a.get_output(), not_calc_b)

        org_1 = OrGate(andg_1.get_output(), andg_2.get_output())
        return org_1.get_output()

    def get_output_result(self) -> list[int]:

        result: list[int] = [0] * 32

        carry: int = self._carry_in
        alu_set: int = 0
        for i in reversed(range(32)):  # 0 -> 31
            alu = ALU1Bit(self._a[i], self._b[i], self._alu_ctrl_sig, carry, 0)
            carry = alu.get_output_carry_out()
            result[i] = alu.get_output_result()
            alu_set = alu.get_output_set()

        alu = ALU1Bit(self._a[0], self._b[0], self._alu_ctrl_sig, carry, alu_set)
        result[31] = alu.get_output_result()

        return result

    def get_output_zero(self) -> int:
        result: list[int] = [0] * 32

        carry: int = self._carry_in
        alu_set: int = 0
        for i in reversed(range(32)):  # 0 -> 31
            alu = ALU1Bit(self._a[i], self._b[i], self._alu_ctrl_sig, carry, 0)
            carry = alu.get_output_carry_out()
            result[i] = alu.get_output_result()
            alu_set = alu.get_output_set()

        alu = ALU1Bit(self._a[0], self._b[0], self._alu_ctrl_sig, carry, alu_set)
        result[31] = alu.get_output_result()

        return int(any(x == 1 for x in result))


# a = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# b = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# alu32 = ALU32Bit(a, b, 1, [0, 1, 1, 0])
# print(alu32.get_output_result())
# print(alu32.get_output_overflow())


# ALU test code
# test = [0,1,1,0]

# ALU1Bit_0 = ALU1Bit(1,1, test, 0, 0)

# print(ALU1Bit_0.get_output_sum())
# print(ALU1Bit_0.get_output_carry_out())
