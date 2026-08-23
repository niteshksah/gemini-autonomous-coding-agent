`timescale 1ns / 1ps

module alu_tb;

    // Inputs
    reg [3:0] a;
    reg [3:0] b;
    reg [1:0] opcode;

    // Outputs
    wire [3:0] result;
    wire       carry_out;
    wire       zero;

    // Instantiate the Unit Under Test (UUT)
    alu uut (
        .a(a),
        .b(b),
        .opcode(opcode),
        .result(result),
        .carry_out(carry_out),
        .zero(zero)
    );

    // Task to display and check results
    task check_alu(
        input [3:0] expected_res,
        input expected_carry,
        input expected_zero,
        input [8*10:1] op_name
    );
        begin
            #10;
            $display("Time=%0t | Op=%s | A=%b (%0d) | B=%b (%0d) | Result=%b (%0d) | Carry=%b | Zero=%b",
                     $time, op_name, a, a, b, b, result, result, carry_out, zero);
            if (result !== expected_res || carry_out !== expected_carry || zero !== expected_zero) begin
                $display("ERROR: Expected Result=%b, Carry=%b, Zero=%b", expected_res, expected_carry, expected_zero);
            end else begin
                $display("PASS");
            end
        end
    endtask

    initial begin
        $display("--------------------------------------------------");
        $display("Starting 4-bit ALU Testbench");
        $display("--------------------------------------------------");

        // Test 1: ADD operation without carry
        a = 4'b0011; b = 4'b0100; opcode = 2'b00; // 3 + 4 = 7
        check_alu(4'b0111, 1'b0, 1'b0, "ADD");

        // Test 2: ADD operation with carry
        a = 4'b1010; b = 4'b0110; opcode = 2'b00; // 10 + 6 = 16 (0 with carry 1)
        check_alu(4'b0000, 1'b1, 1'b1, "ADD Carry");

        // Test 3: SUB operation
        a = 4'b1001; b = 4'b0011; opcode = 2'b01; // 9 - 3 = 6
        check_alu(4'b0110, 1'b0, 1'b0, "SUB");

        // Test 4: SUB operation resulting in 0
        a = 4'b0101; b = 4'b0101; opcode = 2'b01; // 5 - 5 = 0
        check_alu(4'b0000, 1'b0, 1'b1, "SUB Zero");

        // Test 5: AND operation
        a = 4'b1100; b = 4'b1010; opcode = 2'b10; // 1100 & 1010 = 1000
        check_alu(4'b1000, 1'b0, 1'b0, "AND");

        // Test 6: OR operation
        a = 4'b1100; b = 4'b0011; opcode = 2'b11; // 1100 | 0011 = 1111
        check_alu(4'b1111, 1'b0, 1'b0, "OR");

        $display("--------------------------------------------------");
        $display("ALU Testbench Completed Successfully");
        $display("--------------------------------------------------");
        $finish;
    end

endmodule
