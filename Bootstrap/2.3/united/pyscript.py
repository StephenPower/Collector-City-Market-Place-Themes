import os
import sys
import datetime
import re
import shutil
import webbrowser


FILEDIR = "templates"
DESIGNDIR = "design"
ASSETSDIR = "assets_url"
ASSETS_ORG = "assets"
notParse = ['404.html', 'layout.html']
SUBCONTENT = "{{ content }}"
now = datetime.datetime.now()
nowDate = now.strftime("%Y-%m-%d %H:%M")

menuBlok = """<ul class="nav">
<li><a href="home.html">Home</a></li>
<li><a href="for_sale.html">For Sale</a></li>
<li><a href="auctions.html">Auctions</a></li>
<li><a href="blog.html">Blog</a></li>
<li><a href="about_us.html">About Us</a></li>
    <li><a href="login.html" id="">Login</a></li>
<li><a href="register.html">Register</a></li>
</ul>
"""
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
searchBlock = """
{% if results|length  == 60 %}
   <div class="NoResults">
      <div class="span2 debar-nav well hidden-phone">
         <ul class="nav nav-list unstyled">
            {% for categories in shop_categories %}
            <li><a href="/search/?q={{categories.name}}">{{ categories.name }}</a></li>
            {% endfor %}
         </ul>
      </div>
      <div class="span8">
         <h2>Sorry we didn't have what you wanted...</h2>
         <h3>Please Look at Our...</h3>
         <b><a href="/for_sale/">Rare Coins For Sale</a></b>
            <p><b> <a href="/auctions/">Online Coin Auctions</a></b></p>
            <p><b> <a href="/home">Our Home Page</a></b></p>
     </div>
   </div>
</div>
   {% else %}"""
   
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
     
def replaceImg(arg):
     assets = arg.group(2)
     assets = assets.replace('src="', "")
     if len(assets.split("|")) == 2:
        name, asset = assets.split("|")
        name = name.replace("'", "").strip()
        name = name.replace("{{", "")
        name = name.replace("}}", "")
        name = name.strip()
     
        return 'src="../assets_url/' + name
def replaceDict(dictName, htmlString):
    htmlOut = htmlString
    for key in dictName:
        htmlOut = htmlOut.replace(key,  dictName[key])


        if "for link in links" in htmlOut:
            htmlOut = re.sub('\{% for link .*[\w\s]*.*[\w\s]*\{% endfor %\}', forLinks, htmlOut) 
            
            
            #htmlOut = re.sub(r'{% for link in links %} .*{% endfor %}', forLinks, htmlOut )   
            
    return htmlOut

replaceDir= { 
'{{ url_terms_of_service  }}': 'terms_of_service.html',
'{{ url_privacy_policy  }}': 'privacy_policies.html',
'{{ url_refund  }}': 'refund.html',
'{{ about|truncate(100) }}': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec ut massa sed lacus feugiat cras amet. ',
'{{ url_my_orders }}': 'my_orders.html', '{{ home.image.url }}': 'http://s3.amazonaws.com/market-media.greatcoins.com/img/no-photo-shop.png ',
'{{ url_terms_of_service }}': 'terms_of_service.html',
'{{ url_privacy_policy }}': 'privacy_policies.html',
'{{ url_refund }}': 'refund.html',
'{{item.url}}': 'view_item.html',
'{{ home.body }}': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec ut massa sed lacus feugiat cras amet. ',
'{{ home.title }}': 'Django Market Home Page',
'{{ shop_name }}': 'Django Market Theme Designer',
'{{ shop_name|title }}': 'Django Market Theme Designer  ',
'{{ url_search }}': 'search.html',
'{{ url_my_shopping }}': 'my_shopping.html',
'{{ total_cart_items }}': '10',
'{{ page_description }}': ' ',
'{{item.title|title}}': 'For Sale Item 1',
'{{ header }}': '',
'searchBlock': '',
'<a href="/about_us/">': 'about_us.html',
'{{item.description|truncate(100)}}': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce a blandit lectus. Praesent cras amet.Lorem ipsum dolor sit amet,Lorem ipsum dolor sit amet',
'<h3>No items for sale.</h3>': '',
'{{item.description|truncate(100)}}': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce a blandit lectus. Praesent cras amet.Lorem ipsum dolor sit amet,Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce a blandit lectus. Praesent cras amet.Lorem ipsum dolor sit amet,',
'{{lot.title|title}}': 'Lot Title 1 For Bid',
'{{lot.title|title}}': 'Lot Title 1 For Bid',
'{{ lot.time_left }} ({{ lot.session_end }})': '14 Hours, 2 Minutes',
'{{lot.price}}': '$1232.32',
'{{ lot.category }}': 'Gold',
'{{ item.category }}': 'Gold',
'{{ item.subcategory }}': 'Double Eagles',
'{{ post.url }}': 'view_post.html',
'{{ post.title }}': 'Blog Post Title',
'/for_sale/': 'for_sale.html',
'/auctions/': 'auctions.html',
'/home': 'home.html',
'{{ post.date_time }}': nowDate,
'{{ post.body|safe|truncate(400) }}': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce a blandit lectus. Praesent cras amet.Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce a blandit lectus. Praesent cras amet.Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce a blandit lectus. Praesent cras amet. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce a blandit lectus. Praesent cras amet.Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce a blandit lectus. Praesent cras amet.Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce a blandit lectus. Praesent cras amet.Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce',
'{{ post.title|title }}': 'View Blog Post Title',
'{{ post.body }}': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce a blandit lectus. Praesent cras amet.Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce a blandit lectus. Praesent cras amet.Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce a blandit lectus. Praesent cras amet. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce a blandit lectus. Praesent cras amet.Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce a blandit lectus. Praesent cras amet.Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce a blandit lectus. Praesent cras amet.Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce a blandit lectus. Praesent cras amet.Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce a blandit lectus. Praesent cras amet.Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce a blandit lectus. Praesent cras amet.',
'<h3 class="title">No lots in this session.</h3>': ' ',
'{{ lot.subcategory }}': 'Quarter Eagle',
'{{ item.description }}': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce a blandit lectus. Praesent cras amet.Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce a blandit lectus. Praesent cras amet.Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce a blandit lectus. Praesent cras amet.',
'{{ lipsum(5,false,20,35) }}': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce a blandit lectus. Praesent cras amet.Lorem ipsum dolor sit amet,',
'{{ lot.description }}': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce a blandit lectus. Praesent cras amet.Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce a blandit lectus. Praesent cras amet.Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce a blandit lectus. Praesent cras amet.',
'{{item.price}}': '$1232.32',
'{{ about.title|title }}': 'About Django Market Shop',
'{{ sessions }}': '<ul class="nav"><li class="active">Session 1:</li><li>Febuary 10th 2014</li><li>Session 2</li><li>Febuary 18th 2092</li></ul>',
'{{ about.body }}': 'Django Market Is the Python Open source alternative to other PHP based shopping carts. In addition, we have a built in marketplace for our shops to enable them to see additonal goods and services. See GitHub For more information',
'<img src="{% if item.image.small %}{{ item.image.small }}{% else %}{{ ': '',
'no_photo_small.png': '',
'|asset_url }}{% endif %}" alt="{{ item.title }}" />': '<script src="holder.js"></script> <img src="holder.js/100x100">',
'{{ flash }}': '',
'{{ categories.name }}': 'Gold',
'{{ footer }}': '', 
'{{ menu }}': menuBlok,
'{{ about|truncate(100) }}': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce a blandit lectus. Praesent cras amet.',
'{{ last_post.body|truncate(100) }}': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce a blandit lectus. Praesent cras amet.',
'{{ last_post.url }}' : 'blog.html',
'{{ last_post.title }}': 'Django Market Blog Post',
'{{ last_post.date_time }}':  nowDate,
'{{ mailing_list }}': mailListBlok 
} 


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


def stripAllTags(html):
    outHtml = re.sub( r'{% (.*) %}', "", html)
    return outHtml

for fileName in os.popen("ls " + FILEDIR):
    fileName = fileName.strip()
    replaceDir['{{ page_title }}'] = 'Django Market ' + fileName 
    
    fileHTML = open(FILEDIR + os.sep + fileName.strip())
    fileHTML = fileHTML.read()
    if fileName in notParse:
        continue
    newContent = layoutHTML.replace(SUBCONTENT, fileHTML)

    newContent = replaceDict(replaceDir, newContent)
    newContent = stripAllTags(newContent)
    
    newContent = re.sub( r'src="({{ (.*) }})', lambda L: replaceImg(L), newContent)
    
    outputFile = open(DESIGNDIR + os.sep + fileName, 'w')
    outputFile.write(newContent)
    
print 'DONE'
os.system("open "+DESIGNDIR +os.sep+"home.html");
