; test/4/listing_0044_register_movs
bits 16

mov ax, 1 ; ax:0x0->0x1
mov bx, 2 ; bx:0x0->0x2
mov cx, 3 ; cx:0x0->0x3
mov dx, 4 ; dx:0x0->0x4
mov sp, ax ; sp:0x0->0x1
mov bp, bx ; bp:0x0->0x2
mov si, cx ; si:0x0->0x3
mov di, dx ; di:0x0->0x4
mov dx, sp ; dx:0x4->0x1
mov cx, bp ; cx:0x3->0x2
mov bx, si ; bx:0x2->0x3
mov ax, di ; ax:0x1->0x4

Final Registers:
	ax: 0x4 (4)
	bx: 0x3 (3)
	cx: 0x2 (2)
	dx: 0x1 (1)
	sp: 0x1 (1)
	bp: 0x2 (2)
	si: 0x3 (3)
	di: 0x4 (4)
