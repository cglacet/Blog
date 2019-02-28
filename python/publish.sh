if [ "$#" -le 0 ]; then
   echo "Error: you have to provide a commit message to publish."
   exit 128
fi

commitmsg="$*"

if [ ${#commitmsg} -lt 5 ]; then
   echo "Error: commit message should be at least 5 characters long."
   exit 128
fi

jupyter nbconvert --stdout --to markdown notes.ipynb > README.md
git add notes.ipynb README.md
git commit -m "$commitmsg"
git push origin master

exit 0
