# Port-forwarding of IMageS

## Installation
1. Clone the repository
`git clone https://github.com/beringresearch/pims`

2. Install requirements
```
cd pims
pip install -r requiremenets.txt
```

3. Add PIMS to your path by adding a line at the end of your .bashrc file
```
export PATH=$PATH:/PATH/TO/PIMS/DIRECTORY
```

Source .bashrc: `source .bashrc`

## Running
On the remote machine:

`pims.py /PATH/TO/FOLDER/WITH/PNG`

On host:

`ssh -L 8050:localhost:8050 user@remote`

PIMS will start serving remote images to a local browser on `localhost:8050`
