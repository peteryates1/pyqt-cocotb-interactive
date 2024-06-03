module adder #(
    DATA_WIDTH = 4
) (
    input c,
    input [DATA_WIDTH-1:0] a, b,
    output [DATA_WIDTH:0] q
);

assign q = a + b + c;

endmodule
