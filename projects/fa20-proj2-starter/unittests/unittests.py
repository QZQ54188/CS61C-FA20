from unittest import TestCase
from framework import AssemblyTest, print_coverage


class TestAbs(TestCase):
    def test_zero(self):
        t = AssemblyTest(self, "abs.s")
        # load 0 into register a0
        t.input_scalar("a0", 0)
        # call the abs function
        t.call("abs")
        # check that after calling abs, a0 is equal to 0 (abs(0) = 0)
        t.check_scalar("a0", 0)
        # generate the `assembly/TestAbs_test_zero.s` file and run it through venus
        t.execute()

    def test_one(self):
        # same as test_zero, but with input 1
        t = AssemblyTest(self, "abs.s")
        t.input_scalar("a0", 1)
        t.call("abs")
        t.check_scalar("a0", 1)
        t.execute()

    def test_minus_one(self):
        t = AssemblyTest(self, "abs.s")
        t.input_scalar("a0", -1)
        t.call("abs")
        t.check_scalar("a0", 1)
        t.execute()

    @classmethod
    def tearDownClass(cls):
        print_coverage("abs.s", verbose=False)


class TestRelu(TestCase):
    def test_simple(self):
        t = AssemblyTest(self, "relu.s")
        # create an array in the data section
        array0 = t.array([1, -2, 3, -4, 5, -6, 7, -8, 9])
        # load address of `array0` into register a0
        t.input_array("a0", array0)
        # set a1 to the length of our array
        t.input_scalar("a1", len(array0))
        # call the relu function
        t.call("relu")
        # check that the array0 was changed appropriately
        t.check_array(array0, [1, 0, 3, 0, 5, 0, 7, 0, 9])
        # generate the `assembly/TestRelu_test_simple.s` file and run it through venus
        t.execute()

    def test_length_1(self):
        # load the test for relu.s
        t = AssemblyTest(self, "relu.s")
        # create an array in the data section
        array0 = t.array([-1])
        # load address of `array0` into register a0
        t.input_array("a0", array0)
        # set a1 to the length of our array
        t.input_scalar("a1", len(array0))
        # call the `relu` function
        t.call("relu")
        # check that the array0 was changed appropriately
        t.check_array(array0, [0])
        # generate the `assembly/TestRelu_test_simple.s` file and run it through venus
        t.execute()

    def test_invalid_n(self):
        t = AssemblyTest(self, "relu.s")
        # set a1 to an invalid length of array
        t.input_scalar("a1", -1)
        # call the `relu` function
        t.call("relu")
        # generate the `assembly/TestRelu_test_invalid_n.s` file and run it through venus
        t.execute(code=78)


    @classmethod
    def tearDownClass(cls):
        print_coverage("relu.s", verbose=False)


class TestArgmax(TestCase):
    def test_simple(self):
        t = AssemblyTest(self, "argmax.s")
        # create an array in the data section
        array = t.array([3, 1, 7, 4, 2])
        # load address of the array into register a0
        t.input_array("a0", array)
        # set a1 to the length of the array
        t.input_scalar("a1", 5)
        # call the `argmax` function
        t.call("argmax")
        # check that the register a0 contains the correct output
        t.check_scalar("a0", 2)
        # generate the `assembly/TestArgmax_test_simple.s` file and run it through venus
        t.execute()
    
    def test_standard(self):
        t = AssemblyTest(self, "argmax.s")
        # create an array in the data section
        array0 = t.array([3, -42, 432, 7, -5, 6, 5, -114, 2])
        # load address of the array into register a0
        t.input_array("a0", array0)
        # set a1 to the length of the array
        t.input_scalar("a1", len(array0))
        # call the `argmax` function
        t.call("argmax")
        # check that the register a0 contains the correct output
        t.check_scalar("a0", 2)
        # generate the `assembly/TestArgmax_test_simple.s` file and run it through venus
        t.execute()

    def test_length_1(self):
        t = AssemblyTest(self, "argmax.s")
        # create an array in the data section
        array0 = t.array([3])
        # load address of the array into register a0
        t.input_array("a0", array0)
        # set a1 to the length of the array
        t.input_scalar("a1", len(array0))
        # call the `argmax` function
        t.call("argmax")
        # check that the register a0 contains the correct output
        t.check_scalar("a0", 0)
        # generate the `assembly/TestArgmax_test_simple.s` file and run it through venus
        t.execute()

    def test_invalid_n(self):
        t = AssemblyTest(self, "argmax.s")
        # set a1 to an invalid length of the array
        t.input_scalar("a1", 0)
        # call the `argmax` function
        t.call("argmax")
        # generate the `assembly/TestArgmax_test_invalid_n.s` file and run it through venus
        t.execute(code=77)

    @classmethod
    def tearDownClass(cls):
        print_coverage("argmax.s", verbose=False)


class TestDot(TestCase):
    def test_simple(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        array1 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        array2 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        # load array addresses into argument registers
        t.input_array("a0", array1)
        t.input_array("a1", array2)
        # load array attributes into argument registers
        t.input_scalar("a2", 9)
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 1) 
        # call the `dot` function
        t.call("dot")
        # check the return value
        t.check_scalar("a0", 285)
        t.execute()

    def test_stride(self):
        t = AssemblyTest(self, "dot.s")
        v0 = t.array([1, 2, 3])
        v1 = t.array([1, 0, 3, 0, 5, 0])
        t.input_array("a0", v0)
        t.input_array("a1", v1)
        t.input_scalar("a2", 3)
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 2)
        t.call("dot")
        t.check_scalar("a0", 22)
        t.execute()

    def test_length_1(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        v0 = t.array([9])
        v1 = t.array([1])
        # load array addresses into argument registers
        t.input_array("a0", v0)
        t.input_array("a1", v1)
        # load array attributes into argument registers
        t.input_scalar("a2", 1)
        t.input_scalar("a3", 1)
        t.input_scalar("a4", 1)
        # call the `dot` function
        t.call("dot")
        # check the return value
        t.check_scalar("a0", 9)
        t.execute()

    def test_stride_error1(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        v0 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        v1 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        # load array addresses into argument registers
        t.input_array("a0", v0)
        t.input_array("a1", v1)
        # load array attributes into argument registers
        t.input_scalar("a2", 3)
        t.input_scalar("a3", 0)
        t.input_scalar("a4", 2)
        # call the `dot` function
        t.call("dot")
        t.execute(code=76)

    def test_stride_error2(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        v0 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        v1 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        # load array addresses into argument registers
        t.input_array("a0", v0)
        t.input_array("a1", v1)
        # load array attributes into argument registers
        t.input_scalar("a2", 3)
        t.input_scalar("a3", 2)
        t.input_scalar("a4", 0)
        # call the `dot` function
        t.call("dot")
        t.execute(code=76)

    def test_length_error(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        v0 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        v1 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        # load array addresses into argument registers
        t.input_array("a0", v0)
        t.input_array("a1", v1)
        # load array attributes into argument registers
        t.input_scalar("a2", 0)
        t.input_scalar("a3", 2)
        t.input_scalar("a4", 1)
        # call the `dot` function
        t.call("dot")
        t.execute(code=75)

    def test_length_error2(self):
        t = AssemblyTest(self, "dot.s")
        # create arrays in the data section
        v0 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        v1 = t.array([1, 2, 3, 4, 5, 6, 7, 8, 9])
        # load array addresses into argument registers
        t.input_array("a0", v0)
        t.input_array("a1", v1)
        # load array attributes into argument registers
        t.input_scalar("a2", -1)
        t.input_scalar("a3", 2)
        t.input_scalar("a4", 1)
        # call the `dot` function
        t.call("dot")
        t.execute(code=75)


    @classmethod
    def tearDownClass(cls):
        print_coverage("dot.s", verbose=False)


class TestMatmul(TestCase):

    def do_matmul(self, m0, m0_rows, m0_cols, m1, m1_rows, m1_cols, result, code=0):
        t = AssemblyTest(self, "matmul.s")
        # we need to include (aka import) the dot.s file since it is used by matmul.s
        t.include("dot.s")

        # create arrays for the arguments and to store the result
        array0 = t.array(m0)
        array1 = t.array(m1)
        array_out = t.array([0] * len(result))

        # load address of input matrices and set their dimensions
        t.input_array("a0", array0)  # load m0's address
        t.input_scalar("a1", m0_rows)  # load m0's rows
        t.input_scalar("a2", m0_cols)  # load m0's columns
        # load address of output array
        t.input_array("a3", array1)  # load m1's address
        t.input_scalar("a4", m1_rows)  # load m1's rows
        t.input_scalar("a5", m1_cols)  # load m1's columns
        # call the matmul function
        t.input_array("a6", array_out)  # load d's address

        t.call("matmul")

        # check the content of the output array
        t.check_array(array_out, result)

        # generate the assembly file and run it through venus, we expect the simulation to exit with code `code`
        t.execute(code=code)

    def test_simple(self):
        self.do_matmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [30, 36, 42, 66, 81, 96, 102, 126, 150]
        )

    def test_length_1(self):
        self.do_matmul(
            [4], 1, 1,
            [5], 1, 1,
            [20]
        )

    def test_zero_dim_m0(self):
        self.do_matmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 0, 3,
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [0, 0, 0, 0, 0, 0, 0, 0, 0], # result does not matter
            code=72
        )

    def test_negative_dim_m0_y(self):
        self.do_matmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, -1,
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # result does not matter
            code=72
        )

    def test_negative_dim_m0_x(self):
        self.do_matmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9], -1, 3,
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # result does not matter
            code=72
        )

    def test_zero_dim_m1(self):
        self.do_matmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 0, 3,
            [0, 0, 0, 0, 0, 0, 0, 0, 0], # result does not matter
            code=73
        )

    def test_negative_dim_m1_y(self):
        self.do_matmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, -1,
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # result does not matter
            code=73
        )

    def test_negative_dim_m1_x(self):
        self.do_matmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [1, 2, 3, 4, 5, 6, 7, 8, 9], -1, 3,
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # result does not matter
            code=73
        )

    def test_unmatched_dims(self):
        self.do_matmul(
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 2,
            [1, 2, 3, 4, 5, 6, 7, 8, 9], 3, 3,
            [0, 0, 0, 0, 0, 0, 0, 0, 0],  # result does not matter
            code=74
        )

    

    @classmethod
    def tearDownClass(cls):
        print_coverage("matmul.s", verbose=False)


class TestReadMatrix(TestCase):

    def doReadMatrix(self, input_file = "inputs/test_read_matrix/test_input.bin",
     result_row = 3, result_col = 3, result_array = [1, 2, 3, 4, 5, 6, 7, 8, 9], fail='', code=0):
        t = AssemblyTest(self, "read_matrix.s")
        # load address to the name of the input file into register a0
        t.input_read_filename("a0", input_file)

        # allocate space to hold the rows and cols output parameters
        rows = t.array([-1])
        cols = t.array([-1])

        # load the addresses to the output parameters into the argument registers
        t.input_array("a1", rows)
        t.input_array("a2", cols)

        # call the main function within test_read_matrix_no_cc, which randomizes registers and calls read_matrix
        t.call("read_matrix")

        # check the output from the function
        t.check_array(rows, [result_row])
        t.check_array(cols, [result_col])
        t.check_array_pointer("a0", result_array)

        # generate assembly and run it through venus
        t.execute(fail=fail, code=code)

    def test_simple_read(self):
        self.doReadMatrix()

    def test_simple0(self):
        self.doReadMatrix(input_file = "inputs/simple0/bin/inputs/input2.bin", result_row = 3,
         result_col = 1, result_array= [2, 1, 6])


    def test_simple(self):
        self.doReadMatrix()


    def test_fail_fopen(self):
        self.doReadMatrix(fail='fopen', code=90)

    def test_fail_fread(self):
        self.doReadMatrix(fail='fread', code=91)

    def test_fail_fclose(self):
        self.doReadMatrix(fail='fclose', code=92)

    def test_fail_malloc(self):
        self.doReadMatrix(fail='malloc', code=88)

    @classmethod
    def tearDownClass(cls):
        print_coverage("read_matrix.s", verbose=False)


class TestWriteMatrix(TestCase):

    def do_write_matrix(self, fail='', code=0):
        t = AssemblyTest(self, "write_matrix.s")
        outfile = "outputs/test_write_matrix/student.bin"
        # load output file name into a0 register
        t.input_write_filename("a0", outfile)
        # load input array and other arguments
        t.input_array("a1", t.array([1, 2, 3, 4, 5, 6, 7, 8, 9]))
        t.input_scalar("a2", 3)  # rows
        t.input_scalar("a3", 3)  # columns
        # call `write_matrix` function
        t.call("write_matrix")
        # generate assembly and run it through venus
        t.execute(fail=fail, code=code)
        # compare the output file against the reference
        if code == 0:
            t.check_file_output(outfile, "outputs/test_write_matrix/reference.bin")

    def test_simple(self):
        self.do_write_matrix()

    def test_fail_fopen(self):
        self.do_write_matrix(fail='fopen', code=93)

    def test_fail_fwrite(self):
        self.do_write_matrix(fail='fwrite', code=94)

    def test_fail_fclose(self):
        self.do_write_matrix(fail='fclose', code=95)

    @classmethod
    def tearDownClass(cls):
        print_coverage("write_matrix.s", verbose=False)


class TestClassify(TestCase):

    def make_test(self):
        t = AssemblyTest(self, "classify.s")
        t.include("argmax.s")
        t.include("dot.s")
        t.include("matmul.s")
        t.include("read_matrix.s")
        t.include("relu.s")
        t.include("write_matrix.s")
        return t

    def run_classify(self, input_dir, input, output_id, msg: str = "", fail='', code=0):
        t = self.make_test()
        output_dir = "outputs/test_basic_main"
        outfile = f"{output_dir}/student{output_id}.bin"
        args = [f"{input_dir}/m0.bin", f"{input_dir}/m1.bin", f"{input_dir}/inputs/{input}", outfile]
        silent = len(msg) == 0
        t.input_scalar("a2", 1 if silent else 0)
        t.call("classify")
        t.execute(fail=fail, code=code, args=args)
        if code == 0:
            t.check_file_output(outfile, f"{output_dir}/reference{output_id}.bin")
            t.check_stdout(msg)

    def test_simple0_input0(self):
        self.run_classify(input_dir="inputs/simple0/bin", input="input0.bin", output_id=0)

    def test_simple0_input0_print_out(self):
        self.run_classify(input_dir="inputs/simple0/bin", input="input0.bin", output_id=0, msg="2")

    def test_fail_malloc(self):
        # unfortunately this test actually does not fail inside classify, but inside read_matrix
        self.run_classify(input_dir="inputs/simple0/bin", input="input0.bin", output_id=0, fail="malloc", code=88)

    def test_wrong_number_of_args(self):
        t = self.make_test()
        t.call("classify")
        t.execute(code=89, args=[""])


# The following are some simple sanity checks:
import subprocess, pathlib, os
script_dir = pathlib.Path(os.path.dirname(__file__)).resolve()

def compare_files(test, actual, expected):
    assert os.path.isfile(expected), f"Reference file {expected} does not exist!"
    test.assertTrue(os.path.isfile(actual), f"It seems like the program never created the output file {actual}")
    # open and compare the files
    with open(actual, 'rb') as a:
        actual_bin = a.read()
    with open(expected, 'rb') as e:
        expected_bin = e.read()
    test.assertEqual(actual_bin, expected_bin, f"Bytes of {actual} and {expected} did not match!")


class TestMain(TestCase):
    """ This sanity check executes src/main.s using venus and verifies the stdout and the file that is generated.
    """

    def run_venus(self, args):
        venus_jar = pathlib.Path('tools') / 'venus.jar'
        cmd = ['java', '-jar', venus_jar, '--immutableText', '--maxsteps', '-1', '--callingConvention'] + args
        # run venus from the project root directory
        r = subprocess.run(cmd, stdout=subprocess.PIPE, cwd=script_dir / '..')
        return r.returncode, r.stdout.decode('utf-8').strip()

    def run_main(self, inputs, output_id, lbl):
        args = [f"{inputs}/m0.bin", f"{inputs}/m1.bin", f"{inputs}/inputs/input0.bin",
                f"outputs/test_basic_main/student{output_id}.bin"]
        reference = f"outputs/test_basic_main/reference{output_id}.bin"

        code, stdout = self.run_venus(["src/main.s"] + args)
        self.assertEqual(code, 0, stdout)
        self.assertEqual(stdout, lbl)

        compare_files(self, actual=script_dir / '..' / args[-1], expected=script_dir / '..' / reference)

    def test0(self):
        self.run_main("inputs/simple0/bin", "0", "2")

    def test1(self):
        self.run_main("inputs/simple1/bin", "1", "1")

    