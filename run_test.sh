# IAWT

test_dir="testcases/T$1"
cp $test_dir/input.txt .
python3 compiler.py
echo lexical_errors.txt:
diff lexical_errors.txt $test_dir/lexical_errors.txt
echo symbol_table.txt:
diff symbol_table.txt $test_dir/symbol_table.txt
echo tokens.txt
diff tokens.txt $test_dir/tokens.txt
