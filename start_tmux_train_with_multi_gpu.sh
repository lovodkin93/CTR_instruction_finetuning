cuda_visible_device="0,1,5,6"
session=$1
accelerator_config_file="/home/nlp/sloboda1/controlled_reduction/instruction_finetuning/multi_gpu_training_configs.yaml"
command="export && conda activate instruction_tuning_37 && cd ~/controlled_reduction/instruction_finetuning && PYTHONPATH=/home/nlp/sloboda1/controlled_reduction/instruction_finetuning CUDA_VISIBLE_DEVICES=${cuda_visible_device} accelerate launch --config_file ${accelerator_config_file} src/train_with_LORA_copy.py" 


tmux new-session -d -s $session
tmux send-keys -t $session "$command" C-m
tmux attach-session -t $session
