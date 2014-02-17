// Credits given to the PhpIDS project at https://dev.itratos.de/projects/php-ids/repository/raw/trunk/lib/IDS/default_filter.xml


//rule selfcontainedxss
//{
//	meta:
//		impact = 5
//		hide = true
//		desc = "Detects self contained xss via with(), common loops and regex to string conversion"
//	strings:
//		$a = /(?:with\s*\(\s*.+\s*\)\s*\w+\s*\()|(?:(?:do|while|for)\s*\([^)]*\)\s*\{)|(?:\/[\w\s]*\[\W*\w)/ nocase
//	condition:
//		$a
//}


rule BasicObfuscatedJavaSriptInjection
{
	meta:
		impact = 0
		desc = "Detects basic obfuscated JavaScript script injections"
	strings:
		$s10 = /(?:\/[\w\s]+\/\.)|(?:=\s*\/\w+\/\s*\.)|(?:\[\s*\/\w+)|(?:(?:this|window|top|parent|frames|self|content)\[\s*\w)/ nocase
	condition:
		$s10
}

rule specific_directory_Path_traversal
{
	meta:
		impact = 5
		hide = true
		desc = "Detects specific directory and path traversal"
	strings:
		$e = /(?:%c0%ae\/)|(?:(?:\/|\\)+(home|conf|usr|etc|proc|opt|s?bin|local|dev|tmp|kern|[br]oot|sys|system|windows|winnt|program|%[a-z_-]{3,}%)(?:\/|\\))|(?:(?:\/|\\)+inetpub|localstart\.asp|boot\.ini)/ nocase
	condition:
		$e
}


/*rule possible_includes_base64_packed_functions 
{
	meta:
		impact = 5
		hide = true
		desc = "Detects possible includes and packed functions"
	strings:
		$f = /(?:\w+script:|@import[^\w]|;base64|base64,)|(?:\w+\s*\([\w\s]+,[\w\s]+,[\w\s]+,[\w\s]+,[\w\s]+,[\w\s]+\))/ nocase
		//$ff = /(?:[A-Za-z0-9]{4}){2,}(?:[A-Za-z0-9]{2}[AEIMQUYcgkosw048]=|[A-Za-z0-9][AQgw]==)/ nocase
		$fff = /(?:[A-Za-z0-9]{4})*(?:[A-Za-z0-9]{2}==|[A-Za-z0-9]{3}=|[A-Za-z0-9]{4})/
	condition:
		$f and $fff
}
*/
/*
rule jsDOM_properties_methods
{
	meta:
		impact = 6
		hide = true
		desc = "Detects JavaScript DOM/miscellaneous properties and methods"
	strings:
		$g = /([^*:\s\w,.\/?+-]\s*)?(?<![a-z]\s)(?<![a-z\/_@>-])(\s*return\s*)?(?:create(?:element|attribute|textnode)|[a-z]+Events?|getelement\w+|appendchild|createrange|createcontextualfragment|removenode|parentnode|decodeuricomponent|\wettimeout|useragent)(?(1)[^\w%"]|(?:\s*[^@\s\w%",.+-]))/ nocase
	condition:
		$g
}
*/



/*rule URL_injection_URI_schemes
{
	meta:
		impact = 5
		hide = true
		desc = "Detects data: URL injections and common URI schemes"
	strings:
		$i = /(?:data:(?:.)*,)|(?:\w+\s*=\W*(?!https?)\w+:)|(jar:\w+:)/ nocase
	condition:
		$i
}*/


rule null_bytes_HTTP_splitting
{
	meta:
		impact = 5
		hide = true
		desc = "Detects nullbytes and HTTP response splitting"
	strings:
		$j = /(?:\\x[01FE]\w)|(?:%[01FE]\w)|(?:&#[01FE]\w)|(?:\\[01FE][0-9a-f])|(?:&#x[01FE]\w)/ nocase
	condition:
		$j
}



rule url_injection_RFE_Attempt
{
	meta:
		impact = 5
		hide = true
		desc = "Detects url injections and RFE attempts"
	strings:
		$k = /(?:\w+]?(?<!href)(?<!src)(?<!longdesc)(?<!returnurl)=(?:https?|ftp):)|(?:\{\s*\$\s*\{)/ nocase
	condition:
		$k
}


rule perl_shellcode_injection_LDAP_Vector
{
	meta:
		impact = 5
		hide = true
		desc = "Detects perl echo shellcode injection and LDAP vectors"
	strings:
		$l = /(?:\.pl\?\w+=\w?\|\w+;)|(?:\|\(\w+=\*)|(?:\*\s*\)+\s*;)/ nocase
	condition:
		$l
}


rule Attribute_breaking_or_obfuscated
{
	meta:
		impact = 4
		hide = true
		desc = "finds attribute breaking injections including obfuscated attributes"
	strings:
		$m = /(?:[\s\/"]+[-\w\/\\\*]+\s*=.+(?:\/\s*>))/ nocase
		$n = /(?:[^\w+-;]\s+[\w\/\\\*]+\s*=)/ nocase
		$o = /(?:\"+.*[<=]\\s*\"[^\"]+\")|(?:\"\\w+\\s*=)|(?:>\\w=\\\/)/ nocase

	condition:
		$m and $n and $o
}


rule ObfuscationPattern_javaScript
{ 
	meta:
		impact = 0
	strings:
		$eval = "eval" nocase fullword
		$charcode = "String.fromCharCode" nocase fullword
		$loc = "location" nocase fullword
		$deanEdwards = "function(p,a,c,k,e,d)" nocase
	condition:
		2 of them
}

