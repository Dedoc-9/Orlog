Produced by `research/rust-core/gen_worked.py` (sha256 163e54f4b30f1d3ad6cef3189f5408a3af3886347e504a79df91633314dfb738) from the reference at `2e9805a`:
`src/orlog/interp.py` sha256 f843291861798c85c90716430a00b24663e4d7521f6cecdf268cb197c7e94d27, `src/orlog/numeric_ref.py` sha256 eacac3dd7c4dfda903f1927994ea8b3a95ba866b3485fb1c6b91428cb5f6bb64. Data, as the vectors are.

**A.1, the empty law.**

The law bytes:
```
orlog-law 0
(decimals fixed)
```
TEXTSEAL `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`; the law seal `91e3deb3c796c4742eb2a12ca5e20e157fdfc172d2bf25237803d58c1f28e0f5`; the seal words `nalog-tupug-sivik-siduh`.

The reference's receipt (the core's differs in its backend line only):
```
orlog-receipt 0
backend reference
law-seal 91e3deb3c796c4742eb2a12ca5e20e157fdfc172d2bf25237803d58c1f28e0f5
text-seal e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
status COMPLETED
output-bytes 0
output-sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
events 0
trace-head 7715e904c45590b3390600b39035119c4e43ef4e7654a2176acd27ff817fa65a
ops 0
claims 0
end
```
Its trace (0 events): empty.

**A.2, a let and a say.**

The law bytes:
```
orlog-law 0
(decimals fixed)
(clause 1 0 (let 0 "x" (lit int 2)))
(clause 2 0 (say (+ int (var 0) (lit int 3))))
```
TEXTSEAL `88e22c52d51ec526acaa7f81a756a3cb7f43b091bf40a62bd741d2f1ca0e1c37`; the law seal `6304879cfa306423bde86f555dab2a3d9b58487e61372e623ee1ae4f95f4d61e`; the seal words `kasah-mivis-zomub-kibog`.

The reference's receipt (the core's differs in its backend line only):
```
orlog-receipt 0
backend reference
law-seal 6304879cfa306423bde86f555dab2a3d9b58487e61372e623ee1ae4f95f4d61e
text-seal 88e22c52d51ec526acaa7f81a756a3cb7f43b091bf40a62bd741d2f1ca0e1c37
status COMPLETED
output-bytes 2
output-sha256 f0b5c2c2211c8d67ed15e75e656c7862d086e9245420892a7de62cd9ec582a06
events 2
trace-head b419cc706a28145fc6d15204c541808c8b1e6396f2cf1f26f033f63b091c0e2c
ops 3
claims 0
end
```
Its trace (2 events):
```
1 A 1 00000000490000000000000002 6f4033604a8ac71abf356b8f3e84483c7666a43ea90805cc1ff93b553a8c7cc6
2 S 2 350a b419cc706a28145fc6d15204c541808c8b1e6396f2cf1f26f033f63b091c0e2c
```

**A.3, a refusal.**

The law bytes:
```
orlog-law 0
(decimals fixed)
(clause 1 0 (say (lit int 1)))
(clause 2 0 (say (/ int (lit int 1) (lit int 0))))
```
TEXTSEAL `70751059da2fba395c50aa0eab1f5ee5b934c623c514303c0e7207bb2a888f84`; the law seal `e6d8b12f7b694133eba2d2d87b241fe51dbbe1dcd4721028b35fd0bd5c8c57df`; the seal words `virim-rahoz-loton-hahug`.

The reference's receipt (the core's differs in its backend line only):
```
orlog-receipt 0
backend reference
law-seal e6d8b12f7b694133eba2d2d87b241fe51dbbe1dcd4721028b35fd0bd5c8c57df
text-seal 70751059da2fba395c50aa0eab1f5ee5b934c623c514303c0e7207bb2a888f84
status REFUSED DIVISION-BY-ZERO 2
output-bytes 2
output-sha256 4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865
events 2
trace-head 6ed0717fc44eb9cffab2f5d40365af51cda3179d3785fc82c74bda2a3f73eda6
ops 3
claims 0
end
```
Its trace (2 events):
```
1 S 1 310a 504d87ff9640c0c1c1f656076b94c35da0c630ab03b682908621ee08515cbd9d
2 R 2 4449564953494f4e2d42592d5a45524f 6ed0717fc44eb9cffab2f5d40365af51cda3179d3785fc82c74bda2a3f73eda6
```

**A.4, a cost counter read inside and after its clause (REREAD-1 C8).**

The law bytes:
```
orlog-law 0
(decimals fixed)
(clause 1 0 (let 0 "n" (lit int 0)))
(clause 2 0 (while 5 (< bool (var 0) (lit int 2))))
(clause 3 2 (change + 0 - (lit int 1)))
(clause 4 2 (claim 0 (lit bool 1) (certificate 2) (given )))
(clause 5 0 (claim 1 (lit bool 1) (certificate 2) (given )))
```
TEXTSEAL `5df6a00e450ce11b4163146bdce7e3b7a4d51c44813d67f7cf6841433821ad8b`; the law seal `e5f37d43618027876a969be4fbb3f79371325cba5de7ddb313930cf43cd70cbf`; the seal words `vilug-lujag-kakab-fival`.

The reference's receipt (the core's differs in its backend line only):
```
orlog-receipt 0
backend reference
law-seal e5f37d43618027876a969be4fbb3f79371325cba5de7ddb313930cf43cd70cbf
text-seal 5df6a00e450ce11b4163146bdce7e3b7a4d51c44813d67f7cf6841433821ad8b
status COMPLETED
output-bytes 0
output-sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
events 6
trace-head 72b60be361eea0da803df2f6764fba98de41aff2c6cbac7957187a3c2d5bef2b
ops 14
claims 2
claim 0 4 2 2 0 2 0
claim 1 5 1 1 0 2 12
end
```
Its trace (6 events):
```
1 A 1 00000000490000000000000000 5df1ba66697fdc66a7150bbe2db5ecebfe080a44278454e73042de18467953c5
2 A 3 00000000490000000000000001 45b29220b0d679fd4b4275fecfedf443400b9bd325acd79d049862571ebbf38e
3 C 4 0000000001 3325562db199e3577e59767fbc4eabf87264cc616b70d18c9a61e14597ebd1e4
4 A 3 00000000490000000000000002 7f0cf79be99b15ffcc0fbd5c67857064dbfd370548ffd233e9b9dda5b51a56ca
5 C 4 0000000001 ed8a874bb7530b3f81e2a10d75ef5780394b699f105bb84b897f801bb9019655
6 C 5 0000000101 72b60be361eea0da803df2f6764fba98de41aff2c6cbac7957187a3c2d5bef2b
```

