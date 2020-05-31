Dim VBEFile, fso

If WScript.Arguments.Count = 0 Then
	WScript.Echo  "Kein Parameter angegeben"
Else
	On Error Resume Next
	
	For each Argument in WScript.Arguments
		VBEFile = VBEFile & Argument & " "
	Next

	Set fso = WScript.CreateObject("Scripting.FileSystemObject")
	If fso.FileExists(VBEFile) Then
		Dim vbe,Conten
		Set vbe = fso.OpenTextFile(VBEFile, 1)
		Conten=vbe.readAll
		CHKerr()
		vbe.close
		Set vbe=Nothing

		Const TagInit = "#@~^" '#@~^awQAAA==
		Const TagFin = "==^#~@" '& chr(0)
		Dim DebCode, FCode
		Do
			FCode=0
			DebCode = Instr(Conten,TagInit)
			If DebCode>0 Then
				If (Instr(DebCode,Conten,"==")-DebCode)=10 Then 'If "==" follows the tag
					FCode=Instr(DebCode,Conten,TagFin)
					If FCode>0 Then
						Conten=Left(Conten,DebCode-1) & _
						Decode(Mid(Conten,DebCode+12,FCode-DebCode-12-6)) & _
						Mid(Conten,FCode+6)
					End If
				End If
			End If
		Loop Until FCode=0
		
		des = mid(VBEFile,1,InstrRev(VBEFile,".",-1)) & "vbs"

		Set vbs = fso.OpenTextFile(des, 2, True)
   			vbs.Write Conten
				vbs.close

	End If
	Set fso=Nothing

end if

Function Decode(Csrc)
	Dim se,i,c,j,index,CsrcTemp
	Dim tDecode(127)
	Const Combinaison = "1231232332321323132311233213233211323231311231321323112331123132"

	Set se=WSCript.CreateObject("Scripting.Encoder")
	For i=9 to 127
		tDecode(i)="JLA"
	Next
	For i=9 to 127
		CsrcTemp=Mid(se.EncodeScriptFile(".vbs",string(3,i),0,""),13,3)
		For j=1 to 3
			c=Asc(Mid(CsrcTemp,j,1))
			tDecode(c)=Left(tDecode(c),j-1) & chr(i) & Mid(tDecode(c),j+1)
		Next
	Next
	tDecode(42)=Left(tDecode(42),1) & ")" & Right(tDecode(42),1)
	Set se=Nothing

	Csrc=Replace(Replace(Csrc,"@&",chr(10)),"@#",chr(13))
	Csrc=Replace(Replace(Csrc,"@*",">"),"@!","<")
	Csrc=Replace(Csrc,"@$","@")
	index=-1
	For i=1 to Len(Csrc)
		c=asc(Mid(Csrc,i,1))
		If c<128 Then index=index+1
		If (c=9) or ((c>31) and (c<128)) Then
			If (c<>60) and (c<>62) and (c<>64) Then
				Csrc=Left(Csrc,i-1) & Mid(tDecode(c),Mid(Combinaison,(index mod 64)+1,1),1) & Mid(Csrc,i+1)
			End If
		End If
	Next
	Decode=Csrc
End Function


Private Function CHKerr()

	if err.number <> 0 then
		if err.number = 62 then
			WScript.echo "Fehlercode: " & err.number & vbcrlf & err.description & vbcrlf & "Leere Dateien können nicht umgewandelt werden"
			err.clear
		else
			WScript.echo "Fehlercode: " & err.number & vbcrlf & err.description
			err.clear
		end if
	end if

End Function