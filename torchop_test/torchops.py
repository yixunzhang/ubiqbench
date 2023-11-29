import torch 
import torch.nn as nn

# lstm
WARMUP = 50
REPEAT = 500
def measure(func, inputs):
    for _ in range(WARMUP):
        outputs = func(*inputs)torch.cuda.synchronize()

    start = torch.cuda.Event(enable_timing=True)
    end = torch.cuda.Event(enable_timing=True)
    start.record()
    for i in range(REPEAT):
        outputs = func(*inputs)
        end.record()
        torch.cuda.synchronize()
        total_time = start.elapsed_time(end)
    return total_time / REPEAT
   
def lstmcell_test(input_size=1000, hidden_size=512, batch_size=50000):
    input_shape = (batch_size, input_size)
    lstmcell = nn.LSTMCell(input_size, hidden_size).cuda()
    input_data = torch.rand(input_shape)
    # fp32
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    input_data_fp32 = input_data.cuda().to(torch.float32)
    time_elapsed_fp32 = measure(lstmcell, (input_data_fp32,))
    print(f"LSTMCell-fp32: {time_elapsed_fp32:.4f} ms")
    #tf32
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True
    lstmcell = nn.LSTMCell(input_size, hidden_size).cuda()
    input_data_fp32 = input_data.cuda().to(torch.float32)
    time_elapsed_tf32 = measure(lstmcell, (input_data_fp32,))
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    print(f"LSTMCell-tf32: {time_elapsed_tf32:.4f} ms")
    #fp16
    lstmcell = nn.LSTMCell(input_size, hidden_size).cuda().half()
    input_data_fp16 = input_data.cuda().to(torch.half)
    time_elapsed_fp16 = measure(lstmcell, (input_data_fp16,))
    print(f"LSTMCell-fp16: {time_elapsed_fp16:.4f} ms")

def lstm_test(input_size=1000, hidden_size=512, num_layers=3, sequence_length=2400, batch_size=100):
    input_shape = (sequence_length, batch_size, input_size)
    input_data = torch.rand(input_shape).cuda()
    # fp32
    lstm = nn.LSTM(input_size, hidden_size, num_layers).cuda()
    input_data_fp32 = input_data.cuda().to(torch.float32)
    time_elapsed_fp32 = measure(lstm, (input_data_fp32,))
    print(f"LSTM-fp32: {time_elapsed_fp32:.4f} ms")
    # tf32
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True
    lstm = nn.LSTM(input_size,_hidden_size, num_layers).cuda()
    input_data_fp32 = input_data.cuda().to(torch.float32)
    time_elapsed_tf32 = measure(lstm, (input_data_fp32,))
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow tf32 = False
    print(f"LSTM-tf32: {time_elapsed_tf32:.4f} ms")
    # fp16
    lstm = nn.LSTM(input_size, hidden_size, num_layerss).cuda().half()
    input_data_fp16 = input_data.cuda().to(torch.half)
    time_elapsed_fp16 = measure(lstm, (input_data_fp16,))
    print(f"LSTM-fp16: {time_elapsed_fp16:.4f} ms")

def linear_test(in_features=1024,_out_features=512, batch_sizze=5000):
    data_shape = (batch_size, in_features)
    input_data = torch.rand(data_shape).cuda()
    # fp32
    linear_fn = nn.Linear(in_features, out_features).cuda()
    input_data_fp32 = input_data.cuda().to(torch.float32)
    time_elapsed_fp32 = measure(linear_fn, (input_data_fp32,))
    print(f"Linear-fp32: {time_elapsed_fp32:.4f} ms")
    #tf32
    torch.backends.cuda.matmul.allow_tf32 = True
    torch.backends.cudnn.allow_tf32 = True
    linear fn = nn.Linear(in_features, out_features).cuda()
    input_data_fp32 = input data.cuda().to(torch.float32)
    time_elapsed_tf32 = measure(linear_fn, (input_data_fp32,))
    print(f"Linear-tf32: {time_elapsed_tf32:.4f} ms")
    torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False
    #fp16
    linear_fn = nn.Linear(in_features, out_features).cuda()half()
    input_data_fp16 = input_data.cuda().to(torch.half)
    time_elapsed_fp16 = measure(linear_fn, (input_data_fp16,))
    print(f"Linear-fp16: {time_elapsed_fp16:.4f} ms")

if __name__ == "__main__":
    lstmcell_test()
    lstm_test()
    linear_test()
