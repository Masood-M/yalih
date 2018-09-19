rule myrule
{
        meta:
                impact = 6
        strings:
                $body = "rapid" nocase
        condition:
                $body
}



rule SuspicousBodyOnload
{
        meta:
                impact = 6
        strings:
                $body = /<body [^>]*onload\s*=\s*['"]*[a-z0-9]+\(['"][a-f0-9]{300}/ nocase
        condition:
                $body
}



rule PossibleShellcodePattern
{
	strings:
#		$a1 = /=\s*?unescape\(\s*?\n?\s*["'](%u[a-fA-F0-9]{4}|%[a-fA-F0-9]{2}){2,}['"]\s*?[\+\)]/ nocase

		$b1 = "unescape" fullword nocase
		$b2 = "%u0A0A" nocase
		$b3 = "%u9090"
		$shellcode = /(%u[A-Fa-f0-9]{4}){8}/

		$c1 = /document\.write\(unescape\(\s*?\n?\s*["'](%u[a-fA-F0-9]{4}|%[a-fA-F0-9]{2}){2,}['"]/ nocase
		
	condition:
		$b1 and ($b2 or $b3) or ($b1 and $shellcode) or $c1
} 

rule PossibleExecutable
{
	strings:
		$a1 = /\.exe['"\s]/ nocase
#		$a2 = /<object.*?classid\s*?=\s*?/ nocase
	
	condition:
		$a1
}


rule PossibleIFrame
{
	meta:
		description = "Possible malicious link redirection"
	strings:
		$a1 = /ini\.php['"]\s*?width=['"]0['"]\s*?height=['"]0["']\s*?frameborder=['"]0['"]><\/iframe>/
	condition:
		$a1
}





	
