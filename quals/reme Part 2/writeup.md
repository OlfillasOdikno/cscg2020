---
html:
  embed_local_images: true
  embed_svg: true
  offline: true
export_on_save:
  html: true
print_background: true
---
@import "../style.less"

# reme Part 2 - localo


**Category:** Reverse Engineering       
**Difficulty:** Medium        
**Author:** 0x4d5a
**Dependencies:** reme Part 1

## Description
>.NET Reversing can't be that hard, right? But I've got some twists waiting for you 😈
>
>Execute with .NET Core Runtime 2.2 with windows, e.g. dotnet ReMe.dll
## Summery
This writeup depends on my writeup for `reme Part 1`.
If we use the password from the last Part as the first argument we get `Nope.` again, but this time with a dot:
```shell
> dotnet ReMe.dll CanIHazFlag? AAAA
There you go. Thats the first of the two flags! CSCG{CanIHazFlag?}
Nope.
``` 

## Solution
Remember the many Debugger checks? None of them worked last time, but after the first Part is another one. This one does detect that we are debugging the program. But we can set a breakpoint on the check and modify the content of `flag6`.
```dotnet
IntPtr moduleHandle = Program.GetModuleHandle("kernel32.dll");
bool flag6 = moduleHandle != IntPtr.Zero;
if (flag6)
{
	IntPtr procAddress = Program.GetProcAddress(moduleHandle, "CheckRemoteDebuggerPresent");
	bool flag7 = Marshal.ReadByte(procAddress) == 233;
	if (flag7)
	{
		Console.WriteLine("Nope!");
		Environment.Exit(-1);
	}
}
```
Before the modification:
@import "before.png"
After the modification:
@import "after.png"
And we pass the check! Back to the `Main` function:
```dotnet
private static void Main(string[] args)
{
	Program.InitialCheck(args);
	byte[] ilasByteArray = typeof(Program).GetMethod("InitialCheck", BindingFlags.Static | BindingFlags.NonPublic).GetMethodBody().GetILAsByteArray();
	byte[] array = File.ReadAllBytes(Assembly.GetExecutingAssembly().Location);
	int[] array2 = array.Locate(Encoding.ASCII.GetBytes("THIS_IS_CSCG_NOT_A_MALWARE!"));
	MemoryStream memoryStream = new MemoryStream(array);
	memoryStream.Seek((long)(array2[0] + Encoding.ASCII.GetBytes("THIS_IS_CSCG_NOT_A_MALWARE!").Length), SeekOrigin.Begin);
	byte[] array3 = new byte[memoryStream.Length - memoryStream.Position];
	memoryStream.Read(array3, 0, array3.Length);
	byte[] rawAssembly = Program.AES_Decrypt(array3, ilasByteArray);
	object obj = Assembly.Load(rawAssembly).GetTypes()[0].GetMethod("Check", BindingFlags.Static | BindingFlags.Public).Invoke(null, new object[]
	{
		args
	});
}
```
After the `Program.InitialCheck(args);` call some stuff is happening, but the only interesting part are th last lines.
The program loads assembly from it memory and invokes a method `Check`. I have done some `Java` stuff a few years ago and since `C#` is basically `Java by Microsoft` they both use some form of `bytecode`. Buf for our needs it is enough to set a breakpoint inside the `Invoke` function and continue until we hit it. 
@import "invoke.png"
Step inside and step over until we hit `object result = RuntimeMethodHandle.InvokeMethod(obj, array, this.Signature, false, wrapExceptions);`

Now step inside again and we are inside the `Check` function:
```dotnet
public static void Check(string[] args)
{
	bool flag = args.Length <= 1;
	if (flag)
	{
		Console.WriteLine("Nope.");
	}
	else
	{
		string[] array = args[1].Split(new string[]
		{
			"_"
		}, StringSplitOptions.RemoveEmptyEntries);
		bool flag2 = array.Length != 8;
		if (flag2)
		{
			Console.WriteLine("Nope.");
		}
		else
		{
			bool flag3 = "CSCG{" + array[0] == "CSCG{n0w" && array[1] == "u" && array[2] == "know" && array[3] == "st4t1c" && array[4] == "and" && Inner.CalculateMD5Hash(array[5]).ToLower() == "b72f3bd391ba731a35708bfd8cd8a68f" && array[6] == "dotNet" && array[7] + "}" == "R3333}";
			if (flag3)
			{
				Console.WriteLine("Good job :)");
			}
		}
	}
}
```
Here we see the check for the second flag, our input is split at `_` and checked:
```
bool flag3 = "CSCG{" + array[0] == "CSCG{n0w" && array[1] == "u" && array[2] == "know" && array[3] == "st4t1c" && array[4] == "and" && Inner.CalculateMD5Hash(array[5]).ToLower() == "b72f3bd391ba731a35708bfd8cd8a68f" && array[6] == "dotNet" && array[7] + "}" == "R3333}";
```
We can simply join the individual checks with `_` to get most the flag:
`CSCG{n0w_u_know_st4t1c_and_`...`_dotNet_R3333}`
We could guess the missing part:
The opposite of `static` is `dynamic`, therefore the part is probably `dyn4m1c`, but since it is just a MD5 hash and the word is probably quite short we can throw it into `CrackStation` first.
@import "crackstation.png"
No 1337 for us this time :(
**IT EVEN HAS** `dyn4m1c` **IN IT'S DATABASE:**
@import "crackstation2.png"
## Mitigation
- check the hash of the entire and long password and use the plaintext as a decryption key for the program or something similar

## Flag
CSCG{n0w_u_know_st4t1c_and_dynamic_dotNet_R3333}