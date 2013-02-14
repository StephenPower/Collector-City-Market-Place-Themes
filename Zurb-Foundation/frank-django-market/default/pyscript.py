import os
import sys
import datetime
import re
import shutil

FILEDIR = "templates"
DESIGNDIR = "design"
ASSETSDIR = "assets_url"
ASSETS_ORG = "assets"

notParse = ['404.html', 'layout.html']

SUBCONTENT = "{{ content }}"
now = datetime.datetime.now()
nowDate = now.strftime("%Y-%m-%d %H:%M")
menuBlok = """<UL>
	<LI><P STYLE="margin-bottom: 0in"><A NAME="menu-primary"></A><A HREF="home.html">Home</A>
		</P>
	<LI><P STYLE="margin-bottom: 0in"><A HREF="for_sale.html">For Sale</A>
		</P>
	<LI><P STYLE="margin-bottom: 0in"><A HREF="auctions.html">Auctions</A>
		</P>
	<LI><P STYLE="margin-bottom: 0in"><A HREF="blog.html">Blog</A> 
	</P>
	<LI><P STYLE="margin-bottom: 0in"><A HREF="about_us.html">About Us</A>
		</P>
	<LI><P STYLE="margin-bottom: 0in"><A HREF="login.html">Login</A> 
	</P>
	<LI><P><A HREF="register.html">Register</A> 
	</P>
</UL>"""


mailListBlok = """
<DIV ID="mail_list_form" DIR="LTR">
	<FORM NAME="form" ACTION="../shellscript" METHOD="POST">
		<P><A NAME="id_email"></A><A NAME="mail_list_submit_btn"></A>Enter
		Your Email Address: <INPUT TYPE=TEXT NAME="email" SIZE=22 MAXLENGTH=75 STYLE="width: 1.92in; height: 0.31in">
		<INPUT TYPE=SUBMIT VALUE="Subscribe" STYLE="width: 1.16in; height: 0.4in">
				</P>
	</FORM>
</DIV>
"""
forLinks = """
<P><A HREF="home.html">Home</A></P>
<P><A HREF="auctions.html">Auctions</A></P>
<P><A HREF="for_sale.html">For Sale</A></P>
<P><A HREF="login.html">Login</A></P>
<P><A HREF="register.html">Register</A></P>
"""

def replaceCSS(path):
    cssFile = open(path)
    cssFileContent = cssFile.read()
    
    cssFileContent = re.sub( r'({{ (.*) }})', lambda L: cssChange(L), cssFileContent)
    cssFile = open(path, 'w')
    cssFile.write(cssFileContent)
def cssChange(arg):
    assets = arg.group(2)
    name, asset = assets.split("|")
    name = name.replace("'", "").strip()
    name = name.replace("{{", "")
    name = name.replace("}}", "")
    name = name.strip()
    cssPath = name
    return cssPath
def replaceLinks(arg):
     assets = arg.group(2)
     assets = assets.replace('href="', "")
     name, asset = assets.split("|")
     name = name.replace("'", "").strip()
     name = name.replace("{{", "")
     name = name.replace("}}", "")
     name = name.strip()
     cssPath = 'assets_url/' + name
     replaceCSS(cssPath)
     return 'href="../assets_url/' + name
     
def replaceDict(dictName, htmlString):
    htmlOut = htmlString
    for key in dictName:
        htmlOut = htmlOut.replace(key,  dictName[key])


        if "for link in links" in htmlOut:
            htmlOut = re.sub('\{% for link .*[\w\s]*.*[\w\s]*\{% endfor %\}', forLinks, htmlOut) 
            
            
            #htmlOut = re.sub(r'{% for link in links %} .*{% endfor %}', forLinks, htmlOut )   
            
    return htmlOut

replaceDir= { '{{ url_my_orders }}': 'my_orders.html', '{{ home.image.url }}': 'http://s3.amazonaws.com/market-media.greatcoins.com/img/no-photo-shop.png ', '{{ url_terms_of_service }}': 'terms_of_service.html', '{{ url_privacy_policy }}': 'privacy_policies.html',  '{{ url_refund }}': 'refund.html', '{{ home.body }}': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec ut massa sed lacus feugiat cras amet. ', '{{ home.title }}': 'Django Market Home Page', '{{ shop_name }}': 'Django Market Theme Designer', '{{ shop_name|title }}': 'Django Market Theme Designer  ', '{{ page_title }}': 'Django Market (html-name.html) Page',  '{{ url_search }}': 'search.html', '{{ url_my_shopping }}': 'my_shopping.html', '{{ total_cart_items }}': '10',  '{{ page_description }}': ' ',  '{{ header }}' : '', '{{ flash }}': '', '{{ menu }}': menuBlok, '{{ about|truncate(100) }}': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce a blandit lectus. Praesent cras amet.', '{{ last_post.url }}' : 'blog.html', '{{ last_post.title }}': 'Django Market Blog Post', '{{ last_post.date_time }}':  nowDate, '{{ mailing_list }}': mailListBlok } 


if not os.path.exists(DESIGNDIR):
    os.makedirs(DESIGNDIR)
else:
    answer = raw_input('Folder designer exists.Do you want to remove it and recreate it with new files? Y/N')
    if answer in  ['y', 'Y']:
        shutil.rmtree(DESIGNDIR)
        print 'Folder designer deleted and recreated'
        os.makedirs(DESIGNDIR)
    else:
        sys.exit()

if not os.path.exists(ASSETSDIR):
    shutil.copytree(ASSETS_ORG, ASSETSDIR)
else:
    answer = raw_input('Folder assets_url exists.Do you want to remove it and recreate it with new files? Y/N')
    if answer in  ['y', 'Y']:
        shutil.rmtree(ASSETSDIR)
        print 'Folder assets_url deleted and recreated'
        shutil.copytree(ASSETS_ORG, ASSETSDIR)

    else:
        sys.exit() 

layoutFile= open(FILEDIR + os.sep + "layout.html")
layoutHTML = layoutFile.read()
layoutHTML = replaceDict(replaceDir, layoutHTML)
layoutHTML = re.sub( r'href="({{ (.*) }})', lambda L: replaceLinks(L), layoutHTML)


for fileName in os.popen("ls " + FILEDIR):
    fileName = fileName.strip()
    
    fileHTML = open(FILEDIR + os.sep + fileName.strip())
    fileHTML = fileHTML.read()
    if fileName in notParse:
        continue
    newContent = layoutHTML.replace(SUBCONTENT, fileHTML)

    newContent = replaceDict(replaceDir, newContent)
    outputFile = open(DESIGNDIR + os.sep + fileName, 'w')
    
    outputFile.write(newContent)
print 'DONE'
