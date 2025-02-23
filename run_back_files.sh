# #!bin/zsh

# this is a shebang this tell the comipler whuich interpreter to use

echo "Starting get_file_dat_API.py..."
python get_file_dat_API.py

echo "Starting try_summarize.py..."
python try_summarize.py

echo "Starting get_file_types.py..."
python get_file_types.py

echo "All scripts executed."

# to run all commands in parallel we can use command1 & command2 & command3, and && I think for sequential thing
# chmod +x run_all.sh, to make it executable
