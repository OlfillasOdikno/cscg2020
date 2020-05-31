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

# reme Part 1 - localo


**Category:** Reverse Engineering       
**Difficulty:** Easy        
**Author:** 0x4d5a

## Description
>.NET Reversing can't be that hard, right? But I've got some twists waiting for you 😈
>
>Execute with .NET Core Runtime 2.2 with windows, e.g. dotnet ReMe.dll
## Summery
The author provided some files and a `.NET` dll. 
When we run `reme` without any arguments, it shows the usage:
```
> dotnet ReMe.dll
Usage: ReMe.exe [password] [flag]
```
If we run `reme` with arguments it says `Nope`: 
```
> dotnet ReMe.dll AAA BBB
Nope
```

## Solution
Like for Java, the Decompilers for .NET are quite good therefore I fired up `dnSpy` and opened the dll. 
```dotnet
using System;
using System.Diagnostics;
using System.IO;
using System.Reflection;
using System.Runtime.InteropServices;
using System.Security.Cryptography;
using System.Text;

namespace ReMe
{
	// Token: 0x02000003 RID: 3
	internal class Program
	{
		// Token: 0x06000005 RID: 5 RVA: 0x00002075 File Offset: 0x00000275
		static Program()
		{
			Program.Initialize();
		}

		// Token: 0x06000006 RID: 6 RVA: 0x00002178 File Offset: 0x00000378
		private static void Main(string[] args)
		{
			Program.InitialCheck(args);
    [...]
```
In `Main` the function `Program.InitialCheck(args);` is called with the program arguments. In this function is the first Flag:

```dotnet
// ReMe.Program
// Token: 0x0600000C RID: 12 RVA: 0x000022BC File Offset: 0x000004BC
private static void InitialCheck(string[] args)
{
	Program.Initialize();
	bool isAttached = Debugger.IsAttached;
	if (isAttached)
	{
		Console.WriteLine("Nope");
		Environment.Exit(-1);
	}
	bool flag = true;
	Program.CheckRemoteDebuggerPresent(Process.GetCurrentProcess().Handle, ref flag);
	bool flag2 = flag;
	if (flag2)
	{
		Console.WriteLine("Nope");
		Environment.Exit(-1);
	}
	bool flag3 = Program.IsDebuggerPresent();
	if (flag3)
	{
		Console.WriteLine("Nope");
		Environment.Exit(-1);
	}
	bool flag4 = args.Length == 0;
	if (flag4)
	{
		Console.WriteLine("Usage: ReMe.exe [password] [flag]");
		Environment.Exit(-1);
	}
	bool flag5 = args[0] != StringEncryption.Decrypt("D/T9XRgUcKDjgXEldEzeEsVjIcqUTl7047pPaw7DZ9I=");
	if (flag5)
	{
		Console.WriteLine("Nope");
		Environment.Exit(-1);
	}
	else
	{
		Console.WriteLine("There you go. Thats the first of the two flags! CSCG{{{0}}}", args[0]);
	}
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
}
```
But the flag is encrypted, we could Reverse-Engineer the `StringEncryption.Decrypt` function or just set a breakpoint at at the `return` inside the `Decrypt` function and watch the `locals`, because the flag is decrypted in memory after that call. Because of some bug we have to also set a breakpoint in `.cctor()` otherwise we would not be able to see the locals.
@import "cctor.png"
Now just press continue until we hit the breakpoint.
@import "flag.png" 
And the flag is in the locals after `cipherText`, just wrap it in the flag format `CSCG{<cipherText>}`.

## Mitigation
- check the hash of the password and use the plaintext as a decryption key for the program or something similar

## Flag
CSCG{CanIHazFlag?}