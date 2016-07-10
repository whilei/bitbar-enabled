#!/bin/bash

# <bitbar.title>Aliaz</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Isaac</bitbar.author>
# <bitbar.author.github>irstacks</bitbar.author.github>
# <bitbar.desc>List available bash aliases.</bitbar.desc>
# <bitbar.image></bitbar.image>
# <bitbar.dependencies></bitbar.dependencies>


echo "∷ | color=#0033cc"  # ∷ ⚯ ɐ ª
echo '---'

$(alias) | while read line; do 
	echo "$line" | sed -e 's/\(alias \)*//g' 
done
