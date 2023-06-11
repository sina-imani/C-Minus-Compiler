# IAWT

test_dir="Testcases/S$1"
cp $test_dir/input.txt .
python3 compiler.py
echo "found errors:"
cat semantic_errors.txt
echo "expected:"
cat $test_dir/semantic_errors.txt
echo "diff:"
diff semantic_errors.txt $test_dir/semantic_errors.txt
echo ""
