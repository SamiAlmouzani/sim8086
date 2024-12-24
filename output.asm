; test/5/listing_0046_add_sub_cmp
bits 16

mov bx, 61443 ; bx:0x0->0xf003
mov cx, 3841 ; cx:0x0->0xf01
bin_result: 1110000100000010
sub bx, cx ; bx:0xf003->0xe102 flags:->S
mov sp, 998 ; sp:0x0->0x3e6
mov bp, 999 ; bp:0x0->0x3e7
bin_result: 0000000000000001
cmp bp, sp ; flags:S->
bin_result: 0000011111101010
add bp, 1027 ; bp:0x3e7->0x7ea flags:->
bin_result: 0000000000000000
sub bp, 2026 ; bp:0x7ea->0x0 flags:->Z

Final Registers:
	ax: 0x0 (0)
	bx: 0xe102 (57602)
	cx: 0xf01 (3841)
	dx: 0x0 (0)
	sp: 0x3e6 (998)
	bp: 0x0 (0)
	si: 0x0 (0)
	di: 0x0 (0)
  flags:1
