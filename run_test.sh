# IAWT

test_dir="Testcases/T$1"
cp $test_dir/input.txt .
python3 compiler.py
./tester_linux.out > result.txt
echo "result:"
cat result.txt
echo "expected:"
cat $test_dir/expected.txt
echo ""
