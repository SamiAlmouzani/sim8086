; test/5/listing_0046_add_sub_cmp
bits 16

mov bx, 61443 ; bx:0x0->0xf003
mov cx, 3841 ; cx:0x0->0xf01
sub bx, cx ; bx:0xf003->0xe102 flags:->S
mov sp, 998 ; sp:0x0->0x3e6
mov bp, 999 ; bp:0x0->0x3e7
cmp bp, sp ; flags:S->
add bp, 1027 ; bp:0x3e7->0x7ea flags:->S
