all_tools = [
    ('ir8t','A collection of scripts/tools.', 'ir8t=ir8tools.tools:main'),
    ('pwned','Check if your password is on password dictionaries.', 'pwned=ir8tools.pwned:main'),
    ('ipinfo','Show info about an IP.', 'ipinfo=ir8tools.ipinfo:main'),
    ('gittu','One command commit and push.', 'gittu=ir8tools.gittu:main'),
    ('echoargs','Echos args passed to it.','echoargs=ir8tools.echoargs:main'),
    ('dnswho','Who is your dns server.','dnswho=ir8tools.dnswho:main'),
    ('dnsinfo','Show dns records of a domain.','dnsinfo=ir8tools.dnsinfo:main'),
    ('adata','Show airtel (Bangladesh) data balance from command line.','adata=ir8tools.automatify_tools.adata:main')
]

def get_tool_links():
    r = list()
    for i in all_tools:
        r.append(i[2])
    return r

def print_tool_list():
    print('Tool Name'.ljust(16) ,'Short Description')
    print(('-'*9).ljust(16), ('-'*17))
    
    for i in all_tools[1:]:
        print(i[0].ljust(16) ,i[1])

