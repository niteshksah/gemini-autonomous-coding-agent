// 4-bit ALU Module
// Operations:
//   2'b00: ADD (a + b)
//   2'b01: SUB (a - b)
//   2'b10: AND (a & b)
//   2'b11: OR  (a | b)

module alu (
    input  wire [3:0] a,
    input  wire [3:0] b,
    input  wire [1:0] opcode,
    output reg  [3:0] result,
    output reg        carry_out,
    output wire       zero
);

    assign zero = (result == 4'b0000);

    always @(*) begin
        carry_out = 1'b0;
        case (opcode)
            2'b00: {carry_out, result} = a + b;
            2'b01: {carry_out, result} = a - b;
            2'b10: result = a & b;
            2'b11: result = a | b;
            default: begin
                result = 4'b0000;
                carry_out = 1'b0;
            end
        endcase
    end

endmodule
