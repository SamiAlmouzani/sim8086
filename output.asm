; test/3/listing_0041_add_sub_cmp_jnz
bits 16

add bx, [bx + si]
add bx, [bp + 0]
add si, 2
add bp, 2
add cx, 8
add bx, [bp + 0]
add cx, [bx + 2]
add bh, [bp + si + 4]
add di, [bp + di + 6]
add [bx + si], bx
add [bp + 0], bx
add [bp + 0], bx
add [bx + 2], cx
add [bp + si + 4], bh
add [bp + di + 6], di
add byte [bx], 34
add word [bp + si + 1000], 29
add ax, [bp + 0]
add al, [bx + si]
add ax, bx
add al, ah
add ax, 1000
add al, 226
add al, 9
sub bx, [bx + si]
sub bx, [bp + 0]
sub si, 2
sub bp, 2
sub cx, 8
sub bx, [bp + 0]
sub cx, [bx + 2]
sub bh, [bp + si + 4]
sub di, [bp + di + 6]
sub [bx + si], bx
sub [bp + 0], bx
sub [bp + 0], bx
sub [bx + 2], cx
sub [bp + si + 4], bh
sub [bp + di + 6], di
sub byte [bx], 34
sub word [bx + di], 29
sub ax, [bp + 0]
sub al, [bx + si]
sub ax, bx
sub al, ah
sub ax, 1000
sub al, 226
sub al, 9
cmp bx, [bx + si]
cmp bx, [bp + 0]
cmp si, 2
cmp bp, 2
cmp cx, 8
cmp bx, [bp + 0]
cmp cx, [bx + 2]
cmp bh, [bp + si + 4]
cmp di, [bp + di + 6]
cmp [bx + si], bx
cmp [bp + 0], bx
cmp [bp + 0], bx
cmp [bx + 2], cx
cmp [bp + si + 4], bh
cmp [bp + di + 6], di
cmp byte [bx], 34
cmp word [4834], 29
cmp ax, [bp + 0]
cmp al, [bx + si]
cmp ax, bx
cmp al, ah
cmp ax, 1000
cmp al, 226
cmp al, 9
jnz ; 2
jnz ; 252
jnz ; 250
jnz ; 252
je ; 254
jl ; 252
jle ; 250
jb ; 248
jbe ; 246
jp ; 244
jo ; 242
js ; 240
jnz ; 238
jnl ; 236
jg ; 234
jnb ; 232
ja ; 230
jnp ; 228
jno ; 226
jns ; 224
loop ; 222
loopz ; 220
loopnz ; 218
jcxz ; 216
