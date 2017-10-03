# MHFGM


This is an implementation of learning Semi-Supervised Factor Graph Model, including Metropolis-Hastings (MH) and Two-chain Metropolis-Hastings (MH+) algorithms. If you have any problem with the code and data format, please contact the author by yujieq@csail.mit.edu.

## Compile & Run

For compiling, simply use `make`.

For running, the command is 

```
MHFGM [-est/-inf] [options]
	-est: training mode
	-inf: inference mode
	-method [MH/MH1]: specify learning algorithm, where MH1 stands for MH+
	-train [filename]: training file
	-param [filename]: input initialized model file (optional)
	-state [filename]: input initialized state file (optional)
	-model [filename]: output model file
	-pred [filename]: output prediction file
	-niter [number]: the maximum iterations in training
	-ninferiter [number]: the maximum iterations in evaluation/infernce
	-learnrate [number]: learning rate η
	-neval [number]: δ, evaluate the model after each δ iterations
	-earlystop [number]: ε, stop learning if validation accuracy does not increase for ε evaluations
	-batch [number]: batch size
	-thread [number]: number of threads
```

Example

```
./MHFGM -est -method MH1 -train input_fb.txt -niter 10000 -ninferiter 10000 -thread 1 -neval 100 -batch 100 -learnrate 1
```

## Data Format

Training file consists of two parts: node and edge.

The first part is node. Each line represent a node (instance), and the format is defined as follows:

```
[+/*/?]label featname_1:val featname_2:val ...
```
where `+/*/?` each stands for training/validation/testing data, labels and feature names can be strings (length<32). The value can be real-valued or 0/1. We suggest to normalize the input features to [0,1].

The second part is edge. Each line represent an edge (correlation between two instances). The format is:

```
#edge line_a line_b edgetype
```
where `line_a`, `line_b` correspond to two nodes in the first part, and lines are counted starting with 1. `edgetype` is a string indicating the type of this edge. Currently the code only support one type.

