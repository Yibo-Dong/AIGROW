# Readme

The artifact for `AIGROW`, a generation tool for bit-level hardware model checking benchmarks.
The platform is Ubuntu20.04 here. It shall also work similarly on other platforms.

Since the limitation of package size, we cannot include all the benchmarks generated here -- we put them on the GitHub repository: https://github.com/Anonymous0U0/AIGROW.

[TOC]

## Organization of this repository
```
.
├── logs&figs               // Experiment results and corresponding figures.
│   ├── RQ1
│   ├── RQ2
│   ├── RQ3
│   └── RQ3-scatter-point
├── packages                // Offline packages that might help.
└── tool                    // All the generation tools.
    ├── backward-car-feedback   // AIGOW-bCAR
    ├── forward-car-feedback    // AIGOW-fCAR
    ├── ic3ref-feedback         // AIGOW-ic3ref
    ├── pdr-feedback            // AIGOW-abcpdr
    └── tool-compare
        ├── aigen               // AIGEN
        ├── aigfuzz             // AIGFUZZ
        ├── aigrow-no-feedback  // AIGOW-no-feed
        └── aigrow-single-thread
            ├── backward-car-feedback
            ├── forward-car-feedback
            ├── ic3ref-feedback
            └── pdr-feedbackcd
```

## Compile and run

We implemented our approach on top of three hardware model checkers: ABC-pdr, IC3-ref, and simpleCAR.
Note that each of these model checkers has its own way of printing outputs, so we keep a separate variant for each.

### Install dependencies and compile relevant tools
Some offline packages are provided here in `packages/dpkg/`, and you can install them with `sudo dpkg -i packages/dpkg/* `. 
Though, We suggest you skip this step for now and only come back later if you find a package required is missing.

Then, install python dependencies. 
```shell
# Install python dependencies:
pip3 install -r requirements.txt 
```

Compile the hardware model checkers and the AIGER suit.
```shell
# compile the checkers.
make all -j8
```
Afterwards, the binaries are kept in `./bin`, like this :
```shell
bin/
├── IC3
├── abc
├── aigfuzz
├── aigtoaig
└── simplecar
```

### Run the Tool
Each variant is kept in a separate folder. We also include the scripts for processing the result.

Note: In this step, there may be such warning info:

```
Exception ignored in: <_io.TextIOWrapper name='<stdout>' mode='w' encoding='utf-8'>
BrokenPipeError: [Errno 32] Broken pipe
```

It's due to the timeout. If you see it, just discard it.

### feedback from ABC-PDR
For example, in pdr-feedback:
```shell
tool/pdr-feedback/
├── bin                 // contains GraFuzzer.py(the generator) and links to binaries
├── deal_record_pdr.py  // the script to deal with the record.
├── feedback_pdr.py     // main of AIGROW-pdr-feedback
├── generate_thread.sh      // helper script used in feedback_pdr
├── params              // the param input to control probabilities of componnets, i.e. INPUT/LATCH/AND-GATE.
├── re_generate_thread.sh   // helper script used in feedback_pdr
└── run.sh              // entrance wrapper.
```

You could run AIGROW with pdr-feedback with the following commands:
```shell
cd tool/pdr-feedback
chmod +x run.sh
timeout 100 ./run.sh
```
The benchmarks generated and the logs are stored in directory `aigerfile_thread` and `result_thread` in `tool/pdr-feedback` respectively.

And you could check the result log:
```shell
python3 deal_record_pdr.py result_thread
cat result_thread/table.txt
```
The benchmarks' information are shown in the `result_thread/table.txt`.

Here, due to the short time limit, the benchmark generated is not very challenging compared to a 24h experiments.

The 24h experiments results are in the `logs&figs` directory, and the efficiency of our approach will be shown in the second step.

### feedback from IC3-ref

Run AIGROW for IC3ref and wait 100s:
```shell
cd tool/ic3ref-feedback
chmod +x run.sh
timeout 100 ./run.sh
```
Same as pdr, the benchmarks generated and the log are stored in directory `aigerfile_thread` and `result_thread` in `tool/ic3ref-feedback` respectively.

Check the result log:
```shell
cat result_thread/record.txt 
```

### feedback from SimpleCAR
Run AIGROW for Backward CAR and wait 100s and check the log:
```shell
cd tool/backward-car-feedback
chmod +x run.sh
timeout 100 ./run.sh
```
Check the result log:
```shell
cat result_thread/record.txt 
```

Run AIGROW for Forward CAR, wait 100s and check the log:
```shell
cd ../..
cd tool/forward-car-feedback
chmod +x run.sh
timeout 100 ./run.sh
```
Check the result log:
```shell
cat result_thread/record.txt 
```
The benchmarks generated and the log are also stored in directory `aigerfile_thread` and `result_thread` in `tool/backward-car-feedback` or `tool/forward-car-feedback` respectively.


## Experiments Reproduction
### The visualization of 24h experiments
The efficiency of AIGROW will be shown in this step.

#### RQ1
The comparison of the efficiency of different tools in generating challenging benchmarks and the performance of AIGROW on different model checkers with different parameters will be shown here. It is related to the Fig.3 and Fig.6 in the submission paper.

```shell
cd logs\&figs/RQ1
cd compare/aigfuzz/ && tar -zxvf records.tar.gz && cd ../../
python3 plot.py
python3 plot2.py
```
RQ1-Fig3.pdf and RQ1-Fig4.pdf is the result of data dealing.

#### RQ2
The QualityRatio of benchmarks generated by different tools will be shown here. It is related to the Fig.4 in the submission paper. These csv files are processed by the original data.

```shell
cd ../..
cd logs\&figs/RQ2
chmod +x vis_quality_retio.sh
./vis_quality_retio.sh
```
The result files are stored in the corresponding folders. For instance: `abc-pdr/abc-pdr.pdf`


#### RQ3
Back to `AIGROW` directory.
The generation procedures of the top 10 hard-to-solve benchmarks will be shown here. It is related to the Fig.6 in the submission paper.
```shell
cd ../..
cd logs\&figs/RQ3
chmod +x vis_relation.sh
./vis_relation.sh
```
The results will be `abc-pdr/relation.pdf`, `ic3-ref/relation.pdf`, `backward_car/relation.pdf`, `forward_car/relation.pdf` respectively.

#### RQ3 scatter
And also the figure for cross comparison:
```shell
cd ../..
cd logs\&figs/RQ3-scatter-point
python3 draw.py
```

## Integrate with your model checker

To integrate with other model checkers:

1. Copy any subfolder from `./tool/` and rename it to `your-checker-feedback`.

   ```bash
   cd ./tool
   cp -r ic3ref-feedback your-checker-feedback
   ```

2. Rename `validation_ic3.sh` and `feedback_ic3.py` to `validation_your-checker.sh` and `feedback_your-checker.py`.

   ```bash
   cd ./your-checker-feedback
   mv validation_ic3.sh validation_your-checker.sh
   mv feedback_ic3.py feedback_your-checker.py
   ```

3. Edit `validation_your-checker.sh` by replacing the command with the path and parameters of your checker. Example:

   ```shell
   timeout 2h your-checker-path -your-checker-para "temp/gen$1.aig" temp
   ```

4. Update all relevant filenames in `feedback_your-checker.py.`(line20-line22)

   ```python
   cmd_gen = './generate_thread.sh '
   cmd_regen = './re_generate_thread.sh '
   cmd_ic3 = './validation_your-checker.sh '
   ```

5. Update all relevant filenames in `run.sh`.

   ```shellscript
   rm -rf result_thread
   rm -rf aigerfile_thread
   rm -rf temp
   chmod +x validation_your-checker.sh
   chmod +x generate_thread.sh
   chmod +x re_generate_thread.sh
   chmod +x bin/aigtoaig
   mkdir result_thread
   mkdir aigerfile_thread
   mkdir temp
   python3 feedback_your-checker.py
   ```

6. &#x20;run the file

```bash
chmod +x run.sh
./run.sh
```

## Appendix Results

### Appendix A

The source code is placed at: `additional/sourceCode.zip`.

The benchmarks are available at: https://zenodo.org/records/14156844 ,`benchmarks_aiger.tar.gz`.

To build:

```shell
make
```

To run:

```shell
$ ./simpleCAR -f|-b [-br 1][-rs] <AIGER_file.aig> <OUTPUT_PATH>
```

Options:

- Original options:

  - -f: forward searching
  - -b: backward searching
  - -br 1: enable branching heuristic
  - -rs: enable refer-skipping heuristic

- New optimization options:

  - `--pick <pickEnum>` : the `pickOrder` optimization, where

    ```c++
    enum PickEnum{
    	PickBasic 	= 0, // the basic approach
    	PickUC		= 1, // according to #(uc) generated in last round. NOTE: mUC is not considered.
    	PickI		= 2, // always pick the initial state(s).
        PickDegree  = 5, // how many children it had generated **within the whole run**.
    };
    ```

  - `-reduce <ratio>`: the `ReduceRatio` optimization.

- New makefile option:

  - `make CONTAINER=STACK` : use original stack as the container
  - `make CONTAINER=PQ`: the `Container` optimization.

The experiment result and corresponding logs, as well as counter-examples are placed at `additional/results`. The certificates(of safe cases) are too large -- together more than 10GB, compressed package more than 3GB -- therefore are left out.

### Appendix B

As shown above in RQ1, `Fig4.pdf`.
