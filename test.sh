make build 

echo "Downloading books..."
wget https://www.gutenberg.org/cache/epub/71838/pg71838.txt
mv pg71838.txt ./tests

echo "Running tests..."
for regex in "(t.h)|(T.h)" "" " " "a|b|c|d|e" "." ".." "..." "...." "(0|1|3|4)+"
do
    time cat ./tests/pg71838.txt  | ./dist/egrep/egrep $regex > /dev/null
    echo "Above the test results for regex '$regex'"
done
