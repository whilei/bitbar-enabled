#!/bin/bash
# website-status
# BitBar plugin
#
# Author Marc Oehler
#
# Gets the status of your website


areteh_url='http://areteh.co/#/' # replace with your url
rstacks_url='http://www.rstacks.org' # replace with your url

areteh_code=$(curl -o /dev/null --silent --head --write-out '%{http_code}\n' $areteh_url)
rstacks_code=$(curl -o /dev/null --silent --head --write-out '%{http_code}\n' $rstacks_url)

case "$areteh_code" in
"200")
    echo "•| color=green" # • 
    ;;
"301" | "302")
    echo "•| color=yellow"
    ;;
*)
    echo "•| color=red"
    ;;
esac
case "$rstacks_code" in
"200")
    echo "•| color=green" # • 
    ;;
"301" | "302")
    echo "•| color=yellow"
    ;;
*)
    echo "•| color=red"
    ;;
esac

echo "---"
echo "$areteh_url -> $areteh_code"
echo "$rstacks_url -> $rstacks_code"




