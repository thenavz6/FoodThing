import itertools

is_authenticated = False
userid = -1
email = ""
username = ""
imageurl = ""
current_token = ""

key = "*(HT#KDMSFGKDSF#()@Jdngfuidsnfej #@UJ3rufnbUFBNES(D hf8932wur832hnoRNFOSDIF HJ*(HJ#R*(#2htru4rebngfej*HTR(*T@JIMSDGGmwds;LwuifnewuIJ N*(#@HJ*(HTFUSENFGJNS Dwh89hf90HUB#@UBTehsfh ewhf*(H#HBRU#BFDJSH *FH#$u bnH@(!BU@B TIWE SFKSDFLSDGFP SLDnv iskdvpLLf[p lsdfplsd fjE*(Fh*()#JHR *(HFUNDSFJ NDSF*HR*)#@U R90hj3UTGB*@!UHJ#TYG*$YHRTG&*^T^T&@!&$*(@!^%YRT(*&SDH BFIUESBWF EHW*(D H #@*UR#*@HTB(UWSHNDR FIONDSJFNVDJIXBNVICJX AWI)JFwsuiabfiu fjhewu9hf9e8wyh r3789YHR(FUWEBSF*YU HEFd879h3Wy8 GBF&U( EH$WY*trghB# (*FByudshf89 h439GH(UFGDSJGb( ht 83hTUIFGNERDSO GIJ)(SJNEDMP@!MR @KJGNDFjkgvHSA)FIDS (*HJGF*(&@#$H )RHN#@JGNDSOIG J0ewsur3 289h tu4 3tn(#OR*Y@ #&*^T#H@^ @_DS)F dsjkf sdionf uidsbf9sd hfeLWNT OD)(FJ SDIUFN(*&@# UY$%*(#htnbUINSD)FIJSD*)FYUH$@(&H %B R)@#UJRFSDfn ds9ghj08 u3 *RH@!(R H)ERGJSGjksdng iofdngoisdnfuiewbhr8th3 *U*TH#@ (HJ*)GHDUhr7h3489h gf8943hgSLDGN OIJTG #@(*  HGT@ #(j sdfi dsng0frhjg8034 hn2 0hJ)G9 wfuhwe0 8U H@#(*HBNF(DSHJnf809swedjugf 89342ht9HBASF(*HD*DFHJ#U(B RTF#@W(*fhjsd89fnvijdsn IJ(*J@#*(NRFUewdsnfvudch v89hr87 4hb(#@HRFIDSNfgv9uhre89hg348bgurnidfgj 89H*(#HR *@HJR#*@TU#(*EHGsu9fnv eufvnsduvn( *H#@(* RH329nrfjiSDNf (UJNV(*N$#W(&RBN#@(NFDjsfn s9udfhsd98h #(*HR(N#@(NFSDJknf ds9h9*H# *(@RHJisndf sdiongfdswiogjnerw8 gh r98HT )*#$JH RNSdfm ds0gbjg8 953hj20inF(SDUfn *(HJTF@$#(*HN(N(#N@(UNFD*S(FH&HG&FHEWHF(fd sadh239 h(*T#H@# (*Hdsufnugdjkgn20ht g8954ht9GBNUI GFB(H SD*FHu 23b"


def xor(s):
    global key
    key = key * (len(s) / len(key) + 1)
    return ''.join(chr(ord(x) ^ ord(y)) for (x,y) in itertools.izip(s, key))
