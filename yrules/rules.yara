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


	
